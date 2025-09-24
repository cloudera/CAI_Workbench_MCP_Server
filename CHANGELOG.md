# Changelog

## Latest Cleanup and Documentation Update

### Changed
- **Removed `server.py`**: Eliminated the legacy compatibility file entirely
- **Updated Claude Desktop config**: Now uses `cml_mcp_server.stdio_server` directly
- **Removed legacy entry point**: `cml-mcp-server` command no longer exists
- **Cleaner documentation**: Removed all references to the old server.py approach
- **Completed `stdio_server.py`**: Added all 47 tool definitions (was only 7)
- **Fixed imports**: Added try/except for package vs direct execution

### Benefits
- Cleaner codebase with no legacy code
- Direct usage of appropriate server files (stdio_server.py or http_server.py)
- Clear separation of concerns
- Both server files are now complete and self-contained

## Major Refactoring (Previous Update)

### Code Organization
- **Split server implementations**: Separated STDIO and HTTP into distinct files
  - `stdio_server.py` - Clean STDIO-only implementation
  - `http_server.py` - HTTP server with all endpoints
- **Fixed HTTP issues**: Working `/mcp-api` endpoint with proper initialization
- **Simplified imports**: Clear separation of concerns

### Server Improvements
- Added `initialize` method to `/mcp-api` endpoint (fixes 404 errors)
- All 47 tools now accessible via HTTP with working implementation
- HTTP transport clearly marked as "development only" without authentication
- Debug endpoints: `/test`, `/debug/tools`, `/debug/call` for easy testing

### Entry Points
- `cml-mcp-stdio` - Runs stdio_server.py
- `cml-mcp-http` - Runs http_server.py

### Documentation
- Updated README with new server structure
- Clear examples for both STDIO and HTTP modes
- Removed OAuth sections (future feature)
- Added troubleshooting section

### Key Fixes
- Fixed "Tool not callable" errors by using direct function mappings
- Fixed 404 errors by adding proper initialize method
- Maintained backward compatibility while improving structure

### Usage
```bash
# STDIO (recommended)
uv run -m cml_mcp_server.stdio_server

# HTTP (development)
uv run -m cml_mcp_server.http_server
```
