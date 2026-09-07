# hoi4-owb-cheat-mod-house-always-wins

A dedicated cheat mod for the Hearts of Iron IV total conversion **Old World Blues**.

This repository is the source of truth. Deploy mirrors it into the local HOI4 mods folder as `house_always_wins`. Workshop gallery shots live in `screenshots/` and are not deployed.

```
pip install -r requirements.txt
python tools/resize_workshop_images.py
python tools/deploy_local_mod.py
```

`thumbnail.png` must be 512×512. Screenshots must be 1920×1080. See [CLAUDE.md](CLAUDE.md) for the local-mod layout and image rules.

## Licence

Code, scripts, and HOI4 script files are licensed under the MIT licence ([LICENSE](LICENSE)).

Creative assets (images, screenshots, `gfx/`, sound, and music) are licensed under Creative Commons CC0 1.0 Universal ([ASSETS_LICENCE.md](ASSETS_LICENCE.md)). If you add a new asset you are agreeing it will be available under this licence and that you have the legal right to do so.
