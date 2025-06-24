# Plane Backup System Test Suite

This directory contains comprehensive tests for the Plane backup and deployment system.

## Test Structure

### E2E Tests (`e2e/`)
End-to-end tests that verify the complete backup and deployment workflows:
- `test-backup-basic.sh` - Tests basic backup functionality
- `test-backup-nas-dependency.sh` - Tests NAS dependency issues (demonstrates need for resilience)
- `test-deployment-flow.sh` - Tests complete deployment workflow
- `test-recovery-procedures.sh` - Tests backup restoration procedures

### Unit Tests (`unit/`)
Individual component tests:
- `test-backup-script.sh` - Unit tests for backup script components
- `test-restore-script.sh` - Unit tests for restore script components
- `test-configuration.sh` - Tests configuration validation

### Integration Tests (`integration/`)
Tests that verify component interactions:
- `test-docker-backup-integration.sh` - Tests Docker container backup integration
- `test-nas-storage-integration.sh` - Tests NAS storage integration

### Test Utilities (`utils/`)
Shared test utilities and helpers:
- `test-helpers.sh` - Common test functions
- `mock-nas.sh` - NAS simulation utilities
- `docker-test-helpers.sh` - Docker testing utilities

## Running Tests

### All Tests
```bash
./run-all-tests.sh
```

### Specific Test Categories
```bash
./run-e2e-tests.sh
./run-unit-tests.sh
./run-integration-tests.sh
```

### Individual Tests
```bash
cd e2e && ./test-backup-basic.sh
```

## Test Philosophy

### Current State Testing
Tests verify that existing functionality works correctly and identify limitations that require new features.

### Failing Tests for Missing Features
Some tests are designed to fail initially, demonstrating the need for features like:
- NAS offline handling
- Backup sync capabilities
- Monitoring and alerting
- Advanced recovery procedures

### Future-Resilient Testing
Tests are designed to be resilient to future changes by:
- Testing behavior rather than implementation details
- Using configurable test parameters
- Focusing on user-visible outcomes
- Abstracting environment-specific details

## Test Status

- ✅ **Passing**: Tests that verify current working functionality
- ❌ **Failing (Expected)**: Tests that demonstrate missing features
- ⚠️ **Skipped**: Tests that require specific environment setup
- 🔄 **Flaky**: Tests that may pass/fail depending on environment

## Contributing

When adding new features:
1. Write failing tests first that demonstrate the need
2. Implement the feature
3. Ensure tests pass
4. Add integration tests for the new feature
5. Update this documentation 