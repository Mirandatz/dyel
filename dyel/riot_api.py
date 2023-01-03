import datetime as dt

import pydantic
import requests
from loguru import logger


class Summoner(pydantic.BaseModel):
    id: str
    account_id: str = pydantic.Field(alias="accountId")
    puuid: str
    name: str
    profile_icon: int = pydantic.Field(alias="profileIconId")
    revision_date: dt.datetime = pydantic.Field(alias="revisionDate")
    summoner_level: int = pydantic.Field(alias="summonerLevel")


def get_summoner_data(
    summoner_name: str,
    api_key: str,
    country_url: str = "https://br1.api.riotgames.com",
) -> Summoner:
    logger.info(
        f"downloading summoner data, name={summoner_name}, country_url={country_url}"
    )

    r = requests.get(
        url=f"{country_url}/lol/summoner/v4/summoners/by-name/{summoner_name}",
        headers={"X-Riot-Token": api_key},
    )

    r.raise_for_status()
    json = r.json()
    return Summoner(**json)
