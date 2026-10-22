"""Generate unlock effects for OWB normal and unique techs."""

from __future__ import annotations

import re
from pathlib import Path

WORKSHOP = Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360")
OWB_ID = "2265420196"
OWB_TECH = WORKSHOP / OWB_ID / "common" / "technologies"
OUT = Path(__file__).resolve().parents[1] / "common" / "scripted_effects" / "haw_tech_research.txt"

NORMAL_FILES = [
    "tech_infantry.txt",
    "tech_industry.txt",
    "tech_naval.txt",
    "tech_engineering.txt",
    "tech_robotics.txt",
    "tech_support.txt",
    "tech_vehicle.txt",
    "tech_air.txt",
    "tech_creatures.txt",
    "tech_horse.txt",
    "tech_naval_modules.txt",
    "tech_tribal.txt",
    "tech_access.txt",
]

NESTED_KEYS = {
    "ai_will_do",
    "allow",
    "categories",
    "dependencies",
    "enable_building",
    "enable_equipments",
    "enable_subunits",
    "folder",
    "modifier",
    "on_research_complete",
    "path",
    "xor",
}
ID_RE = re.compile(r"^\t([a-zA-Z][a-zA-Z0-9_]*) = \{", re.M)
UNLOCK_ANY_RE = re.compile(r"[A-Za-z0-9_]+_unlock_tech")
TECH_LEVEL_RE = re.compile(r"([A-Za-z0-9_]+_tech_level_[A-Za-z0-9_]+)\s*=\s*1")
REAL_TECH_RE = re.compile(r"(research_cost|enable_equipments|enable_subunits)\s*=")
ENABLE_RE = re.compile(r"enable_(equipments|subunits)\s*=")
LEADS_RE = re.compile(r"leads_to_tech\s*=\s*([A-Za-z0-9_]+)")
DEP_RE = re.compile(r"([A-Za-z0-9_]+)\s*=\s*1")
SKIP_DEPS = {"blocked_tech", "blocked_unit_tech"}


def collect_tech_files() -> list[tuple[str, Path]]:
    files: dict[str, Path] = {}
    for filename in NORMAL_FILES:
        path = OWB_TECH / filename
        if path.is_file():
            files[filename] = path
    return list(files.items())


def extract_block(body: str, key: str) -> str | None:
    match = re.search(rf"{key}\s*=\s*\{{", body)
    if not match:
        return None
    start = match.end() - 1
    depth = 0
    for index, char in enumerate(body[start:], start):
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return body[start : index + 1]
    return None


def extract_techs(text: str) -> list[tuple[str, str]]:
    matches = list(ID_RE.finditer(text))
    techs: list[tuple[str, str]] = []
    for i, match in enumerate(matches):
        name = match.group(1)
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        techs.append((name, text[match.end() : end]))
    return techs


def is_blocked_flag(body: str) -> bool:
    deps = extract_block(body, "dependencies") or ""
    if "blocked_tech" in deps or "blocked_unit_tech" in deps:
        return True
    if re.search(r"allow\s*=\s*\{\s*always\s*=\s*no", body):
        return True
    return False


def is_real_tech(name: str, body: str) -> bool:
    if name in NESTED_KEYS or name.startswith("category_"):
        return False
    return bool(REAL_TECH_RE.search(body))


def tech_level_deps(body: str) -> list[str]:
    deps: list[str] = []
    seen: set[str] = set()
    block = extract_block(body, "dependencies")
    text = block or ""
    for dep in TECH_LEVEL_RE.findall(text):
        if dep not in seen:
            seen.add(dep)
            deps.append(dep)
    return deps


def named_deps(body: str) -> list[str]:
    block = extract_block(body, "dependencies") or ""
    deps: list[str] = []
    seen: set[str] = set()
    for dep in DEP_RE.findall(block):
        if dep in SKIP_DEPS or dep.endswith("_unlock_tech") or dep in seen:
            continue
        seen.add(dep)
        deps.append(dep)
    return deps


def allow_inner(body: str) -> str | None:
    block = extract_block(body, "allow")
    if not block:
        return None
    inner = block[1:-1].strip()
    if not inner or inner == "always = no":
        return None
    return inner


def extra_limits(body: str) -> list[str]:
    limits: list[str] = []
    branch = extract_block(body, "allow_branch")
    if not branch:
        return limits
    for raw in branch[1:-1].splitlines():
        stripped = raw.strip()
        if stripped.startswith("has_dlc"):
            limits.append(stripped)
    return limits


def is_unique_tech(name: str, body: str) -> bool:
    deps = extract_block(body, "dependencies") or ""
    allow = extract_block(body, "allow") or ""
    if UNLOCK_ANY_RE.search(deps) or UNLOCK_ANY_RE.search(allow):
        return True
    if "blocked_unit_tech" in deps:
        return True
    if "blocked_tech" in deps and ENABLE_RE.search(body):
        return True
    if re.search(r"allow\s*=\s*\{\s*always\s*=\s*no", body) and ENABLE_RE.search(body):
        return True
    return False


def is_flag_only_unlock(name: str, body: str) -> bool:
    return name.endswith("_unlock_tech") and not ENABLE_RE.search(body)


