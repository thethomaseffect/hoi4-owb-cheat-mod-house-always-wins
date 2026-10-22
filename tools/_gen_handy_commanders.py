"""History templates + spawn effects for namelist Handy commanders."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "history" / "general" / "haw_handy_commanders.txt"
EFFECTS = ROOT / "common" / "scripted_effects" / "haw_commander_spawn.txt"
SLOTS = 24

ARMY_TRAITS = """\
			old_guard brilliant_strategist inflexible_strategist politically_connected brave war_hero career_officer trait_cautious media_personality infantry_officer cavalry_officer armor_officer engineer_officer irregulars_officer militias_officer jaeger organizer cavalry_leader infantry_leader skilled_staffer trickster adaptable winter_expert trait_engineer panzer_leader commando panzer_expert combined_arms_expert cavalry_expert scavenger infantry_expert ambusher camouflage_expert guerilla_fighter
			desert_fox desert_fox_II swamp_fox swamp_fox_II hill_fighter hill_fighter_II trait_mountaineer trait_mountaineer_II urban_assault_specialist urban_assault_specialist_II ranger ranger_II jungle_rat jungle_rat_II winter_specialist winter_specialist_II rad_rat rad_rat_II fortress_buster skirmisher paratrooper air_force_liaison naval_invader invader_ii naval_liason expert_improviser logistics_wizard
			strong_trait rooted_trait pain_train_trait strong_back_trait perceptive_trait awareness_trait sniper_trait night_person_trait enduring_trait survivalist_trait life_giver_trait aqua_boy_trait charismatic_trait local_leader_trait animal_friend_trait inspirational_trait intelligent_trait gun_nut_trait robotics_expert_trait nerd_rage_trait agile_trait gunslinger_trait lead_foot_trait ninja_trait lucky_trait idiot_savant_trait mysterious_stranger_trait bloody_mess_trait savage_leader_trait observant_leader_trait tough_leader_trait loved_leader_trait cunning_leader_trait nimble_leader_trait fortunate_leader_trait flexible_trait negotiator_trait cult_of_personality_trait smooth_talker_trait ferocious_loyalty_trait vigilant_recycler_trait junk_rounds_trait melee_hacker_trait light_touch_trait heavyweight_trait fight_the_power_trait sneering_imperialist_trait ranger_trait antivenom_trait one_man_army_trait
			commando_trait tight_nuts_trait tech_wizard_trait targeting_computer_trait hot_blooded_trait hoarder_trait built_to_destroy_trait fast_metabolism skilled_trait bruiser_trait fast_shot_trait finesse_trait pyromaniac_trait camouflage_trait xenotech_expert_trait fortune_finder_trait"""

MARSHAL_TRAITS = """\
			old_guard brilliant_strategist inflexible_strategist politically_connected brave war_hero career_officer trait_cautious media_personality infantry_officer cavalry_officer armor_officer engineer_officer irregulars_officer militias_officer jaeger organizer cavalry_leader infantry_leader skilled_staffer trickster adaptable winter_expert trait_engineer panzer_leader commando panzer_expert combined_arms_expert cavalry_expert scavenger infantry_expert ambusher camouflage_expert guerilla_fighter
			offensive_doctrine defensive_doctrine fast_planner thorough_planner unyielding_defender aggressive_assaulter organisational_leader inspirational_leader expert_delegator
			desert_fox desert_fox_II swamp_fox swamp_fox_II hill_fighter hill_fighter_II trait_mountaineer trait_mountaineer_II urban_assault_specialist urban_assault_specialist_II ranger ranger_II jungle_rat jungle_rat_II winter_specialist winter_specialist_II rad_rat rad_rat_II fortress_buster skirmisher paratrooper air_force_liaison naval_invader invader_ii naval_liason expert_improviser logistics_wizard
			strong_trait rooted_trait pain_train_trait strong_back_trait perceptive_trait awareness_trait sniper_trait night_person_trait enduring_trait survivalist_trait life_giver_trait aqua_boy_trait charismatic_trait local_leader_trait animal_friend_trait inspirational_trait intelligent_trait gun_nut_trait robotics_expert_trait nerd_rage_trait agile_trait gunslinger_trait lead_foot_trait ninja_trait lucky_trait idiot_savant_trait mysterious_stranger_trait bloody_mess_trait savage_leader_trait observant_leader_trait tough_leader_trait loved_leader_trait cunning_leader_trait nimble_leader_trait fortunate_leader_trait flexible_trait negotiator_trait cult_of_personality_trait smooth_talker_trait ferocious_loyalty_trait vigilant_recycler_trait junk_rounds_trait melee_hacker_trait light_touch_trait heavyweight_trait fight_the_power_trait sneering_imperialist_trait ranger_trait antivenom_trait one_man_army_trait
			commando_trait tight_nuts_trait tech_wizard_trait targeting_computer_trait hot_blooded_trait hoarder_trait built_to_destroy_trait fast_metabolism skilled_trait bruiser_trait fast_shot_trait finesse_trait pyromaniac_trait camouflage_trait xenotech_expert_trait fortune_finder_trait"""

NAVY_TRAITS = """\
			seawolf fleet_protector blockade_runner superior_tactician spotter fly_swatter ironside air_controller silent_hunter torpedo_expert lancer destroyer_leader loading_drill_master hunter_killer cruiser_captain search_pattern_expert lone_wolf concealment_expert mine_sweeper mine_layer smoke_screen_expert big_guns_expert ground_pounder safety_first marksman crisis_magician flight_deck_manager fighter_director
			arctic_water_expert inshore_fighter blue_water_expert green_water_expert
			old_guard_navy gentlemanly gunnery_expert chief_engineer navy_media_personality bold navy_career_officer battleship_adherent aviation_enthusiast naval_lineage
			submarine_officer destroyer_officer cruiser_officer heavy_ship_officer carrier_officer"""

TYPES = [
    (
        "general",
        "corps_commander",
        """		corps_commander = {{
			skill = 9
			attack_skill = 9
			defense_skill = 9
			planning_skill = 9
			logistics_skill = 9
			traits = {{
{traits}
			}}
		}}""",
        ARMY_TRAITS,
        """			army = {
				large = "GFX_portrait_haw_servebot"
				small = "GFX_idea_haw_handy"
			}""",
    ),
    (
        "marshal",
        "field_marshal",
        """		field_marshal = {{
			skill = 9
			attack_skill = 9
			defense_skill = 9
			planning_skill = 9
			logistics_skill = 9
			traits = {{
{traits}
			}}
		}}""",
        MARSHAL_TRAITS,
        """			army = {
				large = "GFX_portrait_haw_servebot"
				small = "GFX_idea_haw_handy"
			}""",
    ),
    (
        "admiral",
        "navy_leader",
        """		navy_leader = {{
			skill = 9
			attack_skill = 9
			defense_skill = 9
			maneuvering_skill = 9
			coordination_skill = 9
			traits = {{
{traits}
			}}
		}}""",
        NAVY_TRAITS,
        """			army = {
				large = "GFX_portrait_haw_servebot"
				small = "GFX_idea_haw_handy"
			}
			navy = {
				large = "GFX_portrait_haw_servebot"
				small = "GFX_idea_haw_handy"
			}""",
    ),
]


def token(kind: str, index: int) -> str:
    return f"haw_handy_{kind}_{index}"


def write_history() -> None:
    lines = [
        "# Generated by tools/_gen_handy_commanders.py. always = no registers templates only.",
        "every_possible_country = {",
        "	limit = { always = no }",
    ]
    for kind, _role, role_block, traits, portraits in TYPES:
        for index in range(1, SLOTS + 1):
            lines.append("	generate_character = {")
            lines.append(f"		token_base = {token(kind, index)}")
            lines.append("		portraits = {")
            lines.append(portraits)
            lines.append("		}")
            lines.append(role_block.format(traits=traits))
            lines.append("	}")
    lines.append("}")
    lines.append("")
    HISTORY.write_text("\n".join(lines), encoding="utf-8")


def write_effects() -> None:
    lines = [
        "# Generated by tools/_gen_handy_commanders.py.",
        "# Each click takes the next free template so HOI4 can roll a new namelist name.",
        "",
        "haw_spawn_handy_commanders = {",
        "	haw_spawn_handy_general = yes",
        "	haw_spawn_handy_general = yes",
        "	haw_spawn_handy_general = yes",
        "	haw_spawn_handy_general = yes",
        "	haw_spawn_handy_general = yes",
        "	haw_spawn_handy_marshal = yes",
        "	haw_spawn_handy_marshal = yes",
        "	haw_spawn_handy_marshal = yes",
        "	haw_spawn_handy_marshal = yes",
        "	haw_spawn_handy_marshal = yes",
        "	haw_spawn_handy_admiral = yes",
        "	haw_spawn_handy_admiral = yes",
        "	haw_spawn_handy_admiral = yes",
        "	haw_spawn_handy_admiral = yes",
        "	haw_spawn_handy_admiral = yes",
        "}",
        "",
    ]
    for kind, *_rest in TYPES:
        lines.append(f"haw_spawn_handy_{kind} = {{")
        for index in range(1, SLOTS + 1):
            name = token(kind, index)
            keyword = "if" if index == 1 else "else_if"
            lines.append(f"	{keyword} = {{")
            lines.append("		limit = {")
            lines.append(f"			NOT = {{ has_character = {name} }}")
            lines.append("		}")
            lines.append("		generate_character = {")
            lines.append(f"			token_base = {name}")
            lines.append("		}")
            lines.append("	}")
        lines.append("}")
        lines.append("")
    EFFECTS.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    write_history()
    write_effects()
    print(f"slots={SLOTS} -> {HISTORY.name}, {EFFECTS.name}")


if __name__ == "__main__":
    main()
