# HLTV Team and Player Stats Scraper

This project is a Python script that uses **Selenium**, **BeautifulSoup**, and **undetected-chromedriver** to scrape detailed team and player statistics from the [HLTV](https://www.hltv.org) website. The script gathers data on teams, their lineups, and individual player stats, saving the results in a CSV file.

## Features

- Extracts information about teams, maps played, win rates, and lineup statistics.
- Collects individual player stats such as impact, KAST, opening kill ratios, and specific kill types (rifles, snipers, SMGs, pistols, etc.).
- Saves the data into a well-structured CSV file sorted by player names.

## Requirements

Make sure you have the following dependencies installed before running the script:

- Python 3.7 or higher
- Python packages:
  - `selenium`
  - `beautifulsoup4`
  - `undetected-chromedriver`
  - `pandas`
  - `numpy`

You can install the dependencies using a `requirements.txt` file:
```bash
pip install -r requirements.txt
```

## Important Notes
Execution Time: The script navigates through multiple pages and performs web scraping, which may take several minutes to complete.
Pop-up Blockers: Ensure there are no restrictions on pop-ups, as the script opens new tabs to collect data.
Date Range: This script is configured to extract data for 2023. To change the date range, modify the line:
```
driver.get('https://www.hltv.org/stats/teams?startDate=2024-08-27&endDate=2024-11-27&rankingFilter=Top50') #Example
```

## CSV Structure
The generated CSV file will include the following columns:

- PLAYER: Player's name.
- TEAM: Team name and lineup year.
- MAPS_PLAYED: Number of maps played.
- WINRATE: Win rate percentage.
- HLTV-IMPACT: Impact rating.
- KAST: KAST percentage (Kills, Assists, Survived, Traded).
- OPENING_Kills: Number of opening kills.
- OK_Ratio: Opening kills ratio.
- RIFLE_Kills: Rifle kills.
- SNIPER_Kills: Sniper kills.
- SMG_Kills: SMG kills.
- PISTOL_Kills: Pistol kills.
- TOTAL_Kills: Total kills of all matchs.
- %HEADSHOT: Percentage of headshots
- TOTAL_Deaths: Total deaths of all matchs.
- K/D_Ratio: KD percentage (Kills, Deaths)
- DAMAGE/Round: 
- GRANADE_DMG/Round:
- MAPS_PLAYED:
- ROUNDS_PLAYED:
- KILLS/Round:
- ASSISTS/Round:
- DEATHS/Rounds:
- SAVED BY TEAMMATE/Round:
- SAVED TEAMMATES/Round:
- RATING 2.1: Rating 2.1 of HLTV.

## Problems detected
You can avoid this problem by modifying code in the undetected_chromedriver\__init__.py.

Go to line 789 (it was not the line in my case) and wrap the time.sleep(0.1) with try-except block here is how the final code look like
```
try:
  time.sleep(0.1)
except:
  pass
```

Thank you for using this scraper! Feel free to open an issue if you have any questions or suggestions.
