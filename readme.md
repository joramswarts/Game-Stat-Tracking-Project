
# Game Data Analytics Project

## Project Overview
This is a Data Engineering project focused on collecting and analyzing in-game user data. The main objective of this project is to retrieve data and user data from League of Legends via the Riot API. Users should be able to run the program, input the in-game username for which they want to collect data. The project not only focuses on providing detailed statistics through a Jupyter Notebook but also introduces automatic data storage to an Azure database. Furthermore, a user-friendly PowerBI dashboard has been implemented to present the data in an accessible manner for users without programming knowledge.

## Motivation
This project is driven by a personal interest in monitoring in-game statistics and the competitive aspect of gaming. The use of stat trackers to analyze in-game data has always caught my attention, and I want to combine this interest with my knowledge and skills to achieve more.

## Project Goals
This project encompasses several objectives:

- Retrieving data from League of Legends through an API.
- Collecting user data and statistics from an API.
- Storing user data and statistics in an Azure database automatically.
- Developing a Jupyter Notebook in which users can input a in-game username and generate detailed statistics.
- Creating a PowerBI dashboard to visually represent general statistics for a more intuitive user experience.

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

In this project, we leverage an Azure SQL database to store user data, facilitating seamless integration with PowerBI for a user-friendly analytics dashboard. Follow the steps below to set up your own Azure SQL database for this project.

### 1. Azure SQL Database Setup

#### a. Create an Azure SQL Database:
   - Go to the [Azure Portal](https://portal.azure.com/).
   - Navigate to "SQL databases" and click "Add" to create a new database.
   - Fill in the required details, such as Database name, Server, and Resource group.
   - Configure the server settings, ensuring that you set up a firewall rule to allow connections.

#### b. Obtain Connection String:
   - Once the database is created, navigate to the "Connection strings" tab in the Azure portal.
   - Copy the connection string; this will be used to connect your Python code to the Azure SQL database.

### 2. Table Creation

In order to store user data, create the necessary tables in your Azure SQL database. Modify the following SQL script according to your requirements:

```sql
-- Example script for creating a 'UserData' table
CREATE TABLE UserData (
    UserID INT PRIMARY KEY,
    UserName NVARCHAR(255) NOT NULL,
    GameStats JSON NOT NULL,
    -- Add additional columns as needed
);
```
### 3. Update Connection in main.ipynb
In the main.ipynb Jupyter Notebook, locate the following code block:

```python
# Connecting to the database
try:
    conn = pyodbc.connect("""
        Driver={ODBC Driver 18 for SQL Server};
        Server=tcp:your_server_name_here.database.windows.net,1433;
        Database=your_database_name_here;
        Uid=your_username_here;
        Encrypt=yes;
        TrustServerCertificate=no;
        Connection Timeout=30;
        Authentication=ActiveDirectoryInteractive
    """)
    cursor = conn.cursor()
except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")
```
Replace the connection string in the pyodbc.connect call with the one you copied from the Azure portal.

Now, your Azure SQL Database should be set up and ready for integration with the Game Data Analytics project. If you encounter any issues or need further assistance, feel free to reach out.

## PowerBI

1. **Download PowerBI Desktop:**
   - If you don't have PowerBI Desktop installed, download and install it from [PowerBI Desktop](https://powerbi.microsoft.com/desktop/).

2. **Open the GitHub Repository:**
   - Navigate to your GitHub repository where the PowerBI file is stored.

3. **Locate the PowerBI File:**
   - Find the PowerBI file (with the extension .pbix) in the repository.

4. **Download the PowerBI File:**
   - Click on the PowerBI file in your GitHub repository.
   - On the file page, click the "Download" button or use the "Download" option in the "Code" dropdown to save the file to your local machine.

5. **Open PowerBI Desktop:**
   - Launch PowerBI Desktop on your machine.

6. **Open the Downloaded PowerBI File:**
   - In PowerBI Desktop, click on "File" in the top menu.
   - Select "Open" and navigate to the location where you downloaded the PowerBI file.
   - Select the file and click "Open."

7. **Update Database Connection:**
   - If the PowerBI file doesn't have the connection information saved, you may need to update the database connection details.
   - Click on "Refresh" to fetch the latest data from your Azure SQL Database.

8. **Review Visualizations:**
   - Explore the visualizations and dashboards within the PowerBI file.
   - Use the filtering and interaction features to analyze the data.

9. **Save Changes (Optional):**
   - If you make any modifications or updates to the file, save the changes by clicking on "File" and selecting "Save" or "Save As."

10. **Publish to Power BI Service (Optional):**
   - If you want to share your PowerBI report online or collaborate with others, you can publish the file to the Power BI service.
   - Click on "Publish" in the top menu and follow the prompts to upload your file to the Power BI service.

For any further assistance or questions related to this project, please feel free to reach out. Good luck with your Game Data Analytics project!
```

You can copy and paste this README into your project repository's documentation, ensuring that you replace placeholders with the actual information and instructions needed for your project. If you have any more specific details or requirements, feel free to include them in the README.