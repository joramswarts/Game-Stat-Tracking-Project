
import pyodbc
from lol_data import calculate_win_percentage_per_role, calculate_champion_synergy

import hashlib

def generate_unique_id(summoner_name, queue_type):
    # Hash the combination of summoner name and queue type to create a unique ID
    unique_id = hashlib.md5(f"{summoner_name}-{queue_type}".encode()).hexdigest()
    return unique_id

def WinrateTable(matches, summoner_data, summoner_name, queue_type):
    # Verbinding maken met de database
    try:
        conn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};Server=tcp:jarvis-cloud-verzamelen-joram.database.windows.net,1433;Database=BitAcademyDB;Uid=152791@student.horizoncollege.nl;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryInteractive")
        cursor = conn.cursor()
    except pyodbc.Error as e:
        print(f"Fout bij het verbinden met de database: {e}")

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
        print("Winrates toegevoegd aan de database!")
    except pyodbc.Error as e:
        print(f"Fout bij het invoegen van winrates in de database: {e}")
    finally:
        cursor.close()
        conn.close()

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
        # Commit the changes
        conn.commit()
        print("Synergy-Table gevuld met data!")
    except pyodbc.Error as e:
        print(f"Fout bij het invoegen van data in Synergy-Table: {e}")
