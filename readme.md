
# Game Data Analytics Project

## Project Overview
This is a Data Engineering project focused on collecting and analyzing in-game data of users. The main goal of this project is to retrieve data from League of Legends and extract user statistics using the Riot games API. Users should be able to run the program, input the in-game username for which they want to collect data. Subsequently, the relevant data will be fetched and visualized to provide insights into the game's statistics. As an additional feature, the project also considers creating a PowerBI dashboard to present the data in a user-friendly manner for those without programming knowledge.

## Motivation
This project is driven by a personal interest in monitoring in-game statistics and the competitive aspect of gaming. The use of stat trackers to analyze in-game data has always caught my attention, and I want to combine this interest with my knowledge and skills to achieve more.

## Project Goals
This project encompasses several objectives:

- Retrieving data from League of Legends using their API.
- Collecting user data and statistics for League of Legends through the same API.
- Developing a Jupyter Notebook where users can input a in-game username and generate comprehensive statistics.
- Optionally, creating a PowerBI dashboard that presents general statistics in a user-friendly way.

## Data Sources
- **Riot Games API**: This API will serve as the source for game and user-related information, including details about the game itself, their mechanics, all user stats and other game-specific data. More information on how to use this API can be found in the project's documentation.

## Setup Instructions
To get started with the project, follow these steps:

1. Clone this repository to your local machine.
   ```bash
   git clone https://github.com/joramswarts/game-data-analytics.git
   cd game-data-analytics
   ```

2. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a configuration file (e.g., `config.py`) to store API keys and other project-specific settings. Make sure to include your Riot API key and any other necessary credentials.

4. Run the Jupyter Notebook (`main.ipynb`) to interact with the project. This notebook will guide you through fetching game data and user statistics.

5. Optionally, set up a PowerBI dashboard by following the documentation provided in the `powerbi/` directory.

## Azure Databases
If you have expertise in working with Azure databases, consider using them to store and manage project data. Azure databases can enhance data consistency, security, and accessibility, making it easier to work with historical data and collaborate with team members.

For any further assistance or questions related to this project, please feel free to reach out. Good luck with your Game Data Analytics project!
```

You can copy and paste this README into your project repository's documentation, ensuring that you replace placeholders with the actual information and instructions needed for your project. If you have any more specific details or requirements, feel free to include them in the README.