# Changelog

All notable changes to the CML MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite (`test_all_functions.py`) with 11 unit tests
- FastMCP integration tests (`test_cml_mcp_client.py`)
- Security vulnerability detection tests
- Comprehensive test documentation in `tests/README.md`

### Changed
- **SECURITY**: Replaced all `subprocess.run` calls with secure `requests` library (46 files)
- API keys now transmitted securely in HTTPS headers instead of process arguments
- Updated all function error handling to use `requests.RequestException`
- Improved timeout handling (30s timeout on all API calls)

### Fixed
- **CRITICAL**: API key exposure vulnerability in process list (CVE-pending)
- Error messages now properly report HTTP status codes
- JSON parsing errors now provide better debugging information

### Security
- Eliminated subprocess-based API calls that exposed credentials
- All HTTP requests now use proper header-based authentication
- Added comprehensive security testing in CI/CD pipeline

---

## [1.0.0] - 2025-10-22

### Added
- Initial public release
- Apache 2.0 license
- NOTICE.txt with third-party attributions
- 47+ MCP tools for Cloudera AI operations
- Support for:
  - Project management
  - Job creation and management
  - Model building and deployment
  - Experiment tracking
  - File operations
  - Application management
- FastMCP-based HTTP and stdio servers
- OAuth 2.1 support
- Comprehensive README documentation

### Changed
- Migrated from private to public repository
- Updated all repository URLs to `github.com/cloudera/CML_MCP_Server`
- Updated license from MIT to Apache 2.0
- Added legal notices for third-party dependencies

---

## Types of Changes

- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` for vulnerability fixes

---

## Release Links

- [Unreleased](https://github.com/cloudera/CML_MCP_Server/compare/v1.0.0...HEAD)
- [1.0.0](https://github.com/cloudera/CML_MCP_Server/releases/tag/v1.0.0)
