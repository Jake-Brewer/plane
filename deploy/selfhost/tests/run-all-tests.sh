#!/bin/bash
# Comprehensive Test Runner for Plane Backup System
# Executes all E2E tests and provides detailed reporting

set -e

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/utils/test-helpers.sh"

# Test configuration
TEST_SUITE_NAME="Plane Backup System E2E Test Suite"
TEST_RESULTS_DIR="$SCRIPT_DIR/results"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RESULTS_FILE="$TEST_RESULTS_DIR/test_results_$TIMESTAMP.log"

# Test categories
declare -a BASELINE_TESTS=(
    "$SCRIPT_DIR/e2e/test-backup-basic.sh"
)

declare -a MISSING_FEATURE_TESTS=(
    "$SCRIPT_DIR/e2e/test-nas-resilience.sh"
)

declare -a ALL_TESTS=()
ALL_TESTS+=("${BASELINE_TESTS[@]}")
ALL_TESTS+=("${MISSING_FEATURE_TESTS[@]}")

# Global test counters
TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0
TOTAL_SKIPPED=0

# Setup function
setup_test_suite() {
    echo "🚀 $TEST_SUITE_NAME"
    echo "=================================================="
    echo "Timestamp: $(date)"
    echo "Test Results Directory: $TEST_RESULTS_DIR"
    echo
    
    # Create results directory
    mkdir -p "$TEST_RESULTS_DIR"
    
    # Initialize results file
    {
        echo "# $TEST_SUITE_NAME"
        echo "Timestamp: $(date)"
        echo "========================================"
        echo
    } > "$RESULTS_FILE"
}

# Function to run a single test and capture results
run_single_test() {
    local test_script="$1"
    local test_name
    test_name=$(basename "$test_script" .sh)
    
    echo "📋 Running: $test_name"
    echo "----------------------------------------"
    
    # Create temporary log file for this test
    local temp_log="$TEST_RESULTS_DIR/${test_name}_temp.log"
    
    # Run the test and capture output
    local test_exit_code=0
    if bash "$test_script" > "$temp_log" 2>&1; then
        test_exit_code=0
    else
        test_exit_code=$?
    fi
    
    # Display test output
    cat "$temp_log"
    
    # Extract test results from output
    local test_results
    test_results=$(grep -E "✅|❌|⚠️.*PASS|FAIL|SKIP" "$temp_log" || true)
    
    # Count results for this test
    local test_passed
    local test_failed  
    local test_skipped
    test_passed=$(echo "$test_results" | grep -c "PASS" || echo "0")
    test_failed=$(echo "$test_results" | grep -c "FAIL" || echo "0")
    test_skipped=$(echo "$test_results" | grep -c "SKIP" || echo "0")
    
    # Update global counters
    TOTAL_PASSED=$((TOTAL_PASSED + test_passed))
    TOTAL_FAILED=$((TOTAL_FAILED + test_failed))
    TOTAL_SKIPPED=$((TOTAL_SKIPPED + test_skipped))
    TOTAL_TESTS=$((TOTAL_TESTS + test_passed + test_failed + test_skipped))
    
    # Append to results file
    {
        echo "## $test_name"
        echo "Exit Code: $test_exit_code"
        echo "Passed: $test_passed | Failed: $test_failed | Skipped: $test_skipped"
        echo
        echo "### Detailed Results:"
        echo "$test_results"
        echo
        echo "### Full Output:"
        cat "$temp_log"
        echo
        echo "----------------------------------------"
        echo
    } >> "$RESULTS_FILE"
    
    # Clean up temp log
    rm -f "$temp_log"
    
    echo
}

# Function to run baseline tests (should pass)
run_baseline_tests() {
    echo "🟢 BASELINE TESTS (Should PASS with current implementation)"
    echo "=========================================================="
    echo "These tests validate existing functionality and establish"
    echo "a baseline for the current backup system capabilities."
    echo
    
    for test_script in "${BASELINE_TESTS[@]}"; do
        if [[ -f "$test_script" ]]; then
            run_single_test "$test_script"
        else
            echo "⚠️  Test script not found: $test_script"
        fi
    done
}

