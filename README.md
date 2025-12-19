# MCP Quadrant - Document & Location Search

A Model Context Protocol (MCP) server providing coordinate conversion tools and document search with Qdrant vector database, featuring quadrant-based spatial search and filtering.

## 🚀 Features

- **Document Storage**: Store and retrieve document chunks with optional geolocation
- **Quadrant-Based Search**: Search within specific geographic quadrants (NE, NW, SE, SW)
- **Location-Based Search**: Find documents near specific coordinates
- **Hybrid Search**: Combine semantic search with geospatial filtering
- **Fast Vector Search**: Powered by Qdrant's efficient vector similarity search

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
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

```

The server will start on `http://127.0.0.1:8000/sse/ `

# To run the MCP inspector

> npx @modelcontextprotocol/inspector http://127.0.0.1:8000/sse/ 
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

### Coordinate Conversion
1. **tlc_to_address_tool** - Convert TLC codes to addresses
2. **address_to_tlc_tool** - Convert addresses to TLC codes
3. **address_to_plasma_tool** - Convert addresses to Plasma format
4. **plasma_to_address_tool** - Convert Plasma coordinates to addresses

### Document Search & Storage
5. **store_document_chunks** - Store document chunks with optional geolocation
6. **search_documents_by_quadrant** - Search within a specific geographic quadrant
7. **search_documents_near_location** - Search near specific coordinates
8. **search_documents_by_filename** - Search documents by filename

