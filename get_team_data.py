import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from bs4 import BeautifulSoup

PREV_YEAR = datetime.now().year - 1
CURR_YEAR = datetime.now().year


def get_chrome_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ssl-version-max=tls1.2")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(options=options)

def get_off(year):
    url = f"https://www.pro-football-reference.com/years/{year}/index.htm"

    driver = get_chrome_driver()
    driver.get(url)

    table = driver.find_element(By.ID, "team_stats")
    soup = BeautifulSoup(table.get_attribute("outerHTML"), "html.parser")

    df = pd.read_html(str(soup), header = 1)[0]

    df_len = len(df)
    for i in range(4):
        df.at[df_len-i, "Rk"] = 999

    df = df[pd.to_numeric(df['Rk'], errors='coerce').notnull()]
    df = df.iloc[:-1]

    driver.quit()

    return df

def get_def(year):
    url = f"https://www.pro-football-reference.com/years/{year}/opp.htm"
    df = pd.read_html(url, header=1)[0]

    return df

if __name__ == "__main__":
    prev_off_df = get_off(PREV_YEAR)
    prev_def_df = get_def(PREV_YEAR)

    with pd.ExcelWriter(f'data/NFL_{PREV_YEAR}_team.xlsx', engine='xlsxwriter') as writer:
        prev_off_df.to_excel(writer, sheet_name=f'Offensive_team_stats_{PREV_YEAR}')
        prev_def_df.to_excel(writer, sheet_name=f'Defensive_team_stats_{PREV_YEAR}')

    #use this later once the season starts
    """
    
    curr_off_df = get_off(CURR_YEAR)
    curr_def_df = get_def(CURR_YEAR)

    with pd.ExcelWriter(f'data/NFL_{CURR_YEAR}_team.xlsx', engine='xlsxwriter') as writer:
        curr_off_df.to_excel(writer, sheet_name=f'Offensive_team_stats_{CURR_YEAR}')
        curr_def_df.to_excel(writer, sheet_name=f'Defensive_team_stats_{CURR_YEAR}')
        
    """
        