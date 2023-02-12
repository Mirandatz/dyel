import datetime as dt

import pydantic
import requests
from loguru import logger
from pydantic import Field
from pydantic.utils import to_lower_camel


class RiotResponseModel(pydantic.BaseModel):
    class Config:
        allow_mutation = False
        validate_assignment = True
        extra = pydantic.Extra.ignore
        alias_generator = to_lower_camel


class Summoner(RiotResponseModel):
    id: str
    account_id: str
    puuid: str
    name: str
    profile_icon_id: int
    revision_date: dt.datetime
    summoner_level: int


class MatchMetadata(RiotResponseModel):
    data_version: str
    match_id: str
    participants: list[str]


class PerkStat(RiotResponseModel):
    defense: int
    flex: int
    offense: int


class PerkSelectionStyle(RiotResponseModel):
    perk: int
    var1: int
    var2: int
    var3: int


class PerkStyle(RiotResponseModel):
    description: str
    selections: list[PerkSelectionStyle]
    style: int


class Perks(RiotResponseModel):
    stat_perks: PerkStat
    styles: list[PerkStyle]


class Participant(RiotResponseModel):
    assists: int
    baron_kills: int
    bounty_level: int
    champ_experience: int
    champ_level: int
    champion_id: int  # Prior to patch 11.4, on Feb 18th, 2021, this field returned invalid championIds. We recommend determining the champion based on the championName field for matches played prior to patch 11.4.
    champion_name: str
    champion_transform: int  # This field is currently only utilized for Kayn's transformations. (Legal values: 0 - None, 1 - Slayer, 2 - Assassin)
    consumables_purchased: int
    damage_dealt_to_buildings: int
    damage_dealt_to_objectives: int
    damage_dealt_to_turrets: int
    damage_self_mitigated: int
    deaths: int
    detector_wards_placed: int
    double_kills: int
    dragon_kills: int
    first_blood_assist: bool
    first_blood_kill: bool
    first_tower_assist: bool
    first_tower_kill: bool
    game_ended_in_early_surrender: bool
    game_ended_in_surrender: bool
    gold_earned: int
    gold_spent: int
    # Both individualPosition and teamPosition are computed by the game server and are different versions of the most likely position played by a player.
    # The individualPosition is the best guess for which position the player actually played in isolation of anything else.
    # The teamPosition is the best guess for which position the player actually played if we add the constraint that each team must have one top player,
    # one jungle, one middle, etc.
    # Generally the recommendation is to use the teamPosition field over the individualPosition field.
    individual_position: str
    inhibitor_kills: int
    inhibitor_takedowns: int
    inhibitors_lost: int
    item0: int
    item1: int
    item2: int
    item3: int
    item4: int
    item5: int
    item6: int
    items_purchased: int
    killing_sprees: int
    kills: int
    lane: str
    largest_critical_strike: int
    largest_killing_spree: int
    largest_multi_kill: int
    longest_time_spent_living: int
    magic_damage_dealt: int
    magic_damage_dealt_to_champions: int
    magic_damage_taken: int
    neutral_minions_killed: int
    nexus_kills: int
    nexus_takedowns: int
    nexus_lost: int
    objectives_stolen: int
    objectives_stolen_assists: int
    participant_id: int
    penta_kills: int
    perks: Perks
    physical_damage_dealt: int
    physical_damage_dealt_to_champions: int
    physical_damage_taken: int
    profile_icon: int
    puuid: str
    quadra_kills: int
    riot_id_name: str
    riot_id_tagline: str
    role: str
    sight_wards_bought_in_game: int
    spell_1_casts: int
    spell_2_casts: int
    spell_3_casts: int
    spell_4_casts: int
    summoner_1_casts: int
    summoner_1_id: int
    summoner_2_casts: int
    summoner_2_id: int
    summoner_id: str
    summoner_level: int
    summoner_name: str
    team_early_surrendered: bool
    team_id: int
    # Both individualPosition and teamPosition are computed by the game server and are different versions of the most likely position played by a player.
    # The individualPosition is the best guess for which position the player actually played in isolation of anything else.
    # The teamPosition is the best guess for which position the player actually played if we add the constraint that each team must have one top player,
    # one jungle, one middle, etc.
    # Generally the recommendation is to use the teamPosition field over the individualPosition field.
    team_position: str
    time_ccing_others: int = Field(alias="timeCCingOthers")
    time_played: int
    total_damage_dealt: int
    total_damage_dealt_to_champions: int
    total_damage_shielded_on_teammates: int
    total_damage_taken: int
    total_heal: int
    total_heals_on_teammates: int
    total_minions_killed: int
    total_time_cc_dealt: int = Field(alias="totalTimeCCDealt")
    total_time_spent_dead: int
    total_units_healed: int
    triple_kills: int
    true_damage_dealt: int
    true_damage_dealt_to_champions: int
    true_damage_taken: int
    turret_kills: int
    turret_takedowns: int
    turrets_lost: int
    unreal_kills: int
    vision_score: int
    vision_wards_bought_in_game: int
    wards_killed: int
    wards_placed: int
    win: bool


