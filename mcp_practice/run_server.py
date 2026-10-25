"""Run the exercise server after its selected transport has been implemented."""

import argparse

import uvicorn

from .exercises.level02_tools import build_calculator_server
from .exercises.level05_http import build_http_app


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local MCP calculator exercise.")
    parser.add_argument("--transport", choices=["stdio", "http"], default="stdio")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")
    server = build_calculator_server()
    if args.transport == "stdio":
        server.run(transport="stdio")
    else:
        uvicorn.run(build_http_app(server), host="127.0.0.1", port=args.port)


if __name__ == "__main__":
    main()
