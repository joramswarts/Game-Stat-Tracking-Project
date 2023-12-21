import matplotlib.pyplot as plt
import plotly.graph_objects as go
from lol_data import get_item_name
import datetime

def visualize_win_percentages(win_percentages):
    # Visualization using matplotlib
    labels = list(win_percentages.keys())
    values = [data["Win Percentage"] for data in win_percentages.values()]  # Extract win percentages

    fig, ax = plt.subplots(figsize=(8, 7))  # Adjust the figure size
    fig.subplots_adjust(top=0.85, bottom=0.15)  # Adjust the top and bottom space

    bars = ax.bar(labels, values)
    plt.title('Win Percentages for Different Roles', y=1.1)  # Adjust the title position
    plt.xlabel('Roles')
    plt.ylabel('Win Percentage')

    # Add the win percentage above each bar without overlapping
    for bar, data in zip(bars, win_percentages.values()):
        text = f"{data['Win Percentage']:.2f}%\n(Matches: {data['Total Matches']})"
        text_x = bar.get_x() + bar.get_width() / 2 - 0.15
        text_y = bar.get_height() + 1

        # Check if the text will overlap with the top border
        if text_y > ax.get_ylim()[1] - 1:
            text_y = ax.get_ylim()[1] - 1 - 2  # Adjust the y-coordinate to leave a small gap at the top

        ax.annotate(text, (text_x, text_y), ha='center', va='bottom',
                    xytext=(0, 8), textcoords='offset points', color='black', fontsize=8)  # Adjust xytext for vertical offset

    # Set y-axis limits to always span from 0 to 100 with a small gap at the top
    ax.set_ylim(0, 102)

    plt.tight_layout()
    plt.show()