def write_grant(
    lines: list[str],
    tech: str,
    and_reqs: list[str],
    or_reqs: list[str],
    extra: list[str] | None,
    indent: str = "\t",
) -> None:
    lines.append(f"{indent}if = {{")
    lines.append(f"{indent}\tlimit = {{")
    lines.append(f"{indent}\t\tNOT = {{ has_tech = {tech} }}")
    seen: set[str] = set()
    for req in and_reqs:
        if req and req not in seen:
            seen.add(req)
            lines.append(f"{indent}\t\thas_tech = {req}")
    parents = [req for req in or_reqs if req and req not in seen]
    if len(parents) == 1:
        lines.append(f"{indent}\t\thas_tech = {parents[0]}")
    elif len(parents) > 1:
        lines.append(f"{indent}\t\tOR = {{")
        for req in parents:
            lines.append(f"{indent}\t\t\thas_tech = {req}")
        lines.append(f"{indent}\t\t}}")
    for raw in extra or []:
        if raw:
            lines.append(f"{indent}\t\t{raw}")
    lines.append(f"{indent}\t}}")
    lines.append(f"{indent}\tset_technology = {{")
    lines.append(f"{indent}\t\tpopup = no")
    lines.append(f"{indent}\t\t{tech} = 1")
    lines.append(f"{indent}\t}}")
    lines.append(f"{indent}}}")


def file_slug(filename: str) -> str:
    return filename.removesuffix(".txt").replace("-", "_")


def subtech_ids(body: str) -> list[str]:
    block = extract_block(body, "sub_technologies")
    if not block:
        return []
    return re.findall(r"[A-Za-z][A-Za-z0-9_]*", block[1:-1])


def main() -> None:
    unique: list[tuple[str, list[str], list[str], list[str]]] = []
    normal_by_file: dict[str, list[tuple[str, list[str], list[str], list[str]]]] = {}
    seen: set[str] = set()
    sources: list[str] = []
    path_parent: dict[str, list[str]] = {}
    sub_parent: dict[str, str] = {}
    collected: list[tuple[str, str, str]] = []

    for filename, path in collect_tech_files():
        sources.append(f"{path.parent.parent.parent.name}/{filename}")
        text = path.read_text(encoding="utf-8", errors="replace")
        for name, body in extract_techs(text):
            if name in NESTED_KEYS or name.startswith("category_"):
                continue
            for child in LEADS_RE.findall(body):
                path_parent.setdefault(child, [])
                if name not in path_parent[child]:
                    path_parent[child].append(name)
            for child in subtech_ids(body):
                sub_parent[child] = name
            if name in seen or not is_real_tech(name, body):
                continue
            seen.add(name)
            collected.append((filename, name, body))

    def extra_parents(name: str) -> list[str]:
        return list(path_parent.get(name, []))

    unique_names: set[str] = set()
    bodies: dict[str, str] = {}
    files_for: dict[str, str] = {}
    for filename, name, body in collected:
        bodies[name] = body
        files_for[name] = filename
        if is_unique_tech(name, body):
            unique_names.add(name)

    changed = True
    while changed:
        changed = False
        for name in bodies:
            if name in unique_names:
                continue
            parents = extra_parents(name)
            if name in sub_parent:
                parents.append(sub_parent[name])
            if any(parent in unique_names for parent in parents):
                unique_names.add(name)
                changed = True

    for filename, name, body in collected:
        if "_tech_level_" in name:
            continue
        if is_flag_only_unlock(name, body):
            continue
        extra = extra_limits(body)
        or_reqs = extra_parents(name)
        and_reqs = tech_level_deps(body)
        if name in sub_parent:
            and_reqs.append(sub_parent[name])
        if name in unique_names:
            unique.append((name, and_reqs + named_deps(body), or_reqs, extra))
            continue
        if is_blocked_flag(body):
            continue
        normal_by_file.setdefault(filename, []).append((name, and_reqs, or_reqs, extra))

    lines = [
        "# Generated by tools/_gen_tech_research.py from OWB tech files.",
        "# Available skips unique/blocked-unit techs. Path parents are OR. XOR branches are both granted.",
        "# Unique grants still need tech levels and a path parent, not company unlock flags.",
        f"# Sources: {', '.join(sources)}",
        "",
        "haw_research_unique_equipment_pass = {",
    ]
    for name, and_reqs, or_reqs, extra in unique:
        write_grant(lines, name, and_reqs, or_reqs, extra)
    lines.append("}")
    lines.append("")
    lines.append("haw_research_unique_equipment = {")
    for _ in range(5):
        lines.append("	haw_research_unique_equipment_pass = yes")
    lines.append("}")
    lines.append("")

    pass_names: list[str] = []
    for filename, techs in normal_by_file.items():
        effect = f"haw_research_normal_{file_slug(filename)}"
        pass_names.append(effect)
        lines.append(f"{effect} = {{")
        for name, and_reqs, or_reqs, extra in techs:
            write_grant(lines, name, and_reqs, or_reqs, extra)
        lines.append("}")
        lines.append("")

    lines.append("haw_unlock_available_normal_techs = {")
    for _ in range(5):
        for effect in pass_names:
            lines.append(f"	{effect} = yes")
    lines.append("}")
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    normal_count = sum(len(techs) for techs in normal_by_file.values())
    print(f"unique={len(unique)} normal={normal_count} files={len(pass_names)} -> {OUT}")
    print("sources:", ", ".join(sources))


if __name__ == "__main__":
    main()
