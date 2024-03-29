# Importing all libraries and data needed to run visuals
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from lol_data import get_item_name
import datetime
import seaborn as sns
import numpy as np

# Barplot that gives insight about win percentages per role
def visualize_win_percentages(win_percentages):
    labels = list(win_percentages.keys())
    values = [data["Win Percentage"] for data in win_percentages.values()]

    # Add styling for the plot
    fig, ax = plt.subplots(figsize=(8, 7), facecolor='#191A24')
    ax.set_facecolor('#232448')
    fig.subplots_adjust(top=0.85, bottom=0.15)
    fig.set_facecolor('#191A24')

    bars = ax.bar(labels, values, color='#56C596')
    plt.title('Win Percentages for Different Roles', y=1.1, color='white')
    plt.xlabel('Roles', color='white')
    plt.ylabel('Win Percentage', color='white')

    # Add the win percentage above each bar without overlapping
    for bar, data in zip(bars, win_percentages.values()):
        text = f"{data['Win Percentage']:.2f}%\n(Matches: {data['Total Matches']})"
        text_x = bar.get_x() + bar.get_width() / 2 - 0.15
        text_y = bar.get_height() + 1

        # Check if the text will overlap with the top border
        if text_y > ax.get_ylim()[1] - 1:
            text_y = ax.get_ylim()[1] - 1 - 2

        ax.annotate(text, (text_x, text_y), ha='center', va='bottom',
                    xytext=(0, 8), textcoords='offset points', color='white', fontsize=8)

    # Set y-axis limits to always go from 0 to 100 with a small gap at the top
    ax.set_ylim(0, 102)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    plt.tight_layout()
    plt.show()

