# MCP Sosreport Tools

Minimal MCP server for working with Fedora `sosreport` archives.

## What’s here
- `mcp_sosreport/server.py`: MCP server exposing `sos_extract`.
- `mcp_sosreport/test_client.py`: Standalone stdio client to test tool calls.
- `.codex/config.toml`: Local Codex MCP server config (relative paths).

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install mcp trio
python mcp_sosreport/server.py
```

## Tool

`sos_extract(tar_path: str, dest_dir: Optional[str]) -> dict`

Extracts a sosreport tarball under `/tmp` only. Defaults to
`/tmp/sosreport-extract-<timestamp>`.
