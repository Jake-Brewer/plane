#!/bin/bash
# Plane Test Utilities and Helper Functions
# Shared utilities for all test scripts

# Colors for test output
export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[1;33m'
export BLUE='\033[0;34m'
export PURPLE='\033[0;35m'
export CYAN='\033[0;36m'
export NC='\033[0m' # No Color

# Test counters
export TESTS_TOTAL=0
export TESTS_PASSED=0
export TESTS_FAILED=0
export TESTS_SKIPPED=0

# Test configuration
export TEST_TEMP_DIR="/tmp/plane-tests"
export TEST_BACKUP_DIR="$TEST_TEMP_DIR/backups"
export TEST_NAS_DIR="$TEST_TEMP_DIR/mock-nas"
export TEST_LOG_FILE="$TEST_TEMP_DIR/test.log"

# Function to initialize test environment
init_test_environment() {
    echo -e "${BLUE}🧪 Initializing test environment...${NC}"
    
    # Create test directories
    mkdir -p "$TEST_TEMP_DIR"
    mkdir -p "$TEST_BACKUP_DIR"
    mkdir -p "$TEST_NAS_DIR"
    
    # Initialize log file
    echo "$(date): Test session started" > "$TEST_LOG_FILE"
    
    echo -e "${GREEN}✅ Test environment initialized${NC}"
}

# Function to cleanup test environment
cleanup_test_environment() {
    echo -e "${BLUE}🧹 Cleaning up test environment...${NC}"
    
    # Remove test directories (be very careful here)
    if [[ "$TEST_TEMP_DIR" == "/tmp/plane-tests" ]]; then
        rm -rf "$TEST_TEMP_DIR"
        echo -e "${GREEN}✅ Test environment cleaned up${NC}"
    else
        echo -e "${RED}❌ Unsafe cleanup path: $TEST_TEMP_DIR${NC}"
    fi
}

# Function to print test header
print_test_header() {
    local test_name="$1"
    local test_description="$2"
    
    echo
    echo -e "${CYAN}================================================${NC}"
    echo -e "${CYAN}🧪 TEST: $test_name${NC}"
    echo -e "${CYAN}📝 $test_description${NC}"
    echo -e "${CYAN}================================================${NC}"
}

# Function to print test result
print_test_result() {
    local test_name="$1"
    local result="$2"  # PASS, FAIL, SKIP
    local message="$3"
    
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    
    case "$result" in
        "PASS")
            TESTS_PASSED=$((TESTS_PASSED + 1))
            echo -e "${GREEN}✅ PASS: $test_name${NC}"
            if [[ -n "$message" ]]; then
                echo -e "${GREEN}   $message${NC}"
            fi
            ;;
        "FAIL")
            TESTS_FAILED=$((TESTS_FAILED + 1))
            echo -e "${RED}❌ FAIL: $test_name${NC}"
            if [[ -n "$message" ]]; then
                echo -e "${RED}   $message${NC}"
            fi
            ;;
        "SKIP")
            TESTS_SKIPPED=$((TESTS_SKIPPED + 1))
            echo -e "${YELLOW}⏭️ SKIP: $test_name${NC}"
            if [[ -n "$message" ]]; then
                echo -e "${YELLOW}   $message${NC}"
            fi
            ;;
        *)
            echo -e "${PURPLE}❓ UNKNOWN: $test_name ($result)${NC}"
            ;;
    esac
}

# Function to print test summary
print_test_summary() {
    echo
    echo -e "${CYAN}================================================${NC}"
    echo -e "${CYAN}📊 TEST SUMMARY${NC}"
    echo -e "${CYAN}================================================${NC}"
    echo -e "${BLUE}Total Tests: $TESTS_TOTAL${NC}"
    echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
    echo -e "${RED}Failed: $TESTS_FAILED${NC}"
    echo -e "${YELLOW}Skipped: $TESTS_SKIPPED${NC}"
    
    if [[ $TESTS_FAILED -gt 0 ]]; then
        echo -e "${RED}❌ Some tests failed${NC}"
        return 1
    elif [[ $TESTS_PASSED -gt 0 ]]; then
        echo -e "${GREEN}✅ All tests passed${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️ No tests were run${NC}"
        return 1
    fi
}

# Function to run a command and capture output
run_command() {
    local command="$1"
    local expected_exit_code="${2:-0}"
    local capture_output="${3:-true}"
    
    if [[ "$capture_output" == "true" ]]; then
        local output
        output=$(eval "$command" 2>&1)
        local exit_code=$?
        
        echo "$output"
        return $exit_code
    else
        eval "$command"
        return $?
    fi
}

# Function to check if Docker is running
check_docker_running() {
    if ! docker info >/dev/null 2>&1; then
        return 1
    fi
    return 0
}

# Function to check if a Docker container exists
check_container_exists() {
    local container_name="$1"
    
    if docker ps -a --format "table {{.Names}}" | grep -q "^${container_name}$"; then
        return 0
    else
        return 1
    fi
}

# Function to check if a Docker container is running
check_container_running() {
    local container_name="$1"
    
    if docker ps --format "table {{.Names}}" | grep -q "^${container_name}$"; then
        return 0
    else
        return 1
    fi
}

