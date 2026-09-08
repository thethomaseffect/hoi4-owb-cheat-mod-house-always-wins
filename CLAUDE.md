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

## What this mod aims to do

Right now there is a local mod called cheat mods combined along with my compat mod designed to make it work with old world blues. I want to make a mod tailored to old work blues specifically, that includes cheats for it's unique mechanics like trade nodes, caps, coring and the way armour penetration works. This should be based a lot on how cheat mods combined does it, but we want the following changes: 

We want absolutely minimal decisions. The cheat_event one should basically be the only option, but even then it should be incredibly rare that we need it (mostly for one-time options, like add caps and other currency, mark all disable trade nodes as enabled, core all available provinces for coring, reduce resistence to min and make compliance max (which enables coring))

What we want to focus on is adding cheat options to all the different political policies that are much better versions of what is there and having our own version of the cheats down the bottom. However, the way we want to implement it is that we want tons of new companies. We don't care about levels of cheat generally and focus on the "most" high version. There are exceptions where it has an impact on the game though.

Some options missing that could be cool
- Upgrade all available trade nodes to max level
- The add infrastructure, air bases and rader.
- Complete current salvaging mission
- justify wargoals for every province of every current neighbour
- increase navel dominance for all sea times to 100% (enabling navel invasions)
- unlock all AVAILABLE technology for your faction. old world blues has tech levels up to sophisticated, and some techs are locked for certain factions. There are also whole trees that cannot be used (NCR, for example, ever gets the animal training options). This skips needing to research everything. we shoudl also have an option to unlock all the sophistigated tech etc. even if it would usually be gated, maybe best way to to change our countryso it allows everything, then the earlier feature would do this too.
- When we add cheat staff, such as advisors, they should always be themed after mr.handy from fallout new vegas. generate new robots with silly names, this way the cheat options are clearly distinct from the real options(and very useful, solve the annoying issue for many nations where you get warned you haveno navel commander when none are available)
- A special forces troop option called servebots. These have OP stats in every category and are very cheap to maintain, and because they are special forces they can participate in navel invasions and paratrooping. They should use very basic equipment so that they don't have issues when created before tech is researched. We should also have a cheat support option that does everything
- An option to unlock all unique technologies. These are usually locked behind events etc. but it might be fun to have the option
- as with technologies, unlock all perks and doctrines. grand doctrines might not be available, but the mod should accomadate if they are.
- Add resources to owned states for stuff we actually use like water and electricity
- National spirits can get clogged up with cheat options with cheat mods combined. Therefore, if possible we should keep all the modifiers to the custom companies and advisors we mentioned earlier.
- If we need pictures for the servebots we use mr. handy or some variation. The cheat commanders should be the same.
- Ditch options that add traits to existing commanders, if people want cheat traits they should just use the cheat options. All cheat commanders for army, navy etc. should have max level and lots of medals
- If possible, an option to teleport all exiled troops to your capital.
- Option to increase influence with all available trader factions to 1000
- option to add more research slots. This shouldn't conflict with any DLCs doing the same, or focuses that do it, so the max should never exceed what the game allows
- option to reduce all puppet autonomy so they can be reduced to next levels if desired
- option to make preparing and executing espionage plans instant,also adding cheat agents.
- add an experimental facility that is a cheat option for thestate it is built in
(all features that reply on DLC should be abscent if DLC is not enabled, meaning that the mod can be used with no DLC, and the features are all optional)
- add 10k stockpile for all unlocked equipment
- unlock one more operative slot (if possible)
- set stability to 100 and war support to 100, set world tension to either 100 or 0

## How we implement this

CMC dumps dozens of decisions and national spirits. This mod does not.

| Surface | What goes there |
| --- | --- |
| OWB policy pickers | One extra "House" option in Army Training, Economy, Engineering, Construction, Vehicle Restoration |
| Bottom of politics | Three new rows: House Policies, Handy Companies, Handy Staff (Mr Handy names, max tier only) |
| One decision | `Open the House console` → event menus for one-shots |

OWB scripted effects we call: `add_caps`, `hard_enable_all_nodes`, `add_core_effect`, `organization_add_influence` (clamped at **300**, not 1000), `select_scavenging_reward`. Armour pen is boosted on Handy Hulls via `ap_attack`. Naval dominance is fleet-based in OWB; the navy policy plus Handy commanders is the first pass. Instant research of every item in a tree is still TODO (tech **levels** and unique unlock flags are in).

Servebots and Servebot Support use `infantry_equipment` only and start unlocked.

## Debug logs (when the game crashes)

Logs are written automatically. `-debug` on the Steam launch options makes them complete.

`C:/Users/[replace with username]/Documents/Paradox Interactive/Hearts of Iron IV/logs/`

That folder is overwritten every launch. CTD copies go to `.../Hearts of Iron IV/crashes/hoi4_YYYYMMDD_HHMMSS/`.

When reporting a crash, send:

1. `logs/error.log` — script problems
2. `logs/exceptions.log` — CTD stack
3. `logs/setup.log` — last thing that finished loading
4. The matching `crashes/hoi4_*` folder if it exists

Optional: add `-crash_data_log` only while reproducing a CTD. It writes `LastRead:` into `meta.yml` in the documents folder and is slow.