import json

import dyel.riot_api


def test_download_summoner_data() -> None:
    client = dyel.riot_api.RiotClient(dyel.riot_api.RiotApiSettings())
    raw = client.download_summoner_data("Mephy")
    data = json.loads(raw)

    assert list(data.keys()) == [
        "id",
        "accountId",
        "puuid",
        "name",
        "profileIconId",
        "revisionDate",
        "summonerLevel",
    ]

    assert data["name"] == "Mephy"
    assert (
        data["puuid"]
        == "iICvb22W3-OAPKdgPEto9eIOwHbuGjiuCIhbExpmXZYx4mQuosBu_LKZSW_9PYWFVvxdz7UaLzMkcQ"
    )
    assert data["id"] == "whn4axlxBaWmkCaakVFfJds6Rn52PQo2M8X8e1BFbGvP"
    assert data["accountId"] == "NSpquHoF_vBQYLZ4ZG7nGoRK8-2fhxUDOKxAc14PTjg"
    assert data["summonerLevel"] == 42
    assert data["revisionDate"] == 1645995498000


def test_download_match_ids() -> None:
    client = dyel.riot_api.RiotClient(dyel.riot_api.RiotApiSettings())
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


# def test_download_match_data_champion_names() -> None:
# client = dyel.riot_api.RiotClient()
# match_data = client.download_match_data("BR1_2679279998")
# assert [
#     "Ahri",
#     "FiddleSticks",
#     "Lillia",
#     "Aphelios",
#     "Lux",
#     "Sion",
#     "MasterYi",
#     "AurelionSol",
#     "MissFortune",
#     "Senna",
# ] == [p.champion_name for p in match_data.info.participants]
