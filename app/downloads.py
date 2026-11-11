"""Intentionally vulnerable fixture for RepairLab; never deploy this module."""

from pathlib import Path


def read_download(download_root: str | Path, filename: str) -> str:
    """Read UTF-8 text inside download_root; outside paths must raise ValueError.

    Missing files inside the root should still raise FileNotFoundError.
    """
    target = Path(download_root) / filename
    return target.read_text(encoding="utf-8")
