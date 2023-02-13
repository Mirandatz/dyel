import backoff
import limits as rate_limit_lib
import pydantic
import requests
from loguru import logger
from pydantic import Field


class RiotAPISettings(pydantic.BaseSettings):
    api_key: str = Field(..., env="RIOT_API_KEY")

    country_url: str = Field(
        "https://br1.api.riotgames.com",
        env="RIOT_COUNTRY_URL",
    )

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


class RiotClient:
    def __init__(self, api_settings: RiotAPISettings) -> None:
        self._rate_limiter = rate_limit_lib.strategies.FixedWindowRateLimiter(
            rate_limit_lib.storage.MemoryStorage()
        )
        self._rate_limits = (
            rate_limit_lib.parse("20 per second"),
            rate_limit_lib.parse("100 per 2 minute"),
        )
        self.api_settings = api_settings

    @backoff.on_exception(backoff.expo, TimeoutError, max_tries=3)
    def _check_api_limits(self) -> None:
        for limit in self._rate_limits:
            if not self._rate_limiter.hit(limit, "normal_query"):
                raise TimeoutError(f"about to hit rate limit=<{limit}>")

    def download_summoner_data(self, summoner_name: str) -> bytes:
        logger.info(f"downloading summoner data, name={summoner_name}")

        self._check_api_limits()

        response = requests.get(
            url=f"{self.api_settings.country_url}/lol/summoner/v4/summoners/by-name/{summoner_name}",
            headers={"X-Riot-Token": self.api_settings.api_key},
        )
        response.raise_for_status()

        return response.content

    def download_match_ids(
        self,
        summoner_puuid: str,
        start_index: int = 0,
        count: int = 20,
    ) -> list[str]:
        logger.info(f"downloading match ids, summoner_id={summoner_puuid}")

        self._check_api_limits()

        response = requests.get(
            url=f"{self.api_settings.region_url}/lol/match/v5/matches/by-puuid/{summoner_puuid}/ids",
            headers={"X-Riot-Token": self.api_settings.api_key},
            params={
                "start_index": start_index,
                "count": count,
            },
        )
        response.raise_for_status()

        match_ids = response.json()
        assert isinstance(match_ids, list)
        return match_ids

    def download_match_data(self, match_id: str) -> bytes:
        logger.info(f"downloading match data, match_Id={match_id}")

        self._check_api_limits()

        response = requests.get(
            url=f"{self.api_settings.region_url}/lol/match/v5/matches/{match_id}",
            headers={"X-Riot-Token": self.api_settings.api_key},
        )
        response.raise_for_status()

        return response.content
