import matplotlib.pyplot as plt

def visualize_win_percentages(win_percentages):
    labels = list(win_percentages.keys())
    values = list(win_percentages.values())

    fig, ax = plt.subplots()
    bars = ax.bar(labels, values)
    plt.title('Win Percentages for Different Roles lats 50 games')
    plt.xlabel('Roles')
    plt.ylabel('Win Percentage')
    # Zorg ervoor dat de y-as altijd van 0 naar 100% gaat in stappen van 10 
    plt.ylim(0, 100)
    plt.yticks(range(0, 110, 10))

# Voeg het win percentage boven elke bar toe
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2 - 0.15, bar.get_height() + 1,
        f"{value:.2f}%", ha='center', va='bottom')


plt.show()
