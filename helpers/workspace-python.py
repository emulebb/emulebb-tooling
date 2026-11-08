#!/usr/bin/env python3
"""Use the workspace-owned interpreter without changing the operator's PATH."""
from __future__ import annotations

import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True


def main() -> int:
    """Bootstrap interpreter selection only; forward script args and Git stdin."""
    root_value = os.environ.get("EMULEBB_WORKSPACE_ROOT", "")
    if not root_value or not Path(root_value).is_absolute():
        raise RuntimeError("EMULEBB_WORKSPACE_ROOT must be inherited")
    owner = Path(root_value) / "repos/emulebb-build"
    if not (owner / "emule_workspace/python_runtime.py").is_file():
        raise RuntimeError("The canonical workspace Python owner is missing")
    if not sys.argv[1:]:
        raise RuntimeError("A workspace script is required")
    sys.path.insert(0, str(owner))
    from emule_workspace.python_runtime import run_script
    return run_script(sys.argv[1:])


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError) as error:
        print(f"Workspace Python: {error}", file=sys.stderr)
        raise SystemExit(1) from error
