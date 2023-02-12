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


def test_download_match_ids() -> None:
    client = dyel.riot_api.RiotClient()
    matche_ids = client.download_match_ids(
        "iICvb22W3-OAPKdgPEto9eIOwHbuGjiuCIhbExpmXZYx4mQuosBu_LKZSW_9PYWFVvxdz7UaLzMkcQ"
    )

    assert [
        "BR1_2472222428",
        "BR1_2472191151",
        "BR1_2472128723",
        "BR1_2472097811",
        "BR1_2472154409",
        "BR1_2472141852",
        "BR1_2471846293",
        "BR1_2471863746",
        "BR1_2471822184",
        "BR1_2471769668",
        "BR1_2471656432",
        "BR1_2471644185",
        "BR1_2471662348",
        "BR1_2471650880",
        "BR1_2471099968",
        "BR1_2471058695",
        "BR1_2471085906",
        "BR1_2471043682",
        "BR1_2471031171",
        "BR1_2471027705",
    ] == matche_ids
