import matplotlib.pyplot as plt
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
    win_rates = [data['WinRate'] for data in champion_stats.values()]
    kdas = [data['KDA'] for data in champion_stats.values()]
    total_games = [data['TotalGames'] for data in champion_stats.values()]

    fig, ax = plt.subplots(figsize=(12, 7))

    bars = ax.bar(labels, win_rates, alpha=0.7, label='Win Rate')

    for bar, kda, games, win_rate in zip(bars, kdas, total_games, win_rates):
        text_kda = f'KDA: {kda:.2f}\nGames: {games}\nWin Rate: {win_rate:.2f}%'
        text_x = bar.get_x() + bar.get_width() / 2
        text_y = bar.get_height()

        ax.text(text_x, text_y / 2, text_kda, ha='center', va='center', color='black', fontsize=8)

    plt.title('Champion Win Rate with Games Played, Win Rate, and KDA')
    plt.xlabel('Champion')
    plt.ylabel('Win Rate (%)')

    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

