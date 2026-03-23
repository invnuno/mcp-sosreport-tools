from __future__ import annotations

import tarfile
from datetime import timedelta
from pathlib import Path

import anyio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


WORKSPACE = Path(__file__).resolve().parents[1]
SERVER = WORKSPACE / "mcp_sosreport" / "server.py"
PYTHON = WORKSPACE / ".venv" / "bin" / "python"


def _make_sample_tarball() -> Path:
    src_dir = Path("/tmp/sosreport-sample-src")
    src_dir.mkdir(parents=True, exist_ok=True)
    (src_dir / "README.txt").write_text("sample sosreport content\n", encoding="utf-8")

    tar_path = Path("/tmp/sosreport-sample.tar.xz")
    with tarfile.open(tar_path, "w:xz") as tar:
        tar.add(src_dir, arcname="sosreport-sample")

    return tar_path


async def main() -> None:
    tar_path = _make_sample_tarball()

    server = StdioServerParameters(
        command=str(PYTHON),
        args=[str(SERVER)],
        cwd=str(WORKSPACE),
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            print("initializing...")
            await session.initialize()
            print("initialized")
            tools = await session.list_tools()
            print("tools:", [t.name for t in tools.tools])
            result = await session.call_tool(
                "sos_extract",
                {"tar_path": str(tar_path)},
                read_timeout_seconds=timedelta(seconds=10),
            )
            print("result:", result)


if __name__ == "__main__":
    anyio.run(main, backend="trio")
