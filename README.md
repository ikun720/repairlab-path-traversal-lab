# RepairLab path traversal lab

Intentionally vulnerable Python file-download example for testing RepairLab.
This is a local test fixture, not a deployable service. All data is generated
inside a temporary directory; no real credentials or private files are included.

## Bug and acceptance contract

`app/downloads.py` joins a user-supplied filename to a download root without
checking the resolved boundary. A caller can read outside that directory using
`../outside.txt`, an absolute path, a similarly named sibling directory, or a
symbolic link. Outside paths must raise `ValueError`. Valid and nested files
must remain readable; missing inside files must raise `FileNotFoundError`.

Only the Python standard library is used. Requires Python 3.11 or newer.

```sh
python -B -m unittest discover -s tests -v
```

The initial version deliberately fails 4 of 7 tests on Linux. On Windows the
symlink case may be skipped if symlink creation is not permitted. After a
correct repair, all available tests must pass without editing the tests.

## Verify with RepairLab

1. Paste this repository's GitHub home URL into a RepairLab conversation with:
   `请诊断文件下载的路径穿越问题，不要修改代码。`
2. Check that the diagnostic identifies `app/downloads.py` and the failed tests.
3. Send: `按刚才的诊断修复它。只修改 app/downloads.py，保留原始测试。`
4. Check the patch, passing tests, unchanged test files, and parent task link.
5. Connect a GitHub fine-grained token scoped to this repository with
   Contents: Read and write in the RepairLab GitHub connection dialog.
6. Preview and explicitly confirm publication to a new `repairlab/<run_id>`
   branch. Inspect that branch on GitHub; the default branch must remain buggy.

RepairLab's built-in AST scanner currently detects dynamic SQL only. For this
non-SQL example, the failing original tests are the reproduction and acceptance
evidence. Zero scanner findings do not mean a complete security audit.
