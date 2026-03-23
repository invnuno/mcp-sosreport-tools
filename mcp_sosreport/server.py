from __future__ import annotations

import tarfile
import time
from pathlib import Path
from typing import Optional

import anyio
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("sosreport-tools", json_response=True, log_level="INFO")


def _ensure_safe_members(tar: tarfile.TarFile, dest_dir: Path) -> None:
    dest_root = dest_dir.resolve()
    for member in tar.getmembers():
        member_path = (dest_root / member.name).resolve()
        if not str(member_path).startswith(str(dest_root)):
            raise ValueError(f"Unsafe tar member path: {member.name}")


@mcp.tool()
def sos_extract(tar_path: str, dest_dir: Optional[str] = None) -> dict:
    """
    Extract a sosreport tarball to /tmp (or a provided destination).

    Args:
        tar_path: Path to the sosreport .tar.xz file.
        dest_dir: Optional destination directory within /tmp. Defaults to /tmp/sosreport-extract-<timestamp>.
    """
    tar_file = Path(tar_path).expanduser()
    if not tar_file.exists() or not tar_file.is_file():
        raise FileNotFoundError(f"Tarball not found: {tar_file}")

    tmp_root = Path("/tmp").resolve()
    if dest_dir:
        candidate = Path(dest_dir).expanduser().resolve()
        if candidate != tmp_root and tmp_root not in candidate.parents:
            raise ValueError("Destination must be within /tmp")
        out_dir = candidate
    else:
        out_dir = tmp_root / f"sosreport-extract-{int(time.time())}"

    out_dir.mkdir(parents=True, exist_ok=True)

    with tarfile.open(tar_file, mode="r:*") as tar:
        _ensure_safe_members(tar, out_dir)
        tar.extractall(out_dir)
        member_count = len(tar.getmembers())

    return {
        "tar_path": str(tar_file),
        "extracted_to": str(out_dir),
        "member_count": member_count,
    }


if __name__ == "__main__":
    anyio.run(mcp.run_stdio_async, backend="trio")
