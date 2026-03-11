import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

# ─── TEAMS ───────────────────────────────────────────────────────────────────
TEAMS = {
    "Mumbai Indians":       {"abbr": "MI",  "city": "Mumbai"},
    "Chennai Super Kings":  {"abbr": "CSK", "city": "Chennai"},
    "Royal Challengers Bangalore": {"abbr": "RCB", "city": "Bangalore"},
    "Kolkata Knight Riders":{"abbr": "KKR", "city": "Kolkata"},
    "Delhi Capitals":       {"abbr": "DC",  "city": "Delhi"},
    "Sunrisers Hyderabad":  {"abbr": "SRH", "city": "Hyderabad"},
    "Rajasthan Royals":     {"abbr": "RR",  "city": "Jaipur"},
    "Punjab Kings":         {"abbr": "PBKS","city": "Mohali"},
    "Lucknow Super Giants": {"abbr": "LSG", "city": "Lucknow"},
    "Gujarat Titans":       {"abbr": "GT",  "city": "Ahmedabad"},
}
TEAM_NAMES = list(TEAMS.keys())

# ─── PLAYERS ─────────────────────────────────────────────────────────────────
TOP_BATSMEN = [
    ("Virat Kohli","RCB"),("Rohit Sharma","MI"),("Shikhar Dhawan","DC"),
    ("David Warner","SRH"),("Suresh Raina","CSK"),("MS Dhoni","CSK"),
    ("AB de Villiers","RCB"),("KL Rahul","PBKS"),("Gautam Gambhir","KKR"),
    ("Faf du Plessis","CSK"),("Robin Uthappa","KKR"),("Ambati Rayudu","CSK"),
    ("Quinton de Kock","MI"),("Jos Buttler","RR"),("Shreyas Iyer","DC"),
    ("Hardik Pandya","MI"),("Rishabh Pant","DC"),("Ishan Kishan","MI"),
    ("Sanju Samson","RR"),("Dinesh Karthik","KKR"),
]
TOP_BOWLERS = [
    ("Lasith Malinga","MI"),("Dwayne Bravo","CSK"),("Amit Mishra","DC"),
    ("Piyush Chawla","KKR"),("Bhuvneshwar Kumar","SRH"),("Jasprit Bumrah","MI"),
    ("Harbhajan Singh","MI"),("Ravindra Jadeja","CSK"),("Sunil Narine","KKR"),
    ("Imran Tahir","CSK"),("Kuldeep Yadav","KKR"),("Yuzvendra Chahal","RCB"),
    ("Trent Boult","MI"),("Mohammed Shami","PBKS"),("Kagiso Rabada","DC"),
    ("Pat Cummins","KKR"),("Rashid Khan","SRH"),("Deepak Chahar","CSK"),
    ("T Natarajan","SRH"),("Harshal Patel","RCB"),
]

VENUES = [
    "Wankhede Stadium, Mumbai","MA Chidambaram Stadium, Chennai",
    "Eden Gardens, Kolkata","M Chinnaswamy Stadium, Bangalore",
    "Arun Jaitley Stadium, Delhi","Rajiv Gandhi Intl Stadium, Hyderabad",
    "Sawai Mansingh Stadium, Jaipur","Punjab Cricket Association Stadium, Mohali",
    "Narendra Modi Stadium, Ahmedabad","BRSABV Ekana Cricket Stadium, Lucknow",
]

IPL_CHAMPIONS = {
    2008:"Rajasthan Royals", 2009:"Deccan Chargers", 2010:"Chennai Super Kings",
    2011:"Chennai Super Kings", 2012:"Kolkata Knight Riders", 2013:"Mumbai Indians",
    2014:"Kolkata Knight Riders", 2015:"Mumbai Indians", 2016:"Sunrisers Hyderabad",
    2017:"Mumbai Indians", 2018:"Chennai Super Kings", 2019:"Mumbai Indians",
    2020:"Mumbai Indians", 2021:"Chennai Super Kings", 2022:"Gujarat Titans",
    2023:"Chennai Super Kings", 2024:"Kolkata Knight Riders", 2025:"Royal Challengers Bangalore",
}

# ─── GENERATE MATCHES ────────────────────────────────────────────────────────
matches, deliveries = [], []
match_id = 1

for season in range(2008, 2026):
    year_teams = TEAM_NAMES if season >= 2022 else TEAM_NAMES[:8]
    num_matches = 74 if season >= 2022 else 60

    season_matches = []
    for _ in range(num_matches):
        t1, t2 = random.sample(year_teams, 2)
        venue = random.choice(VENUES)
        toss_winner = random.choice([t1, t2])
        toss_decision = random.choice(["bat", "field"])
        bat_first = toss_winner if toss_decision == "bat" else (t2 if toss_winner == t1 else t1)
        bat_second = t2 if bat_first == t1 else t1

        t1_score = random.randint(130, 230)
        t2_score = random.randint(100, t1_score + 30)
        winner = bat_first if t1_score > t2_score else bat_second
        win_by_runs = abs(t1_score - t2_score) if winner == bat_first else 0
        win_by_wickets = random.randint(1, 9) if winner == bat_second else 0
        if t1_score == t2_score:
            result = "Super Over"
        elif winner == bat_first:
            result = f"Won by {win_by_runs} runs"
        else:
            result = f"Won by {win_by_wickets} wickets"

        mom_pool = [p[0] for p in TOP_BATSMEN + TOP_BOWLERS]
        player_of_match = random.choice(mom_pool)

        match_row = {
            "match_id": match_id, "season": season, "date": f"{season}-0{random.randint(1,5)}-{random.randint(10,30):02d}",
            "venue": venue, "team1": t1, "team2": t2,
            "toss_winner": toss_winner, "toss_decision": toss_decision,
            "team1_score": t1_score, "team2_score": t2_score,
            "winner": winner, "win_by_runs": win_by_runs, "win_by_wickets": win_by_wickets,
            "result": result, "player_of_match": player_of_match, "umpire1": "Kumar Dharmasena", "umpire2": "S Ravi",
        }
        matches.append(match_row)
        season_matches.append(match_id)
        match_id += 1

    # Ball-by-ball for subset (first 10 matches each season for performance)
    for mid in season_matches[:15]:
        for innings in [1, 2]:
            runs_left = random.randint(130, 220)
            wickets = 0
            for over in range(20):
                for ball in range(1, 7):
                    if wickets >= 10 or runs_left <= 0:
                        break
                    is_wicket = random.random() < 0.07
                    extras = random.choice([0,0,0,0,1,2]) if random.random() < 0.1 else 0
                    runs = random.choices([0,1,2,3,4,6],[35,25,10,3,15,7])[0]
                    batsman = random.choice(TOP_BATSMEN)[0]
                    bowler = random.choice(TOP_BOWLERS)[0]
                    deliveries.append({
                        "match_id": mid, "inning": innings, "over": over+1,
                        "ball": ball, "batsman": batsman, "bowler": bowler,
                        "batsman_runs": runs, "extra_runs": extras,
                        "total_runs": runs + extras, "is_wicket": int(is_wicket),
                        "dismissal_kind": random.choice(["caught","bowled","lbw","run out","stumped"]) if is_wicket else "",
                    })
                    if is_wicket: wickets += 1

matches_df = pd.DataFrame(matches)
deliveries_df = pd.DataFrame(deliveries)
matches_df.to_csv("/home/claude/ipl-analysis/data/matches.csv", index=False)
deliveries_df.to_csv("/home/claude/ipl-analysis/data/deliveries.csv", index=False)
print(f"✅ Generated {len(matches_df)} matches & {len(deliveries_df)} deliveries")
