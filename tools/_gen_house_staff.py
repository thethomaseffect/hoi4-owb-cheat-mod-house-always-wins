"""Inline Handy staff in history and keep mid-save spawn in sync.

Names are omitted so HOI4 rolls each country's namelist, same as Recruit.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "history" / "general" / "haw_house_staff.txt"
EFFECTS = ROOT / "common" / "scripted_effects" / "haw_staff_spawn.txt"

CIVILIAN = """\
		portraits = {
			civilian = { small = "GFX_idea_haw_handy" }
		}"""

ARMY_SMALL = """\
		portraits = {
			army = { small = "GFX_idea_haw_handy" }
		}"""

ARMY_LARGE = """\
		portraits = {
			army = {
				large = "GFX_portrait_haw_servebot"
				small = "GFX_idea_haw_handy"
			}
		}"""

ARMY_NAVY = """\
		portraits = {
			army = {
				large = "GFX_portrait_haw_servebot"
				small = "GFX_idea_haw_handy"
			}
			navy = {
				large = "GFX_portrait_haw_servebot"
				small = "GFX_idea_haw_handy"
			}
		}"""

# extra=True characters fill More Advisor Slots (6 eco, 6 culture, 3 HC, 2 theorist).
STAFF: list[dict[str, str | bool]] = [
    {
        "token": "haw_eco_ledger",
        "idea": "haw_eco_ledger",
        "slot": "economic_advisor",
        "ledger": "civilian",
        "portraits": CIVILIAN,
        "body": """\
			modifier = {
				consumer_goods_factor = -0.5
				industrial_capacity_factory = 2.0
				industrial_capacity_dockyard = 2.0
				caps_flat_income_modifier = 250
			}""",
    },
    {
        "token": "haw_eco_dividend",
        "idea": "haw_eco_dividend",
        "slot": "economic_advisor",
        "ledger": "civilian",
        "portraits": CIVILIAN,
        "body": """\
			modifier = {
				production_speed_buildings_factor = 2.0
				local_resources_factor = 2.0
				industry_repair_factor = 2.0
				caps_income_modifier = 2.0
				caps_country_trade_modifier = 2.0
			}""",
    },
    {
        "token": "haw_eco_payroll",
        "idea": "haw_eco_payroll",
        "slot": "economic_advisor",
        "ledger": "civilian",
        "portraits": CIVILIAN,
        "body": """\
			modifier = {
				political_power_gain = 2.0
				research_speed_factor = 2.0
				stability_factor = 0.5
				caps_expense_modifier = -0.9
			}""",
    },
    {
        "token": "haw_eco_inventory",
        "idea": "haw_eco_inventory",
        "slot": "economic_advisor",
        "ledger": "civilian",
        "portraits": CIVILIAN,
        "extra": True,
        "body": """\
			modifier = {
				supply_consumption_factor = -0.9
				out_of_supply_factor = -0.9
				no_supply_grace = 240
				attrition = -0.5
			}""",
    },
    {
        "token": "haw_eco_tariff",
        "idea": "haw_eco_tariff",
        "slot": "economic_advisor",
        "ledger": "civilian",
        "portraits": CIVILIAN,
        "extra": True,
        "body": """\
			modifier = {
				trade_opinion_factor = 2.0
				min_export = -0.3
				extra_trade_to_target_factor = 1.0
				caps_country_trade_modifier = 2.0
			}""",
    },
    {
        "token": "haw_eco_vault",
        "idea": "haw_eco_vault",
        "slot": "economic_advisor",
        "ledger": "civilian",
        "portraits": CIVILIAN,
        "extra": True,
        "body": """\
			modifier = {
				local_resources_factor = 2.0
				fuel_gain_factor = 2.0
				encryption = 2
			}""",
    },
    {
        "token": "haw_culture_etiquette",
        "idea": "haw_culture_etiquette",
        "slot": "cultural_advisor",
        "ledger": "civilian",
        "portraits": CIVILIAN,
        "body": """\
			modifier = {
				stability_factor = 1.0
				war_support_factor = 1.0
				political_power_gain = 2.0
			}""",
    },
    {
        "token": "haw_culture_broadcast",
        "idea": "haw_culture_broadcast",
        "slot": "cultural_advisor",
        "ledger": "civilian",
        "portraits": CIVILIAN,
        "body": """\
			modifier = {
				compliance_growth = 1.0
				resistance_growth = -1.0
				resistance_target = -0.5
			}""",
    },
    {
        "token": "haw_culture_pageant",
        "idea": "haw_culture_pageant",
        "slot": "cultural_advisor",
        "ledger": "civilian",
        "portraits": CIVILIAN,
        "body": """\
			modifier = {
				research_speed_factor = 1.0
				drift_defence_factor = 2.0
				improve_relations_maintain_cost_factor = -0.9
			}""",
    },
    {
        "token": "haw_culture_census",
        "idea": "haw_culture_census",
        "slot": "cultural_advisor",
        "ledger": "civilian",
        "portraits": CIVILIAN,
        "extra": True,
        "body": """\
			modifier = {
				monthly_population = 1.0
				conscription = 0.15
				non_core_manpower = 0.5
				weekly_manpower = 500
			}""",
    },
    {
        "token": "haw_culture_gala",
        "idea": "haw_culture_gala",
        "slot": "cultural_advisor",
        "ledger": "civilian",
        "portraits": CIVILIAN,
        "extra": True,
        "body": """\
			modifier = {
				improve_relations_maintain_cost_factor = -0.9
				opinion_gain_monthly_factor = 2.0
				justify_war_goal_time = -0.9
				guarantee_tension = -1.0
			}""",
    },
    {
        "token": "haw_culture_archive",
        "idea": "haw_culture_archive",
        "slot": "cultural_advisor",
        "ledger": "civilian",
        "portraits": CIVILIAN,
        "extra": True,
        "body": """\
			modifier = {
				decryption = 2
				encryption = 2
				research_speed_factor = 0.5
				drift_defence_factor = 1.0
			}""",
    },
    {
        "token": "haw_centurion_coffee",
        "idea": "haw_char_centurion_coffee",
        "slot": "army_chief",
        "ledger": "army",
        "portraits": ARMY_LARGE,
        "body": """\
			traits = { haw_army_chief }""",
    },
    {
        "token": "haw_admiral_suds",
        "idea": "haw_char_admiral_suds",
        "slot": "navy_chief",
        "ledger": "navy",
        "portraits": ARMY_NAVY,
        "body": """\
			traits = { haw_navy_chief }""",
    },
    {
        "token": "haw_marshall_mops",
        "idea": "haw_char_marshall_mops",
        "slot": "air_chief",
        "ledger": "air",
        "portraits": ARMY_LARGE,
        "body": """\
			traits = { haw_air_chief }""",
    },
    {
        "token": "haw_major_brush",
        "idea": "haw_major_brush",
        "slot": "high_command",
        "ledger": "army",
        "portraits": ARMY_SMALL,
        "body": """\
			modifier = {
				army_attack_factor = 2.0
				army_org_factor = 2.0
				planning_speed = 2.0
			}""",
    },
    {
        "token": "haw_colonel_sponge",
        "idea": "haw_colonel_sponge",
        "slot": "high_command",
        "ledger": "army",
        "portraits": ARMY_SMALL,
        "body": """\
			modifier = {
				army_defence_factor = 2.0
				max_dig_in = 50
				attrition = -0.9
			}""",
    },
    {
        "token": "haw_captain_polish",
        "idea": "haw_captain_polish",
        "slot": "high_command",
        "ledger": "army",
        "portraits": ARMY_SMALL,
        "extra": True,
        "body": """\
			modifier = {
				special_forces_cap = 24
				special_forces_attack_factor = 2.0
				special_forces_defence_factor = 2.0
				recon_factor = 2.0
				breakthrough_factor = 2.0
				army_speed_factor = 1.0
			}""",
    },
    {
        "token": "haw_professor_clank",
        "idea": "haw_char_professor_clank",
        "slot": "theorist",
        "ledger": "army",
        "portraits": ARMY_SMALL,
        "body": """\
			traits = { haw_theorist }
			research_bonus = {
				land_doctrine = 1.0
				naval_doctrine = 1.0
				air_doctrine = 1.0
			}""",
    },
    {
        "token": "haw_doctor_cog",
        "idea": "haw_char_doctor_cog",
        "slot": "theorist",
        "ledger": "army",
        "portraits": ARMY_SMALL,
        "extra": True,
        "body": """\
			traits = { haw_theorist_cog }
			research_bonus = {
				industry = 1.0
				electronics = 1.0
				air_doctrine = 0.5
			}""",
    },
]


def advisor_block(entry: dict[str, str | bool]) -> str:
    token = str(entry["token"])
    idea = str(entry["idea"])
    slot = str(entry["slot"])
    ledger = str(entry["ledger"])
    portraits = str(entry["portraits"])
    body = str(entry["body"])
    return f"""	generate_character = {{
		token_base = {token}
{portraits}
		advisor = {{
			slot = {slot}
			idea_token = {idea}
			ledger = {ledger}
			allowed = {{ always = yes }}
			visible = {{ always = yes }}
			cost = 0
			can_be_fired = yes
{body}
			ai_will_do = {{ factor = 0 }}
		}}
	}}"""


def guarded_block(entry: dict[str, str | bool]) -> str:
    token = str(entry["token"])
    inner = advisor_block(entry).replace("\n", "\n\t")
    return f"""	if = {{
		limit = {{ NOT = {{ has_character = {token} }} }}
{inner}
	}}"""


def write_history() -> None:
    lines = [
        "# Generated by tools/_gen_house_staff.py. No name = faction namelist.",
        "every_possible_country = {",
        "	set_country_flag = haw_staff_spawned",
    ]
    for entry in STAFF:
        lines.append(advisor_block(entry))
    lines.append("}")
    lines.append("")
    HISTORY.write_text("\n".join(lines), encoding="utf-8")


def write_effects() -> None:
    core = [entry for entry in STAFF if not entry.get("extra")]
    extra = [entry for entry in STAFF if entry.get("extra")]
    lines = [
        "# Generated by tools/_gen_house_staff.py. History characters only exist on a new game.",
        "",
        "haw_ensure_house_staff = {",
        "	if = {",
        "		limit = { NOT = { has_country_flag = haw_staff_spawned } }",
        "		haw_spawn_house_staff = yes",
        "		set_country_flag = haw_staff_spawned",
        "	}",
        "	else = {",
        "		haw_spawn_extra_house_staff = yes",
        "	}",
        "	haw_fix_house_theorists = yes",
        "}",
        "",
        "haw_ensure_player_cheats = {",
        "	if = {",
        "		limit = { NOT = { has_idea = haw_free_picks } }",
        "		add_ideas = haw_free_picks",
        "	}",
        "	haw_ensure_house_staff = yes",
        "	haw_grant_gated_cheats = yes",
        "}",
        "",
        "haw_spawn_house_staff = {",
    ]
    for entry in core:
        lines.append(advisor_block(entry))
    lines.append("	haw_spawn_extra_house_staff = yes")
    lines.append("}")
    lines.append("")
    lines.append("haw_spawn_extra_house_staff = {")
    for entry in extra:
        lines.append(guarded_block(entry))
    lines.append("}")
    lines.append("")
    EFFECTS.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    write_history()
    write_effects()
    print(f"staff={len(STAFF)} extras={sum(1 for e in STAFF if e.get('extra'))} -> {HISTORY.name}, {EFFECTS.name}")


if __name__ == "__main__":
    main()
