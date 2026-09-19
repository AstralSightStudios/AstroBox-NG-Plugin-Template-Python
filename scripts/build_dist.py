#!/usr/bin/env python3
"""把 Python 插件编译成 component 并放进 dist/。"""

import argparse
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", action="store_true", help="额外打一个 .abp 包")
    args = parser.parse_args()

    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    entry = manifest["entry"]

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    # componentize-py 需要能同时找到 wit 目录和入口模块
    cmd = [
        sys.executable,
        "-m",
        "componentize_py",
        "-d",
        str(ROOT / "wit"),
        "-w",
        "psys-world-v4",
        "componentize",
        "app",
        "-p",
        str(ROOT / "src"),
        "-o",
        str(DIST / entry),
    ]
    print(" ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        return result.returncode

    shutil.copy(ROOT / "manifest.json", DIST / "manifest.json")
    icon = ROOT / manifest.get("icon", "")
    if icon.is_file():
        shutil.copy(icon, DIST / icon.name)

    if args.package:
        abp = ROOT / f"{manifest['name'].replace(' ', '-')}-{manifest['version']}.abp"
        with zipfile.ZipFile(abp, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in DIST.rglob("*"):
                if path.is_file():
                    archive.write(path, path.relative_to(DIST))
        print(f"packaged -> {abp}")

    print(f"built -> {DIST / entry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
