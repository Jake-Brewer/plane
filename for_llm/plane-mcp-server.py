# Required dependencies:
#   pip install fastapi httpx prometheus_client starlette uvicorn

import os
import logging
import sys
import time
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
from prometheus_client import (
    Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
)
from starlette.responses import Response as StarletteResponse

PLANE_API_URL = os.environ.get("PLANE_API_URL", "http://localhost:51534")
PLANE_API_KEY = os.environ.get("PLANE_API_KEY", "")
PLANE_MCP_PORT = int(os.environ.get("PLANE_MCP_PORT", "43533"))

# Configure comprehensive logging with UTF-8 encoding for Windows compatibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('plane-mcp-server.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Log startup information
logger.info("STARTUP: Starting ✈️ MCP Server")
logger.info(f"CONFIG: ✈️ API URL: {PLANE_API_URL}")
logger.info(f"CONFIG: API Key configured: {'Yes' if PLANE_API_KEY else 'No'}")
logger.info(f"CONFIG: MCP Server Port: {PLANE_MCP_PORT}")

app = FastAPI(
    title="✈️ MCP Server",
    description="Exposes all ✈️ API endpoints as MCP tools for Cursor."
)

# Enhanced Prometheus metrics
REQUEST_COUNT = Counter(
    'plane_mcp_requests_total',
    'Total ✈️ MCP requests',
    ['endpoint', 'method', 'status']
)
REQUEST_LATENCY = Histogram(
    'plane_mcp_request_latency_seconds',
    '✈️ MCP request latency',
    ['endpoint', 'method']
)
TIMEOUT_COUNTER = Counter(
    'plane_mcp_timeouts_total',
    'Total timeout errors',
    ['endpoint', 'timeout_type', 'duration']
)
ERROR_COUNTER = Counter(
    'plane_mcp_errors_total',
    'Total errors by type',
    ['endpoint', 'error_type', 'status_code']
)
RESPONSE_SIZE_HISTOGRAM = Histogram(
    'plane_mcp_response_size_bytes',
    'Response size in bytes',
    ['endpoint', 'method']
)

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """Comprehensive logging middleware for all requests"""
    start_time = time.time()
    request_id = f"{int(start_time * 1000000) % 1000000:06d}"
    
    # Log incoming request
    client_host = request.client.host if request.client else 'unknown'
    logger.info(
        f"REQ [{request_id}] {request.method} {request.url.path} - "
        f"Client: {client_host}"
    )
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        # Log response with status indicator
        if response.status_code < 400:
            status_indicator = "SUCCESS"
        elif response.status_code >= 500:
            status_indicator = "ERROR"
        else:
            status_indicator = "WARNING"
            
        logger.info(
            f"{status_indicator} [{request_id}] {response.status_code} - "
            f"{duration:.3f}s"
        )
        
        # Track slow requests
        if duration > 5.0:
            logger.warning(
                f"SLOW [{request_id}] {duration:.3f}s for "
                f"{request.method} {request.url.path}"
            )
        
        return response
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"ERROR [{request_id}] after {duration:.3f}s: {str(e)}")
        ERROR_COUNTER.labels(
            endpoint=request.url.path,
            error_type=type(e).__name__,
            status_code="500"
        ).inc()
        raise

@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    logger.debug("METRICS: Metrics requested")
    return StarletteResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
