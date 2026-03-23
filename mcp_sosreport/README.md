# MCP Sosreport Tools

Minimal MCP server exposing tools for working with sosreport archives.

## Run

Using `uv`:

```bash
uv run --with mcp python mcp_sosreport/server.py
```

Using `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install mcp trio
python mcp_sosreport/server.py
```

Note: The server runs with the AnyIO Trio backend; install `trio` in the same environment.

## Tool

`sos_extract(tar_path: str, dest_dir: Optional[str]) -> dict`

Extracts a sosreport tarball to `/tmp/sosreport-extract-<timestamp>` by default. If `dest_dir` is provided, it **must** be within `/tmp`.

## Test With Codex (OpenAI)

1. Ensure you have a Codex config file at `~/.codex/config.toml` or a project override at `.codex/config.toml`. Codex only loads project configs for trusted projects. citeturn4view0
2. Configure the MCP server entry using the `mcp_servers.<id>.command`, `args`, and optional `cwd` keys. citeturn1view0
3. Run Codex and call the tool:

Example `.codex/config.toml`:

```toml
[mcp_servers.sosreport]
command = ".venv/bin/python"
args = ["mcp_sosreport/server.py"]
cwd = "."
enabled = true
enabled_tools = ["sos_extract"]
```

Then prompt Codex with something like:

```
Extract this sosreport tarball: /path/to/sosreport-*.tar.xz
```
