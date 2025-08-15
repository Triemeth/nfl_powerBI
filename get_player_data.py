import pandas as pd
from datetime import datetime

PREV_YEAR = datetime.now().year - 1
CURR_YEAR = datetime.now().year

def get_data(year, category):

    url = f"https://www.pro-football-reference.com/years/{year}/{category}"
    if category != "passing.htm":
        df = pd.read_html(url, header=1)[0]
    else:
        df = pd.read_html(url)[0]

    return df


if __name__ == "__main__":
    df_qb_prev = get_data(PREV_YEAR, "passing.htm")
    df_rb_prev = get_data(PREV_YEAR, "rushing.htm")
    df_wr_prev = get_data(PREV_YEAR, "receiving.htm")
    df_def_prev = get_data(PREV_YEAR, "defense.htm")

    off_abbreviations = ["C", "RB", "FB", "HB", "OG", "OT", 
                         "LG", "LT", "RG", "RT", "TE", "QB", "WR"]
    df_def_prev = df_def_prev[~df_def_prev["Pos"].isin(off_abbreviations)]

    for i in range(0, len(df_def_prev)):
        df_def_prev.iloc[i, df_def_prev.columns.get_loc("Rk")] = i + 1

    with pd.ExcelWriter(f'data/NFL_{PREV_YEAR}_player.xlsx', engine='xlsxwriter') as writer:
        df_qb_prev.to_excel(writer, sheet_name='QBs')
        df_rb_prev.to_excel(writer, sheet_name='RBs')
        df_wr_prev.to_excel(writer, sheet_name='WRs')
        df_def_prev.to_excel(writer, sheet_name='DEF')
    
    #use this later once the season starts
    """

    df_qb_curr = get_data(CURR_YEAR, "passing.htm")
    df_rb_curr = get_data(CURR_YEAR, "rushing.htm")
    df_wr_curr = get_data(CURR_YEAR, "receiving.htm")
    df_def_curr = get_data(CURR_YEAR, "defense.htm")

    off_abbreviations = ["C", "RB", "FB", "HB", "OG", "OT", 
                         "LG", "LT", "RG", "RT", "TE", "QB", "WR"]
    df_def_curr = df_def_curr[~df_def_curr["Pos"].isin(off_abbreviations)]

    for i in range(0, len(df_def_curr)):
        df_def_curr["RK"] = i

    with pd.ExcelWriter(f'data/NFL_{CURR_YEAR}_player.xlsx', engine='xlsxwriter') as writer:
        df_qb_curr.to_excel(writer, sheet_name='QBs')
        df_rb_curr.to_excel(writer, sheet_name='RBs')
        df_wr_curr.to_excel(writer, sheet_name='WRs')
        df_def_curr.to_excel(writer, sheet_name='DEF')

    """