class Ban(RiotResponseModel):
    champion_id: int
    pick_turn: int


class Objective(RiotResponseModel):
    first: bool
    kills: int


class Objectives(RiotResponseModel):
    baron: Objective
    champion: Objective
    dragon: Objective
    inhibitor: Objective
    rift_herald: Objective
    tower: Objective


class Team(RiotResponseModel):
    bans: list[Ban]
    objectives: Objectives
    team_id: int
    win: bool


class MatchInfo(RiotResponseModel):
    game_creation: dt.datetime
    game_duration: dt.timedelta
    game_end_timestamp: dt.datetime
    game_id: int
    game_mode: str
    game_start_timestamp: dt.datetime
    game_type: str
    game_version: str
    map_id: int
    participants: list[Participant]
    platform_id: str
    queue_id: int
    teams: list[Team]
    tournament_code: str


class MatchData(RiotResponseModel):
    metadata: MatchMetadata
    info: MatchInfo


class RiotClient(pydantic.BaseSettings):
    api_key: str = Field(..., env="RIOT_API_KEY")

    country_url: str = Field("https://br1.api.riotgames.com", env="RIOT_COUNTRY_URL")

    region_url: str = Field(
        "https://americas.api.riotgames.com",
        env="RIOT_REGION_URL",
    )

    # pydantic magic
    class Config:
        allow_mutation = False
        validate_assignment = True
        extra = pydantic.Extra.forbid
        env_prefix = "DYEL_"
        env_file = "secrets/secrets.env"

    def download_summoner_data(self, summoner_name: str) -> Summoner:
        logger.info(f"downloading summoner data, name={summoner_name}")

        response = requests.get(
            url=f"{self.country_url}/lol/summoner/v4/summoners/by-name/{summoner_name}",
            headers={"X-Riot-Token": self.api_key},
        )
        response.raise_for_status()

        return Summoner(**response.json())

    def download_match_ids(
        self,
        summoner_puuid: str,
        start_index: int = 0,
        count: int = 20,
    ) -> list[str]:
        logger.info(f"downloading match ids, summoner_id={summoner_puuid}")

        response = requests.get(
            url=f"{self.region_url}/lol/match/v5/matches/by-puuid/{summoner_puuid}/ids",
            headers={"X-Riot-Token": self.api_key},
            params={"count": count},
        )
        response.raise_for_status()

        match_ids = response.json()
        assert isinstance(match_ids, list)
        return match_ids

    def download_match_data(self, match_id: str) -> MatchData:
        logger.info(f"downloading match data, match_Id={match_id}")

        response = requests.get(
            url=f"{self.region_url}/lol/match/v5/matches/{match_id}",
            headers={"X-Riot-Token": self.api_key},
        )
        response.raise_for_status()

        return MatchData(**response.json())


def main() -> None:
    riot = RiotClient()
    # summoner = riot.download_summoner_data("Anaab")
    # match_ids = riot.download_match_ids(summoner.puuid)
    # print(match_ids)
    match = riot.download_match_data("BR1_2679279998")
    print([p.champion_name for p in match.info.participants])


if __name__ == "__main__":
    main()