# Lineplot that gives insight about win percentages in the last 2 weeks
def plot_win_percentage_over_time(matches, summoner_data):
    # Gather dates from each match
    match_dates = [datetime.datetime.utcfromtimestamp(match['info']['gameCreation'] // 1000).strftime('%Y-%m-%d') for match in matches]

    # Gather dates from the last 14 days
    last_two_weeks = datetime.datetime.utcnow() - datetime.timedelta(days=14)
    recent_dates = [date for date in sorted(set(match_dates)) if datetime.datetime.strptime(date, '%Y-%m-%d') >= last_two_weeks]

    # Count WR, dates and amount of matches for each day
    win_percentages_by_date = []
    num_matches_by_date = []

    for date in sorted(set(recent_dates)):
        total_matches_on_date = sum(1 for match, match_date in zip(matches, match_dates) if match_date == date and 'info' in match and 'participants' in match['info'])
        total_wins_on_date = sum(1 for match, match_date in zip(matches, match_dates) if match_date == date and 'info' in match and 'participants' in match['info'] and any(participant['win'] for participant in match['info']['participants'] if participant['puuid'] == summoner_data['puuid']))

        win_percentage_on_date = (total_wins_on_date / total_matches_on_date) * 100 if total_matches_on_date > 0 else None
        win_percentages_by_date.append(win_percentage_on_date)
        num_matches_by_date.append(total_matches_on_date)
    
    # Count total games
    total_games = sum(num_matches_by_date)
    print(f"Total games in the last two weeks for this queue type: {total_games}")

    # Plot the lineplot and add styling
    fig, ax = plt.subplots(facecolor='#191A24')
    ax.set_facecolor('#232448')
    ax.plot(sorted(set(recent_dates)), win_percentages_by_date, marker='o', color='#56C596')

    plt.title('Win Percentage Over the Last Two Weeks', color='white')
    plt.xlabel('Date', color='white')
    plt.ylabel('Win Percentage', color='white')

    # Set y-axis limits to always span from 0 to 100
    ax.set_yticks(range(0, 101, 10))
    ax.set_yticklabels([f"{i}%" for i in range(0, 101, 10)])

    # Add the WR and amount of matches to the points in the plot
    for date, win_percentage, num_matches in zip(sorted(set(recent_dates)), win_percentages_by_date, num_matches_by_date):
        if win_percentage is not None:
            ax.text(date, win_percentage, f"{win_percentage:.2f}%\n{num_matches} games", ha='right', va='bottom', fontsize=8, color='white')

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.xticks(rotation=45, color='white')
    plt.tight_layout()
    plt.show()

# Barplot that gives insight about win percentages and KDA from all champions played by user.
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

    # Gathering plot values
    labels = list(champion_stats.keys())
    kdas = [data['KDA'] for data in champion_stats.values()]
    win_rates = [data['WinRate'] for data in champion_stats.values()]
    total_games = [data['TotalGames'] for data in champion_stats.values()]

    fig, ax = plt.subplots(figsize=(12, 7), facecolor='#191A24')
    ax.set_facecolor('#232448')

    bars = ax.bar(labels, kdas, alpha=0.7, label='KDA', color='#56C596')

    for bar, kda, win_rate, games in zip(bars, kdas, win_rates, total_games):
        text_kda = f'KDA: {kda:.2f}\nWR: {win_rate:.2f}%\nGames: {games}'
        text_x = bar.get_x() + bar.get_width() / 2
        text_y = bar.get_height()

        ax.text(text_x, text_y / 2, text_kda, ha='center', va='center', color='white', fontsize=5.5)

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.title('Champion KDA with Win Rate and Games Played', color='white')
    plt.xlabel('Champion', color='white')
    plt.ylabel('KDA', color='white')

    plt.legend()
    plt.xticks(rotation=45, color='white')
    plt.tight_layout()
    plt.show()

# Table visual that gives insight about best item builds for each champion calculated by user winrate.
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

# Barplot that gives insight about the synergy from your top 3 most played champions with the other champions in game.
def visualize_champion_synergy(champion_synergy, top_champions, min_games_played=2):
    # Set up subplots for each top champion
    num_top_champions = len(top_champions)
    fig, axes = plt.subplots(num_top_champions, 2, figsize=(15, 10 * num_top_champions), sharey='row', gridspec_kw={'hspace': 0.5})
    fig.set_facecolor('#191A24')
    fig.suptitle('Champion Synergy for your top 3 most played champions', color='white')

    for i, champion in enumerate(top_champions):
        # Extract synergy data for the current champion
        synergy_data = champion_synergy[champion]

        # Filter teammate champions with games played greater than the threshold and non-zero winrate
        filtered_synergy_data = {teammate: data for teammate, data in synergy_data.items() if data['games_played'] >= min_games_played and np.mean(data['winrate']) > 0}

        # Plot Winrate Synergy
        winrate_synergy = {teammate: np.mean(data['winrate']) * 100 if data['winrate'] else np.nan for teammate, data in filtered_synergy_data.items()}
        sorted_winrate_synergy = sorted(winrate_synergy.items(), key=lambda x: x[1], reverse=True)
        teammate_names, winrates = zip(*sorted_winrate_synergy)

        # Plot the bar chart
        ax1 = sns.barplot(x=winrates, y=teammate_names, hue=teammate_names, ax=axes[i, 0], palette='crest', dodge=False)
        ax1.set_facecolor('#232448') 
        axes[i, 0].set_title(f'Winrate Synergy for {champion}', color='white')
        axes[i, 0].set_xlabel('Winrate (%)', color='white')
        axes[i, 0].set_ylabel('Teammate Champion', color='white')

        # Add winrate values to the bars
        for bar, winrate, teammate_name in zip(axes[i, 0].patches, winrates, teammate_names):
            height = bar.get_height()
            games_played = filtered_synergy_data[teammate_name]['games_played']
            axes[i, 0].text(bar.get_x() + bar.get_width() / 2, bar.get_y() + height / 2, f'WR: {winrate:.2f}% | Games: {games_played}', ha='center', va='center', fontsize=8, color='white')

        # Set text color for ticks on x and y axes
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')

        # Plot KDA Synergy
        kda_synergy = {teammate: np.mean(data['kda']) if data['kda'] else np.nan for teammate, data in filtered_synergy_data.items()}
        sorted_kda_synergy = sorted(kda_synergy.items(), key=lambda x: x[1], reverse=True)
        teammate_names, kdas = zip(*sorted_kda_synergy)

        # Plot the bar chart
        ax1 = sns.barplot(x=kdas, y=teammate_names, hue=teammate_names, ax=axes[i, 1], palette='crest', dodge=False)
        ax1.set_facecolor('#232448') 
        axes[i, 1].set_title(f'KDA Synergy for {champion}', color='white')
        axes[i, 1].set_xlabel('Average KDA', color='white')
        axes[i, 1].set_ylabel('Teammate Champion', color='white')

        # Add KDA values to the bars
        for bar, kda, teammate_name in zip(axes[i, 1].patches, kdas, teammate_names):
            height = bar.get_height()
            games_played = filtered_synergy_data[teammate_name]['games_played']
            axes[i, 1].text(bar.get_x() + bar.get_width() / 2, bar.get_y() + height / 2, f'KDA: {kda:.2f} | Games: {games_played}', ha='center', va='center', fontsize=8, color='white')

        # Set text color for ticks on x and y axes
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
    plt.show()
    