# Function to wait for a condition with timeout
wait_for_condition() {
    local condition_command="$1"
    local timeout_seconds="${2:-30}"
    local check_interval="${3:-1}"
    
    local elapsed=0
    
    while [[ $elapsed -lt $timeout_seconds ]]; do
        if eval "$condition_command" >/dev/null 2>&1; then
            return 0
        fi
        
        sleep "$check_interval"
        elapsed=$((elapsed + check_interval))
    done
    
    return 1
}

# Function to create a mock backup file
create_mock_backup() {
    local backup_dir="$1"
    local backup_name="${2:-plane_backup_$(date +%Y%m%d_%H%M%S).sql.gz}"
    local backup_path="$backup_dir/$backup_name"
    
    mkdir -p "$backup_dir"
    
    # Create a mock SQL dump and compress it
    cat > "$backup_path.tmp" << 'EOF'
--
-- PostgreSQL database dump
--
-- Dumped from database version 13.7
-- Dumped by pg_dump version 13.7

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;

-- Mock table data
CREATE TABLE test_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO test_table (name) VALUES ('test_data_1'), ('test_data_2');
EOF
    
    gzip "$backup_path.tmp"
    mv "$backup_path.tmp.gz" "$backup_path"
    
    echo "$backup_path"
}

# Function to verify backup file integrity
verify_backup_integrity() {
    local backup_path="$1"
    
    if [[ ! -f "$backup_path" ]]; then
        return 1
    fi
    
    # Check if it's a valid gzip file
    if ! gzip -t "$backup_path" >/dev/null 2>&1; then
        return 1
    fi
    
    # Check if it contains SQL content
    if ! zcat "$backup_path" | head -5 | grep -q "PostgreSQL database dump"; then
        return 1
    fi
    
    return 0
}

# Function to simulate NAS unavailable
simulate_nas_offline() {
    local nas_path="$1"
    
    # Move the directory to simulate it being unavailable
    if [[ -d "$nas_path" ]]; then
        mv "$nas_path" "${nas_path}.offline"
        return 0
    fi
    
    return 1
}

# Function to simulate NAS back online
simulate_nas_online() {
    local nas_path="$1"
    
    # Move the directory back to simulate it being available
    if [[ -d "${nas_path}.offline" ]]; then
        mv "${nas_path}.offline" "$nas_path"
        return 0
    fi
    
    return 1
}

# Function to count files matching pattern
count_files() {
    local directory="$1"
    local pattern="$2"
    
    if [[ ! -d "$directory" ]]; then
        echo "0"
        return
    fi
    
    find "$directory" -name "$pattern" 2>/dev/null | wc -l
}

# Function to get file age in seconds
get_file_age_seconds() {
    local file_path="$1"
    
    if [[ ! -f "$file_path" ]]; then
        echo "-1"
        return
    fi
    
    local file_timestamp
    file_timestamp=$(stat -c %Y "$file_path" 2>/dev/null || stat -f %m "$file_path" 2>/dev/null)
    local current_timestamp
    current_timestamp=$(date +%s)
    
    echo $((current_timestamp - file_timestamp))
}

# Function to assert condition
assert() {
    local condition="$1"
    local error_message="$2"
    
    if ! eval "$condition"; then
        echo -e "${RED}❌ Assertion failed: $error_message${NC}"
        echo -e "${RED}   Condition: $condition${NC}"
        return 1
    fi
    
    return 0
}

# Function to assert file exists
assert_file_exists() {
    local file_path="$1"
    local error_message="${2:-File does not exist: $file_path}"
    
    assert "[[ -f '$file_path' ]]" "$error_message"
}

# Function to assert directory exists
assert_directory_exists() {
    local dir_path="$1"
    local error_message="${2:-Directory does not exist: $dir_path}"
    
    assert "[[ -d '$dir_path' ]]" "$error_message"
}

# Function to assert command succeeds
assert_command_succeeds() {
    local command="$1"
    local error_message="${2:-Command failed: $command}"
    
    if ! eval "$command" >/dev/null 2>&1; then
        echo -e "${RED}❌ Assertion failed: $error_message${NC}"
        echo -e "${RED}   Command: $command${NC}"
        return 1
    fi
    
    return 0
}

# Function to assert command fails
assert_command_fails() {
    local command="$1"
    local error_message="${2:-Command should have failed: $command}"
    
    if eval "$command" >/dev/null 2>&1; then
        echo -e "${RED}❌ Assertion failed: $error_message${NC}"
        echo -e "${RED}   Command: $command${NC}"
        return 1
    fi
    
    return 0
}

# Export all functions for use in other scripts
export -f init_test_environment cleanup_test_environment
export -f print_test_header print_test_result print_test_summary
export -f run_command check_docker_running check_container_exists check_container_running
export -f wait_for_condition create_mock_backup verify_backup_integrity
export -f simulate_nas_offline simulate_nas_online count_files get_file_age_seconds
export -f assert assert_file_exists assert_directory_exists
export -f assert_command_succeeds assert_command_fails 