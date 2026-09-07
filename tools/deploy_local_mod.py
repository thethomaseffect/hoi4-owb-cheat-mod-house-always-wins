"""Mirror this git repo into the single local HOI4 mod folder."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

MOD_SLUG = "house_always_wins"
DOCUMENTS_GAME = Path("Paradox Interactive") / "Hearts of Iron IV"

EXCLUDE_DIR_NAMES = {
    ".git",
    ".cursor",
    ".github",
    ".venv",
    "__pycache__",
    "tools",
}
EXCLUDE_ROOT_FILES = {
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "CLAUDE.md",
    "LICENSE",
    "README.md",
}


def hoi4_documents() -> Path:
    home = Path.home()
    candidates = [
        home / "Documents",
        home / "OneDrive" / "Documents",
        Path(os.environ.get("USERPROFILE", str(home))) / "Documents",
    ]
    for candidate in candidates:
        documents_game = candidate / DOCUMENTS_GAME
        if documents_game.is_dir():
            return documents_game
    return home / "Documents" / DOCUMENTS_GAME


def parse_remote_file_id(text: str) -> str | None:
    match = re.search(r'remote_file_id\s*=\s*"([^"]+)"', text)
    return match.group(1) if match else None


def existing_remote_file_id(mods_dir: Path, slug: str) -> str | None:
    for path in (mods_dir / slug / "descriptor.mod", mods_dir / f"{slug}.mod"):
        if path.is_file():
            remote_id = parse_remote_file_id(path.read_text(encoding="utf-8"))
            if remote_id:
                return remote_id
    return None


def with_remote_file_id(text: str, remote_id: str | None) -> str:
    body = text.replace("\r\n", "\n")
    if not body.endswith("\n"):
        body += "\n"
    body = re.sub(r'remote_file_id\s*=\s*"[^"]+"\n?', "", body)
    if remote_id:
        body += f'remote_file_id="{remote_id}"\n'
    return body


def with_path(text: str, path: str) -> str:
    body = text.replace("\r\n", "\n")
    if not body.endswith("\n"):
        body += "\n"
    body = re.sub(r'^path\s*=\s*"[^"]+"\n?', "", body, flags=re.MULTILINE)
    lines = body.splitlines(keepends=True)
    insert_at = len(lines)
    for index, line in enumerate(lines):
        if line.startswith("remote_file_id"):
            insert_at = index
            break
    lines.insert(insert_at, f'path="{path}"\n')
    return "".join(lines)


def should_copy(relative: Path) -> bool:
    if relative.parts and relative.parts[0] in EXCLUDE_DIR_NAMES:
        return False
    if len(relative.parts) == 1 and relative.name in EXCLUDE_ROOT_FILES:
        return False
    return True


def mirror_repo(repo: Path, dest: Path) -> list[Path]:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    copied: list[Path] = []
    for source in repo.rglob("*"):
        if not source.is_file():
            continue
        relative = source.relative_to(repo)
        if not should_copy(relative):
            continue
        target = dest / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(relative)
    return copied


def deploy(repo: Path, mods_dir: Path, slug: str) -> Path:
    dest = mods_dir / slug
    remote_id = existing_remote_file_id(mods_dir, slug)
    copied = mirror_repo(repo, dest)

    descriptor_src = repo / "descriptor.mod"
    if not descriptor_src.is_file():
        raise FileNotFoundError(f"Missing {descriptor_src}")
    descriptor_text = with_remote_file_id(
        descriptor_src.read_text(encoding="utf-8"), remote_id
    )
    (dest / "descriptor.mod").write_text(descriptor_text, encoding="utf-8")

    pointer = with_path(descriptor_text, dest.as_posix())
    (mods_dir / f"{slug}.mod").write_text(pointer, encoding="utf-8")

    print(f"Updated {dest} ({len(copied)} files)")
    print(f"Updated {mods_dir / f'{slug}.mod'}")
    return dest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mods-directory",
        type=Path,
        help="Override Documents/.../Hearts of Iron IV/mod",
    )
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    mods_dir = args.mods_directory or (hoi4_documents() / "mod")
    mods_dir.mkdir(parents=True, exist_ok=True)
    deploy(repo, mods_dir, MOD_SLUG)
    return 0


if __name__ == "__main__":
    sys.exit(main())