def plot_win_percentage_over_time(matches, summoner_data):
    # Verzamel datums voor elke wedstrijd
    match_dates = [datetime.datetime.utcfromtimestamp(match['info']['gameCreation'] // 1000).strftime('%Y-%m-%d') for match in matches]

    # Verkrijg datums van de afgelopen 14 dagen
    last_two_weeks = datetime.datetime.utcnow() - datetime.timedelta(days=14)
    recent_dates = [date for date in sorted(set(match_dates)) if datetime.datetime.strptime(date, '%Y-%m-%d') >= last_two_weeks]

    # Houd winstpercentages, datums en het aantal wedstrijden bij voor elke dag
    win_percentages_by_date = []
    num_matches_by_date = []

    for date in sorted(set(recent_dates)):
        total_matches_on_date = sum(1 for match, match_date in zip(matches, match_dates) if match_date == date and 'info' in match and 'participants' in match['info'])
        total_wins_on_date = sum(1 for match, match_date in zip(matches, match_dates) if match_date == date and 'info' in match and 'participants' in match['info'] and any(participant['win'] for participant in match['info']['participants'] if participant['puuid'] == summoner_data['puuid']))

        win_percentage_on_date = (total_wins_on_date / total_matches_on_date) * 100 if total_matches_on_date > 0 else None
        win_percentages_by_date.append(win_percentage_on_date)
        num_matches_by_date.append(total_matches_on_date)
    
    # Print het totaal aantal wedstrijden in de terminal
    total_games = sum(num_matches_by_date)
    print(f"Total games in the last two weeks for this queue type: {total_games}")

    # Plot de lijngrafiek
    fig, ax = plt.subplots()
    ax.plot(sorted(set(recent_dates)), win_percentages_by_date, marker='o')

    plt.title('Win Percentage Over the Last Two Weeks')
    plt.xlabel('Date')
    plt.ylabel('Win Percentage')

    # Stel de stappen op de y-as in van 0 naar 100
    ax.set_yticks(range(0, 101, 10))
    ax.set_yticklabels([f"{i}%" for i in range(0, 101, 10)])

    # Voeg winstpercentages en het aantal wedstrijden toe aan de bolletjes
    for date, win_percentage, num_matches in zip(sorted(set(recent_dates)), win_percentages_by_date, num_matches_by_date):
        if win_percentage is not None:
            ax.text(date, win_percentage, f"{win_percentage:.2f}%\n{num_matches} games", ha='right', va='bottom', fontsize=8)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def visualize_champion_stats(matches, summoner_data):
    summoner_puuid = summoner_data['puuid']

    champion_stats = {}

    for match in matches:
        if 'info' in match and 'participants' in match['info']:
            for participant in match['info']['participants']:
                if 'championInfo' in participant and participant['puuid'] == summoner_puuid:
                    champion_name = participant['championInfo']['name']
                    if champion_name not in champion_stats:
                        champion_stats[champion_name] = {'Wins': 0, 'TotalGames': 0, 'KDA': 0}

                    champion_stats[champion_name]['TotalGames'] += 1
                    if participant.get('win', False):
                        champion_stats[champion_name]['Wins'] += 1

                    # Calculate KDA (kills + assists / deaths)
                    kills = participant['kills']
                    deaths = participant['deaths']
                    assists = participant['assists']
                    champion_stats[champion_name]['KDA'] += (kills + assists) / max(1, deaths)

    for champion_name, stats in champion_stats.items():
        stats['WinRate'] = (stats['Wins'] / stats['TotalGames']) * 100 if stats['TotalGames'] > 0 else 0
        stats['KDA'] /= stats['TotalGames']

    # Visualization using matplotlib
    labels = list(champion_stats.keys())
    kdas = [data['KDA'] for data in champion_stats.values()]
    win_rates = [data['WinRate'] for data in champion_stats.values()]
    total_games = [data['TotalGames'] for data in champion_stats.values()]

    fig, ax = plt.subplots(figsize=(12, 7))

    bars = ax.bar(labels, kdas, alpha=0.7, label='KDA')

    for bar, kda, win_rate, games in zip(bars, kdas, win_rates, total_games):
        text_kda = f'KDA: {kda:.2f}\nWR: {win_rate:.2f}%\nGames: {games}'
        text_x = bar.get_x() + bar.get_width() / 2
        text_y = bar.get_height()

        ax.text(text_x, text_y / 2, text_kda, ha='center', va='center', color='black', fontsize=5.5)

    plt.title('Champion KDA with Win Rate and Games Played')
    plt.xlabel('Champion')
    plt.ylabel('KDA')

    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def create_table_visual(matches, summoner_puuid):
    # Create the table_data
    table_data = []

    # Dictionary to store win and total match counts for each champion and build combination
    champion_build_stats = {}

    for match in matches:
        if 'info' in match and 'participants' in match['info']:
            for participant in match['info']['participants']:
                if participant['puuid'] == summoner_puuid:
                    # Extract relevant information
                    champion_name = participant['championInfo']['name']
                    items = [f"{i+1}. {get_item_name(participant[f'item{i}'])}" for i in range(4)]
                    win = participant.get('win', False)

                    # Add data to the table_data
                    table_data.append({
                        'Champion Name': champion_name,
                        'Item Build': items,
                        'Win': win
                    })

                    # Update champion and build stats
                    key = (champion_name, tuple(items))
                    if key not in champion_build_stats:
                        champion_build_stats[key] = {'wins': 0, 'total_matches': 0}
                    champion_build_stats[key]['total_matches'] += 1
                    if win:
                        champion_build_stats[key]['wins'] += 1

# Create a dictionary to store unique builds for each champion
    unique_builds = {}

    for match in matches:
        if 'info' in match and 'participants' in match['info']:
            for participant in match['info']['participants']:
                if participant['puuid'] == summoner_puuid:
                    # Extract relevant information
                    champion_name = participant['championInfo']['name']
                    items = [get_item_name(participant[f'item{i}']) for i in range(4)]
                    win = participant.get('win', False)

                    # Update champion and build stats
                    key = (champion_name, tuple(items))
                    if key not in unique_builds:
                        unique_builds[key] = {'wins': 0, 'total_matches': 0}
                    unique_builds[key]['total_matches'] += 1
                    if win:
                        unique_builds[key]['wins'] += 1

# Create the table_data using unique builds
    table_data = []
    for key, stats in unique_builds.items():
        champion_name, items = key
        win_percentage = (stats['wins'] / stats['total_matches']) * 100 if stats['total_matches'] > 0 else 0

        # Add data to the table_data
        table_data.append({
            'Champion Name': champion_name,
            'Item Build': [f"{i+1}. {item}" for i, item in enumerate(items)],
            'Result': f"{win_percentage:.2f}% ({stats['wins']} wins, {stats['total_matches'] - stats['wins']} losses)",
            'Win Percentage': win_percentage
        })

# Sort table_data based on 'Champion Name' alphabetically and 'Win Percentage' in descending order
    table_data = sorted(table_data, key=lambda x: (x['Champion Name'], -x['Win Percentage']))

# Create the table figure
    fig = go.Figure(data=[go.Table(
        header=dict(values=['<b>Champion Name<b>', '<b>Item Build<b>', '<b>Result<b>'],
                    fill_color='#191A24',  # Set background color for header
                    font=dict(color='#56C596'),  # Set text color for header
                    align='left'),
        cells=dict(values=[
            [entry['Champion Name'] for entry in table_data],
            ['<br>'.join(entry['Item Build']) for entry in table_data],
            [entry['Result'] for entry in table_data]
        ],
                fill_color='#232448',  # Set background color for cells
                font=dict(color='#56C596'),  # Set text color for cells
                align='left'))
    ])

# Set layout properties for a scrollable table
    fig.update_layout(
        height=600,
        autosize=True,
        margin=dict(l=0, r=0, b=0, t=0),
    )

    fig.show()

