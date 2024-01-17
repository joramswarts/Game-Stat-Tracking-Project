import pyodbc
from lol_data import calculate_win_percentage_per_role, get_match_data_extended
import hashlib

def generate_unique_id(summoner_name, queue_type):
    # Hash the combination of summoner name and queue type to create a unique ID
    unique_id = hashlib.md5(f"{summoner_name}-{queue_type}".encode()).hexdigest()
    return unique_id

def WinrateTable(matches, summoner_data, summoner_name, queue_type, cursor, conn):
    win_percentages = calculate_win_percentage_per_role(matches, summoner_data['puuid'])
    unique_id = generate_unique_id(summoner_name, queue_type)

    try:
        cursor.execute("""
            MERGE INTO Winrate_Table AS Target
            USING (VALUES (?, ?, ?, ?, ?, ?, ?)) AS Source (UniqueID, Overall, TopLane, Jungle, MidLane, ADC, Support)
            ON Target.UniqueID = Source.UniqueID
            WHEN MATCHED THEN
                UPDATE SET
                    Overall = Source.Overall,
                    TopLane = Source.TopLane,
                    Jungle = Source.Jungle,
                    MidLane = Source.MidLane,
                    ADC = Source.ADC,
                    Support = Source.Support
            WHEN NOT MATCHED THEN
                INSERT (UniqueID, Overall, TopLane, Jungle, MidLane, ADC, Support)
                VALUES (Source.UniqueID, Source.Overall, Source.TopLane, Source.Jungle, Source.MidLane, Source.ADC, Source.Support);
        """,
        (unique_id,
        win_percentages['Overall']['Win Percentage'],
        win_percentages['Top']['Win Percentage'],
        win_percentages['Jungle']['Win Percentage'],
        win_percentages['Middle']['Win Percentage'],
        win_percentages['Bottom']['Win Percentage'],
        win_percentages['Utility']['Win Percentage']))

        conn.commit()
        print("Winrates added to the database!")
    except pyodbc.Error as e:
        print(f"Error inserting winrates into the database: {e}")


def SynergyTable(unique_id, champion_synergy, cursor, conn):
    try:
        for user_champion, synergies in champion_synergy.items():
            for teammate_champion, data in synergies.items():
                cursor.execute("""
                    INSERT INTO Synergy_Table (UniqueID, SynergyChampName, ChampionName, WinRate, AverageKDA)
                    VALUES (?, ?, ?, ?, ?)
                """,
                (unique_id, user_champion, teammate_champion, 
                 sum(data['winrate']) / data['games_played'] if data['games_played'] > 0 else 0,
                 sum(data['kda']) / data['games_played'] if data['games_played'] > 0 else 0))
                conn.commit()
        print("Synergy-Table filled with data!")
    except pyodbc.Error as e:
        print(f"Error inserting data into Synergy-Table: {e}")


def SummonerDataTable(unique_id, summoner_data, queue_type, cursor, conn):
    try:
        cursor.execute("""
            MERGE INTO Summoner_Data_Table AS Target
            USING (VALUES (?, ?, ?, ?)) AS Source (UniqueID, SummonerName, SummonerLevel, QueueType)
            ON Target.UniqueID = Source.UniqueID
            WHEN MATCHED THEN
                UPDATE SET
                    SummonerName = Source.SummonerName,
                    SummonerLevel = Source.SummonerLevel,
                    QueueType = Source.QueueType
            WHEN NOT MATCHED THEN
                INSERT (UniqueID, SummonerName, SummonerLevel, QueueType)
                VALUES (Source.UniqueID, Source.SummonerName, Source.SummonerLevel, Source.QueueType);
        """,
        (unique_id,
        summoner_data['name'],
        summoner_data['summonerLevel'],
        queue_type))

        conn.commit()
        print("Summoner data added to the database!")
    except pyodbc.Error as e:
        print(f"Error inserting summoner data into the database: {e}")

def MatchDataTable(unique_id, matches, summoner_puuid, cursor, conn):
    try:
        if matches:
            for match in matches:
                match_id = match['metadata']['matchId']
                champion_played = None
                game_duration = match['info']['gameDuration']
                win_loss = None
                baron_kills = 0
                dragon_kills = 0
                turret_kills = 0
                minion_kills = 0
                wards_placed = 0
                wards_killed = 0
                vision_score = 0
                
                for participant in match['info']['participants']:
                    if participant['puuid'] == summoner_puuid:
                        champion_played = participant['championName']
                        win_loss = participant['win']
                        kills = participant['kills']
                        deaths = participant['deaths']
                        assists = participant['assists']
                        baron_kills = participant['baronKills']
                        dragon_kills = participant['dragonKills']
                        turret_kills = participant['turretKills']
                        minion_kills = participant['totalMinionsKilled']
                        wards_placed = participant['wardsPlaced']
                        wards_killed = participant['wardsKilled']
                        vision_score = participant['visionScore']

                        cursor.execute("""
                            MERGE INTO Match_Data_Table AS Target
                            USING (
                                SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                            ) AS Source (UniqueID, MatchID, Champion, Kills, Deaths, Assists, WinLoss, GameDuration, BaronKills, DragonKills, TurretKills, MinionKills, Wards_Placed, Wards_killed, VisionScore)
                            ON Target.UniqueID = Source.UniqueID AND Target.MatchID = Source.MatchID
                            WHEN MATCHED THEN
                                UPDATE SET
                                    Champion = Source.Champion,
                                    Kills = Source.Kills,
                                    Deaths = Source.Deaths,
                                    Assists = Source.Assists,
                                    WinLoss = Source.WinLoss,
                                    GameDuration = Source.GameDuration,
                                    BaronKills = Source.BaronKills,
                                    DragonKills = Source.DragonKills,
                                    TurretKills = Source.TurretKills,
                                    MinionKills = Source.MinionKills,
                                    Wards_Placed = Source.Wards_Placed,
                                    Wards_killed = Source.Wards_killed,
                                    VisionScore = Source.VisionScore
                            WHEN NOT MATCHED THEN
                                INSERT (UniqueID, MatchID, Champion, Kills, Deaths, Assists, WinLoss, GameDuration, BaronKills, DragonKills, TurretKills, MinionKills, Wards_Placed, Wards_killed, VisionScore)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                        """,
                        (unique_id, match_id, champion_played, kills, deaths, assists, win_loss, game_duration, baron_kills, dragon_kills, turret_kills, minion_kills, wards_placed, wards_killed, vision_score,
                        unique_id, match_id, champion_played, kills, deaths, assists, win_loss, game_duration, baron_kills, dragon_kills, turret_kills, minion_kills, wards_placed, wards_killed, vision_score))

            conn.commit()
            print("Match data added to Match-Data-Table!")
        else:
            print("No matches available to add into Match-Data-Table.")
    except pyodbc.Error as e:
        print(f"Error inserting data into Match-Data-Table: {e}")
    finally:
        cursor.close()
        conn.close()