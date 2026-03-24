# MCP Sosreport Tools

![MCP](https://img.shields.io/badge/MCP-Tools-2f6f8f)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776ab)

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
