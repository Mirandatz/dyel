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

    class Config:
        validiate_all = True


class RiotClient(pydantic.BaseSettings):
    api_key: str = pydantic.Field(..., env="RIOT_API_KEY")

    country_url: str = pydantic.Field(
        "https://br1.api.riotgames.com", env="RIOT_COUNTRY_URL"
    )

    region_url: str = pydantic.Field(
        "https://americas.api.riotgames.com",
        env="RIOT_REGION_URL",
    )

    # pydantic magic
    class Config:
        env_prefix = "DYEL_"
        env_file = "secrets/secrets.env"

    def download_summoner_data(self, summoner_name: str) -> Summoner:
        logger.info(f"downloading summoner data, name={summoner_name}")

        response = requests.get(
            url=f"{self.country_url}/lol/summoner/v4/summoners/by-name/{summoner_name}",
            headers={"X-Riot-Token": self.api_key},
        )

        response.raise_for_status()
        json = response.json()
        return Summoner(**json)


def main() -> None:
    riot = RiotClient()
    summoner = riot.download_summoner_data("Mephy")
    print(summoner)


if __name__ == "__main__":
    main()
