# MCP Address Conversion - Coordinate Conversion Server

A Model Context Protocol (MCP) server providing coordinate conversion tools between TLC, Plasma, and human-readable addresses.

## 🚀 Quick Start with UV

### 1. Install UV (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### 2. Setup the Project

```bash
# Navigate to your project directory
cd MCP_ADDRESS

# Create a virtual environment and install dependencies
uv venv
uv pip install -e .
```

### 3. Run the MCP Server

```bash
# Activate the virtual environment (optional, uv can run without activation)
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Run
uv run python main.py

# OR run directly without activating venv
uv run main.py
```

The server will start on `http://0.0.0.0:8000`

# To run the MCP inspector

> npx @modelcontextprotocol/inspector http://0.0.0.0:8000/sse

## 🔧 Configure Claude Desktop

Add this to your Claude Desktop config file:

**Location:**

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Configuration:**

```json
{
  "mcpServers": {
    "quadrant": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/MCP_ADDRESS",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

**Replace `/absolute/path/to/MCP_QUADRANT`** with your actual project path.

## 📦 Available Tools

1. **tlc_to_address_tool** - Convert TLC codes to addresses
2. **address_to_tlc_tool** - Convert addresses to TLC codes
3. **address_to_plasma_tool** - Convert addresses to Plasma format
4. **plasma_to_address_tool** - Convert Plasma coordinates to addresses

## 🛠️ Development Commands

```bash
# Install dependencies
uv pip install -e .

# Install with geocoding support
uv pip install -e ".[geocoding]"

# Update dependencies
uv pip install --upgrade mcp fastmcp uvicorn starlette

# Run tests (after adding tests)
uv run pytest

# Format code (if you add ruff/black)
uv run ruff format .
```

## 📝 Project Structure

```
MCP_QUADRANT/
├── tools/
│   ├── __init__.py
│   ├── address_plasma.py # Address → Plasma conversion
│   ├── address_TLC.py    # Address → TLC conversion
│   ├── plasma_address.py # Plasma → Address conversion
│   └── TLC_address.py    # TLC → Address conversion
├── server.py             # SSE server setup
├── main.py               # Main MCP server
├── requirements.txt      # Pip requirements (backup)
├── pyproject.toml        # UV/Python project config
└── README.md             # This file
```

## 🔄 Next Steps

1. Implement your actual conversion algorithms in each module
2. Add real geocoding logic if needed
3. Test each tool independently
4. Restart Claude Desktop to load the MCP server

## 📚 Resources

- [UV Documentation](https://docs.astral.sh/uv/)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP Guide](https://github.com/jlowin/fastmcp)

## 🐛 Troubleshooting

**Server won't start:**

- Check that all dependencies are installed: `uv pip list`
- Verify Python version: `uv run python --version` (should be 3.10+)
- Check for syntax errors in your conversion modules

**Claude Desktop doesn't see the tools:**

- Restart Claude Desktop completely
- Check the path in `claude_desktop_config.json` is absolute
- View Claude Desktop logs for errors

**Import errors:**

- Make sure you're in the project directory
- Run `uv pip install -e .` to install in editable mode