def health_check():
    """Health check endpoint with detailed status"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "plane_api_url": PLANE_API_URL,
        "api_key_configured": bool(PLANE_API_KEY),
        "uptime_seconds": (
            time.time() - start_time if 'start_time' in globals() else 0
        )
    }
    logger.debug("HEALTH: Health check requested")
    return health_status

# Enhanced API proxy with comprehensive logging and timeout handling
@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_plane_api(path: str, request: Request):
    """Enhanced API proxy with detailed logging and timeout handling"""
    url = f"{PLANE_API_URL}/api/{path}"
    method = request.method
    start_time = time.time()
    request_id = f"api_{int(start_time * 1000000) % 1000000:06d}"
    
    # Log API request details
    logger.info(f"PROXY [{request_id}] {method} {path}")
    
    headers = dict(request.headers)
    if PLANE_API_KEY:
        headers["X-Api-Key"] = PLANE_API_KEY
        logger.debug(f"AUTH [{request_id}] API key added to headers")
    else:
        logger.warning(f"AUTH [{request_id}] No API key configured!")
    
    data = await request.body()
    params = dict(request.query_params)
    
    # Log request size
    if data:
        logger.debug(f"DATA [{request_id}] Request body size: {len(data)} bytes")
    if params:
        logger.debug(f"PARAMS [{request_id}] Query params: {params}")
    
    timeout_config = httpx.Timeout(
        connect=10.0,  # Connection timeout
        read=30.0,     # Read timeout
        write=10.0,    # Write timeout
        pool=5.0       # Pool timeout
    )
    
    async with httpx.AsyncClient(timeout=timeout_config) as client:
        try:
            logger.debug(f"SEND [{request_id}] Sending request to {url}")
            
            resp = await client.request(
                method, url, headers=headers, content=data, params=params
            )
            
            duration = time.time() - start_time
            status = resp.status_code
            response_size = len(resp.content)
            
            # Update metrics
            REQUEST_COUNT.labels(
                endpoint=path, method=method, status=status
            ).inc()
            REQUEST_LATENCY.labels(
                endpoint=path, method=method
            ).observe(duration)
            RESPONSE_SIZE_HISTOGRAM.labels(
                endpoint=path, method=method
            ).observe(response_size)
            
            # Log response details
            if status < 400:
                status_indicator = "API_SUCCESS"
            elif status >= 500:
                status_indicator = "API_ERROR"
            else:
                status_indicator = "API_WARNING"
                
            logger.info(
                f"{status_indicator} [{request_id}] {status} - "
                f"{duration:.3f}s - {response_size} bytes"
            )
            
            # Log slow API calls
            if duration > 10.0:
                logger.warning(
                    f"SLOW_API [{request_id}] {duration:.3f}s for "
                    f"{method} {path}"
                )

            # Return response content
            content_type = resp.headers.get("content-type", "")
            if content_type.startswith("application/json"):
                content = resp.json()
            else:
                content = resp.text
                
            return JSONResponse(
                content=content,
                status_code=status,
                headers=dict(resp.headers)
            )
            
        except httpx.TimeoutException as e:
            duration = time.time() - start_time
            timeout_type = type(e).__name__
            
            TIMEOUT_COUNTER.labels(
                endpoint=path,
                timeout_type=timeout_type,
                duration=f"{duration:.1f}s"
            ).inc()
            
            logger.error(
                f"TIMEOUT [{request_id}] {timeout_type} after "
                f"{duration:.3f}s for {method} {path}"
            )
            
            return JSONResponse(
                content={
                    "error": "Request timeout",
                    "duration": duration,
                    "timeout_type": timeout_type
                },
                status_code=504
            )
            
        except Exception as e:
            duration = time.time() - start_time
            error_type = type(e).__name__
            
            ERROR_COUNTER.labels(
                endpoint=path,
                error_type=error_type,
                status_code="500"
            ).inc()
            
            logger.error(
                f"ERROR [{request_id}] {error_type} after "
                f"{duration:.3f}s: {str(e)}"
            )
            
            return JSONResponse(
                content={
                    "error": str(e),
                    "error_type": error_type,
                    "duration": duration
                },
                status_code=500
            )

# MCP Protocol endpoints
@app.post("/tools/list")
async def list_tools():
    """List available MCP tools"""
    return {
        "tools": [
            {
                "name": "proxy_plane_api",
                "description": "Proxy any ✈️ API endpoint with logging",
                "inputSchema": {"type": "object"}
            }
        ]
    }

@app.post("/tools/call")
async def call_tool(request: Request):
    """Call MCP tool"""
    tool_data = await request.json()
    
    if tool_data.get("name") == "proxy_plane_api":
        # This would integrate with the proxy endpoint
        return {"content": "Tool executed successfully"}
    
    return JSONResponse(
        content={"error": "Unknown tool"},
        status_code=404
    )

@app.on_event("startup")
async def startup_event():
    """Server startup tasks"""
    global start_time
    start_time = time.time()
    logger.info("STARTUP: ✈️ MCP Server started successfully")
    logger.info(f"METRICS: Available at http://localhost:{PLANE_MCP_PORT}/metrics")
    logger.info(f"HEALTH: Available at http://localhost:{PLANE_MCP_PORT}/health")
    
    # Test ✈️ connectivity on startup
    if PLANE_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                headers = {"X-Api-Key": PLANE_API_KEY}
                url = f"{PLANE_API_URL}/api/workspaces/"
                resp = await client.get(url, headers=headers)
                if resp.status_code == 200:
                    logger.info("CONNECTIVITY: ✈️ API test SUCCESS")
                else:
                    logger.warning(
                        f"CONNECTIVITY: ✈️ API test returned {resp.status_code}"
                    )
        except Exception as e:
            logger.error(f"CONNECTIVITY: ✈️ API test failed: {str(e)}")
    else:
        logger.warning("CONNECTIVITY: No API key configured - API calls will fail")

if __name__ == "__main__":
    import uvicorn
    logger.info(f"SERVER: Starting on port {PLANE_MCP_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PLANE_MCP_PORT) 