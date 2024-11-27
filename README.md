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
driver.get('https://www.hltv.org/stats/teams?startDate=2023-01-01&endDate=2023-12-31')
```

## CSV Structure
The generated CSV file will include the following columns:

- playerName: Player's name.
- teamName: Team name and lineup year.
- mapsPlayed: Number of maps played.
- winrate: Win rate percentage.
- hltvImpact: Impact rating.
- KAST: KAST percentage (kills, assists, survived, traded).
- openingKills: Number of opening kills.
- OKratio: Opening kills ratio.
- rifleKills: Rifle kills.
- sniperKills: Sniper kills.
- smgKills: SMG kills.
- pistolKills: Pistol kills.
Additional stats dynamically scraped from the player's page.

## Contributions
To contribute to this project:
1. Fork this repository.
2. Create a new branch for your changes: git checkout -b feature-new-functionality.
3. Submit a pull request with your improvements.

## Problems
You can avoid this problem by modifying code in the undetected_chromedriver\__init__.py.

Go to line 789 (it was not the line in my case) and wrap the time.sleep(0.1) with try-except block here is how the final code look like
```
try:
  time.sleep(0.1)
except:
  pass
```

Thank you for using this scraper! Feel free to open an issue if you have any questions or suggestions.
