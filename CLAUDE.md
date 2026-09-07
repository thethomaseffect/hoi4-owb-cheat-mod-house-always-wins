# House Always Wins (HOI4 / Old World Blues)

This git repo is the source of truth. Hearts of Iron IV does not load the repo itself. Deploy mirrors the HOI4 files here into **one** local mod and updates that same local mod on every later deploy.

## How HOI4 local mods work

The launcher only reads `.mod` files in:

`C:/Users/[replace with username]/Documents/Paradox Interactive/Hearts of Iron IV/mod`

A playable local mod is two things:

```
Documents/Paradox Interactive/Hearts of Iron IV/mod/
  house_always_wins.mod
  house_always_wins/
    descriptor.mod
    thumbnail.png
    common/ ...
```

- `descriptor.mod` (in git and in the local folder) has **no** `path`.
- `house_always_wins.mod` is the launcher pointer: same metadata plus `path=` pointing at the local folder, using **forward slashes**.
- `dependencies` are exact display names (`"Old World Blues"`), not folder names or Steam IDs.
- `replace_path="some/folder"` wipes that folder from earlier mods in the playset. Do not set it unless the wipe is intended.
- If the Documents copy already has `remote_file_id`, deploy keeps it so a Workshop upload stays the same item.

Workshop content lives under `Steam/steamapps/workshop/content/394360`. Vanilla is `Steam/steamapps/common/Hearts of Iron IV`. Playsets and enable-state live in `launcher-v2.sqlite` and `dlc_load.json`.

## Develop here, deploy there

1. Edit only this repo (`descriptor.mod`, `common/`, `events/`, `interface/`, and so on).
2. Do not hand-edit the Documents copy. It is a generated mirror.
3. Deploy to update the existing `house_always_wins` local mod (never a new slug per change):

```
python tools/deploy_local_mod.py
```

Deploy:

- Replaces `.../mod/house_always_wins/`
- Writes `.../mod/house_always_wins.mod` with `path` set
- Skips `.git`, `.cursor`, `tools/`, `screenshots/`, `README.md`, `LICENSE`, `ASSETS_LICENCE.md`, and `CLAUDE.md`
- Copies `descriptor.mod`, `thumbnail.png`, and every HOI4 content folder

Override the destination with `--mods-directory` if needed.

## Thumbnails and Workshop screenshots

| Use | Path | Size | Notes |
| --- | --- | --- | --- |
| Launcher / Workshop preview | `thumbnail.png` (repo root, deployed) | **512×512** PNG, 1:1, under 1 MB | HOI4 rejects bad thumbnails silently. Paradox Mods also caps 1 MB. |
| Workshop gallery | `screenshots/` (not deployed) | **1920×1080**, 16:9, under 1 MB | Drop source shots here. Do not put them in the mod folder. |

After adding or replacing images:

```
python tools/resize_workshop_images.py
```

The script center-crops to the target aspect, scales with LANCZOS, and recompresses until the file is under 1 MB. `thumbnail.png` stays PNG. Screenshot format is kept (PNG or JPG).

## This mod

| Field | Value |
| --- | --- |
| Display name | House Always Wins |
| Local slug | `house_always_wins` |
| Depends on | Old World Blues |
| Tags | Gameplay, Utilities |

After the first deploy, enable **House Always Wins** in the launcher playset, below Old World Blues.

## Licence

- **MIT** ([LICENSE](LICENSE)): code, tools, and HOI4 script files (`common/`, `events/`, `interface/` scripts, and so on).
- **CC0 1.0** ([ASSETS_LICENCE.md](ASSETS_LICENCE.md)): creative assets — `thumbnail.png`, `screenshots/`, `gfx/`, sound, and music. Adding an asset means it is released under CC0 and that the contributor has the right to do so.
