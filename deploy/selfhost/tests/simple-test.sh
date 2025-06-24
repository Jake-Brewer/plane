#!/bin/bash
# Simple Test for Backup System - Windows Compatible
# Basic validation of backup system components

set -e

echo "🚀 Simple Backup System Test"
echo "============================"
echo "Testing basic backup system components..."
echo

# Test counters
TESTS_TOTAL=0
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    echo -n "🧪 Testing: $test_name... "
    
    if eval "$test_command" >/dev/null 2>&1; then
        echo "✅ PASS"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo "❌ FAIL"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Test 1: Check if backup script exists
run_test "Backup script exists" "[[ -f 'deploy/selfhost/backup-postgres.sh' ]]"

# Test 2: Check if enhanced backup script exists (should fail)
run_test "Enhanced backup script exists" "[[ -f 'deploy/selfhost/enhanced-backup-postgres.sh' ]]"

# Test 3: Check if sync script exists (should fail)
run_test "Sync script exists" "[[ -f 'deploy/selfhost/sync-nas-backups.sh' ]]"

# Test 4: Check if monitor script exists (should fail)
run_test "Monitor script exists" "[[ -f 'deploy/selfhost/monitor-nas.sh' ]]"

# Test 5: Check if restore script exists
run_test "Restore script exists" "[[ -f 'deploy/selfhost/restore-postgres.sh' ]]"

# Test 6: Check if test utilities exist
run_test "Test utilities exist" "[[ -f 'deploy/selfhost/tests/utils/test-helpers.sh' ]]"

# Test 7: Check if E2E tests exist
run_test "Basic E2E test exists" "[[ -f 'deploy/selfhost/tests/e2e/test-backup-basic.sh' ]]"
run_test "NAS resilience test exists" "[[ -f 'deploy/selfhost/tests/e2e/test-nas-resilience.sh' ]]"

# Test 8: Check backup script configuration
if [[ -f "deploy/selfhost/backup-postgres.sh" ]]; then
    run_test "Backup script has BACKUP_DIR config" "grep -q 'BACKUP_DIR=' deploy/selfhost/backup-postgres.sh"
    run_test "Backup script has DB_NAME config" "grep -q 'DB_NAME=' deploy/selfhost/backup-postgres.sh"
    run_test "Backup script has NAS path" "grep -q 'Z:' deploy/selfhost/backup-postgres.sh"
else
    echo "⚠️  Skipping backup script configuration tests (script not found)"
fi

# Test 9: Check for NAS resilience features (should fail)
if [[ -f "deploy/selfhost/backup-postgres.sh" ]]; then
    run_test "Backup script has NAS detection" "grep -q 'nas.*available\|check.*nas' deploy/selfhost/backup-postgres.sh"
    run_test "Backup script has local fallback" "grep -q 'tmp.*backup\|local.*backup\|fallback' deploy/selfhost/backup-postgres.sh"
else
    echo "⚠️  Skipping NAS resilience tests (script not found)"
fi

echo
echo "📊 Test Summary"
echo "==============="
echo "Total Tests: $TESTS_TOTAL"
echo "✅ Passed: $TESTS_PASSED"
echo "❌ Failed: $TESTS_FAILED"

if [[ $TESTS_FAILED -gt 0 ]]; then
    echo
    echo "📋 Analysis:"
    echo "============"
    echo "✅ Baseline functionality tests should PASS"
    echo "❌ NAS resilience tests should FAIL (missing features)"
    echo
    echo "This is EXPECTED behavior:"
    echo "• Current backup system works (passing tests)"
    echo "• NAS resilience features not implemented (failing tests)"
    echo "• Failed tests indicate what needs to be built"
fi

echo
echo "🎯 Next Steps:"
echo "=============="
echo "1. Review failed tests as implementation requirements"
echo "2. Implement missing NAS resilience features"
echo "3. Re-run tests to validate implementations"
echo "4. Use full E2E test suite once features are implemented"

echo
echo "✅ Simple test completed!" 