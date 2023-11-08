
# Game Data Analytics Project

## Project Overview
This is a Data Engineering project focused on collecting and analyzing in-game data of users. The main goal of this project is to retrieve data from various games using the RARG video game database API and extract user statistics by web scraping from tracker.gg, a popular stats tracking website. Users should be able to run the program, input their in-game username, and specify the game for which they want to collect data. Subsequently, the relevant data will be fetched and visualized to provide insights into the game's statistics. As an additional feature, the project also considers creating a PowerBI dashboard to present the data in a user-friendly manner for those without programming knowledge.

## Motivation
This project is driven by a personal interest in monitoring in-game statistics and the competitive aspect of gaming. The use of stat trackers to analyze in-game data has always caught my attention, and I want to combine this interest with my knowledge and skills to achieve more.

## Project Goals
This project encompasses several objectives:

- Retrieving data from various games using the RARG video game database API.
- Collecting user data and statistics for different games through web scraping.
- Developing a Jupyter Notebook where users can input the game's name and generate comprehensive statistics.
- Considering the possibility of entering the username to fetch statistics for different players.
- Optionally, creating a PowerBI dashboard that presents general statistics in a user-friendly way.

## Data Sources
- **RARG Video Game Database API**: This API will serve as the source for game-related information, including details about different games, their mechanics, and other game-specific data. More information on how to use this API can be found in the project's documentation.

- **tracker.gg**: This website will be used to scrape user statistics for various games. You may need to implement web scraping techniques to extract the necessary data. Make sure to respect the website's terms of use and consider rate limiting to avoid overloading their servers.

## Setup Instructions
To get started with the project, follow these steps:

1. Clone this repository to your local machine.
   ```bash
   git clone https://github.com/yourusername/game-data-analytics.git
   cd game-data-analytics
   ```

2. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a configuration file (e.g., `config.yaml`) to store API keys and other project-specific settings. Make sure to include your RARG API key and any other necessary credentials.

4. Run the Jupyter Notebook (`game_data_analytics.ipynb`) to interact with the project. This notebook will guide you through fetching game data and user statistics.

5. Optionally, set up a PowerBI dashboard by following the documentation provided in the `powerbi/` directory.

## Azure Databases
If you have expertise in working with Azure databases, consider using them to store and manage project data. Azure databases can enhance data consistency, security, and accessibility, making it easier to work with historical data and collaborate with team members.

For any further assistance or questions related to this project, please feel free to reach out. Good luck with your Game Data Analytics project!
```

You can copy and paste this README into your project repository's documentation, ensuring that you replace placeholders with the actual information and instructions needed for your project. If you have any more specific details or requirements, feel free to include them in the README.