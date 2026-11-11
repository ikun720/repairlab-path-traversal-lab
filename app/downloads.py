"""Intentionally vulnerable fixture for RepairLab; never deploy this module."""

from pathlib import Path


def read_download(download_root: str | Path, filename: str) -> str:
    """Read UTF-8 text inside download_root; outside paths must raise ValueError.

    Missing files inside the root should still raise FileNotFoundError.
    """
    root = Path(download_root).resolve()
    target = (Path(download_root) / filename).resolve()
    if target != root and root not in target.parents:
        raise ValueError("resolved download path escapes the download root")
    return target.read_text(encoding="utf-8")
