from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route
def create_sse_server(mcp: FastMCP):
    transport = SseServerTransport("/messages/")
    async def handle_sse(request):
        async with transport.connect_sse(
            request.scope,
            request.receive,
            request._send
        ) as streams:
            await mcp._mcp_server.run(
                streams[0],
                streams[1],
                mcp._mcp_server.create_initialization_options()
            )
    routes = [
        Route("/sse/", endpoint=handle_sse, methods=["GET"]),
        Mount("/messages", app=transport.handle_post_message),  # <-- no trailing slash
    ]
    return Starlette(routes=routes)