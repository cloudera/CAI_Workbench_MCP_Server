# Contributing to CAI MCP Workbench Server

Thanks for contributing! Keep it simple.

## 🚀 Quick Start

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/CAI_Workbench_MCP_Server.git
cd CAI_Workbench_MCP_Server

# 2. Install
pip install uv
uv sync

# 3. Run tests
uv run pytest tests/ -v
```

---

## 🔄 Making Changes

### Branching Strategy

We use a simple two-branch strategy:
- **`main`** - Stable, production-ready (default branch)
- **`dev`** - Active development

**All contributions go to `dev` first, then released to `main`.**

### 1. Create Branch

```bash
git checkout dev
git pull origin dev
git checkout -b feature/your-feature
```

### 2. Make Changes

- Write code
- Add tests
- Run tests: `uv run pytest tests/ -v`

### 3. Commit

```bash
git add .
git commit -m "feat: your change"
git push origin feature/your-feature
```

**Commit format:** `type: description`

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests

### 4. Create PR

- **Target branch: `dev`** (not main!)
- Fill in description
- Wait for review

---

## ✅ Requirements

### All PRs Must:

- ✅ Pass all tests
- ✅ Have no security vulnerabilities
- ✅ Follow code style
- ✅ Include documentation updates if needed

### Code Standards

```python
# ✅ GOOD - Use requests library
import requests

headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get(url, headers=headers, timeout=30)

# ❌ BAD - Never use subprocess with API keys
import subprocess
subprocess.run(["curl", "-H", f"Bearer {api_key}", url])
```

**Key Rules:**
- Never expose API keys in subprocess/logs
- Always use `requests` library for HTTP
- Add timeout to all requests (30s)
- Use type hints
- Write docstrings

---

## 🧪 Testing

### Run Tests

```bash
# All tests
uv run pytest tests/ -v

# Just security tests
uv run pytest tests/test_all_functions.py::test_no_subprocess_vulnerabilities -v

# FastMCP test
uv run python tests/test_cai_mcp_client.py --quick
```

### Add Tests

Every new function needs tests in `tests/test_all_functions.py`:

```python
def test_my_function(mock_config):
    """Test my new function."""
    result = my_function(mock_config, {"param": "value"})
    assert isinstance(result, dict)
    assert "success" in result
```

---

## 🔒 Security

**Critical:** Never expose API keys!

- ❌ Don't log them
- ❌ Don't print them
- ❌ Don't pass as subprocess args
- ✅ Use HTTPS headers only

**Report vulnerabilities:** Email security@cloudera.com (not GitHub issues!)

---

## 📝 Documentation

Update docs if you:
- Add new function
- Change behavior
- Add dependencies

---

## 🎯 That's It!

Keep it simple:
1. Fork → Branch → Code → Test → PR
2. Target `dev` branch
3. Pass tests
4. Get approval
5. Merge!

Questions? Open a GitHub Discussion.
