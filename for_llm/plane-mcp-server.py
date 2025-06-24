# Required dependencies:
#   pip install fastapi httpx prometheus_client starlette uvicorn

import os
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import httpx
import time
from prometheus_client import (
    Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
)
from starlette.responses import Response as StarletteResponse

PLANE_API_URL = os.environ.get("PLANE_API_URL", "http://localhost:51534")
PLANE_API_KEY = os.environ.get("PLANE_API_KEY", "")
PLANE_MCP_PORT = int(os.environ.get("PLANE_MCP_PORT", "43533"))

app = FastAPI(
    title="Plane MCP Server",
    description="Exposes all Plane API endpoints as MCP tools for Cursor."
)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'plane_mcp_requests_total',
    'Total Plane MCP requests',
    ['endpoint', 'method', 'status']
)
REQUEST_LATENCY = Histogram(
    'plane_mcp_request_latency_seconds',
    'Plane MCP request latency',
    ['endpoint', 'method']
)


@app.get("/metrics")
def metrics():
    return StarletteResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Example: Proxy a Plane API endpoint (GET /api/workspaces/)
@app.api_route(
    "/api/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
)
async def proxy_plane_api(path: str, request: Request):
    url = f"{PLANE_API_URL}/api/{path}"
    method = request.method
    headers = dict(request.headers)
    headers["Authorization"] = f"Bearer {PLANE_API_KEY}"
    data = await request.body()
    params = dict(request.query_params)
    start = time.time()
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.request(
                method, url, headers=headers, content=data, params=params
            )
            status = resp.status_code
            content = resp.content
            REQUEST_COUNT.labels(
                endpoint=path, method=method, status=status
            ).inc()
            REQUEST_LATENCY.labels(
                endpoint=path, method=method
            ).observe(time.time() - start)
            return Response(
                content=content, status_code=status, headers=resp.headers
            )
        except Exception as e:
            REQUEST_COUNT.labels(
                endpoint=path, method=method, status="error"
            ).inc()
            return JSONResponse({"error": str(e)}, status_code=500)


# Placeholder: MCP tool registration endpoint (for Cursor MCP protocol)
@app.post("/tools/list")
async def list_tools():
    # TODO: Dynamically enumerate Plane API endpoints as MCP tools
    return {
        "tools": [
            {
                "name": "proxy_plane_api",
                "description": "Proxy any Plane API endpoint",
                "inputSchema": {"type": "object"}
            }
        ]
    }


# Placeholder: MCP tool call endpoint
@app.post("/tools/call")
async def call_tool(request: Request):
    # TODO: Parse tool call and dispatch to proxy_plane_api
    body = await request.json()
    return {"result": "Tool call received", "body": body}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PLANE_MCP_PORT) 