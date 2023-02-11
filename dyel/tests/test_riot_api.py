import datetime as dt

import dyel.riot_api


def test_download_summoner_data() -> None:
    client = dyel.riot_api.RiotClient()
    summoner = client.download_summoner_data("Mephy")

    assert summoner.name == "Mephy"
    assert (
        summoner.puuid
        == "iICvb22W3-OAPKdgPEto9eIOwHbuGjiuCIhbExpmXZYx4mQuosBu_LKZSW_9PYWFVvxdz7UaLzMkcQ"
    )
    assert summoner.id == "whn4axlxBaWmkCaakVFfJds6Rn52PQo2M8X8e1BFbGvP"
    assert summoner.account_id == "NSpquHoF_vBQYLZ4ZG7nGoRK8-2fhxUDOKxAc14PTjg"
    assert summoner.summoner_level == 42
    assert summoner.revision_date == dt.datetime(
        year=2022, month=2, day=27, hour=20, minute=58, second=18, tzinfo=dt.UTC
    )