# Function to run missing feature tests (should fail)
run_missing_feature_tests() {
    echo "🔴 MISSING FEATURE TESTS (Should FAIL - demonstrates needed features)"
    echo "====================================================================="
    echo "These tests demonstrate functionality that needs to be implemented."
    echo "Failures indicate missing features, not broken functionality."
    echo
    
    for test_script in "${MISSING_FEATURE_TESTS[@]}"; do
        if [[ -f "$test_script" ]]; then
            run_single_test "$test_script"
        else
            echo "⚠️  Test script not found: $test_script"
        fi
    done
}

# Function to generate comprehensive summary
generate_summary() {
    echo "📊 TEST SUITE SUMMARY"
    echo "===================="
    echo "Total Tests Run: $TOTAL_TESTS"
    echo "✅ Passed: $TOTAL_PASSED"
    echo "❌ Failed: $TOTAL_FAILED"
    echo "⚠️  Skipped: $TOTAL_SKIPPED"
    echo
    
    # Calculate percentages
    if [[ $TOTAL_TESTS -gt 0 ]]; then
        local pass_percentage
        local fail_percentage
        pass_percentage=$(( (TOTAL_PASSED * 100) / TOTAL_TESTS ))
        fail_percentage=$(( (TOTAL_FAILED * 100) / TOTAL_TESTS ))
        
        echo "📈 Success Rate: $pass_percentage%"
        echo "📉 Failure Rate: $fail_percentage%"
    fi
    
    echo
    echo "💾 Detailed results saved to: $RESULTS_FILE"
    echo
}

# Function to provide implementation guidance
provide_implementation_guidance() {
    echo "🎯 IMPLEMENTATION GUIDANCE"
    echo "========================="
    echo
    echo "Based on test results, here's what needs to be implemented:"
    echo
    
    if [[ $TOTAL_FAILED -gt 0 ]]; then
        echo "❌ Failed Tests Indicate Missing Features:"
        echo "   • NAS availability detection and handling"
        echo "   • Local backup fallback when NAS offline"
        echo "   • Backup synchronization when NAS returns"
        echo "   • NAS monitoring daemon for automatic recovery"
        echo "   • Pending backup queue management"
        echo "   • Local backup retention during outages"
        echo "   • Enhanced logging and alerting"
        echo
        echo "🔧 Next Steps:"
        echo "   1. Implement enhanced backup script with NAS detection"
        echo "   2. Create sync script for pending backup recovery"
        echo "   3. Develop NAS monitoring daemon"
        echo "   4. Add configuration for resilience features"
        echo "   5. Re-run tests to validate implementations"
    else
        echo "✅ All tests passed! The backup system is fully implemented."
    fi
    
    echo
}

# Main execution function
main() {
    # Parse command line arguments
    local run_baseline=true
    local run_missing=true
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --baseline-only)
                run_missing=false
                shift
                ;;
            --missing-only)
                run_baseline=false
                shift
                ;;
            --help)
                echo "Usage: $0 [--baseline-only] [--missing-only] [--help]"
                echo "  --baseline-only   Run only baseline tests (should pass)"
                echo "  --missing-only    Run only missing feature tests (should fail)"
                echo "  --help           Show this help message"
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done
    
    # Initialize test suite
    setup_test_suite
    
    # Run selected test categories
    if [[ "$run_baseline" == true ]]; then
        run_baseline_tests
    fi
    
    if [[ "$run_missing" == true ]]; then
        run_missing_feature_tests
    fi
    
    # Generate reports and guidance
    generate_summary
    provide_implementation_guidance
    
    echo "🏁 Test suite completed successfully!"
    echo "   Check $RESULTS_FILE for detailed results"
    
    return 0
}

# Execute main function
main "$@" 