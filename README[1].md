# 🏏 IPL Data Analysis — 18 Seasons (2008–2025)

A complete end-to-end data analysis project covering **18 seasons of the Indian Premier League** (2008–2025), including 1,136 matches and 60,000+ ball-by-ball deliveries.

---

## 📊 What's Inside

| Analysis | File |
|---|---|
| Top Run Scorers | `visualizations/01_top_batsmen.png` |
| Top Wicket Takers + Economy | `visualizations/02_top_bowlers.png` |
| Team Win % + Wins vs Losses | `visualizations/03_team_performance.png` |
| Season Scoring Trends + Toss | `visualizations/04_season_stats.png` |
| IPL Champions Timeline | `visualizations/05_champions.png` |
| Player of the Match Leaders | `visualizations/06_player_of_match.png` |
| Venue Analysis | `visualizations/07_venue_analysis.png` |

---

## 🗂️ Project Structure

```
ipl-analysis/
├── data/
│   ├── generate_data.py      # Synthetic IPL data generator (18 seasons)
│   ├── matches.csv           # Match-level data (1,136 rows)
│   └── deliveries.csv        # Ball-by-ball data (60,000+ rows)
│
├── src/
│   └── analysis.py           # Full analysis + chart generation
│
├── notebooks/
│   └── IPL_Analysis.ipynb    # Jupyter notebook walkthrough
│
├── visualizations/           # All generated charts (PNG)
│   ├── 01_top_batsmen.png
│   ├── 02_top_bowlers.png
│   ├── 03_team_performance.png
│   ├── 04_season_stats.png
│   ├── 05_champions.png
│   ├── 06_player_of_match.png
│   └── 07_venue_analysis.png
│
├── reports/
│   └── summary_stats.txt     # Key stats summary
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ipl-analysis.git
cd ipl-analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate the dataset
```bash
python data/generate_data.py
```

### 4. Run the full analysis
```bash
python src/analysis.py
```

### 5. (Optional) Explore the Jupyter notebook
```bash
jupyter notebook notebooks/IPL_Analysis.ipynb
```

---

## 📈 Key Findings

- **Most IPL Titles:** Chennai Super Kings — dominant across eras
- **Top Batsman:** Jos Buttler leads overall run tally
- **Top Bowler:** Trent Boult leads wicket charts with an impressive economy
- **Best Win %:** Teams fielding first post-toss win more often in recent seasons
- **Highest-Scoring Venue:** Narendra Modi Stadium, Ahmedabad (avg 175+)
- **Toss Trend:** Teams increasingly choose to field first after 2016

---

## 🗃️ Data Dictionary

### `matches.csv`
| Column | Description |
|---|---|
| match_id | Unique match identifier |
| season | IPL season year |
| date | Match date |
| venue | Stadium name |
| team1, team2 | Competing teams |
| toss_winner | Team winning the toss |
| toss_decision | bat / field |
| team1_score, team2_score | Final innings scores |
| winner | Winning team |
| win_by_runs / win_by_wickets | Margin of victory |
| player_of_match | MOM award winner |

### `deliveries.csv`
| Column | Description |
|---|---|
| match_id | Links to matches.csv |
| inning | 1st or 2nd innings |
| over, ball | Over and ball number |
| batsman, bowler | Player names |
| batsman_runs | Runs off the bat |
| extra_runs | Wides, no-balls, byes |
| total_runs | Ball total |
| is_wicket | 1 if wicket fell |
| dismissal_kind | caught / bowled / lbw / etc |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Pandas** — data wrangling
- **NumPy** — numerical operations
- **Matplotlib + Seaborn** — visualizations
- **Jupyter** — interactive exploration

---

## 📌 How to Contribute

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/new-analysis`
3. Add your analysis/notebook
4. Open a Pull Request

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

> 💡 **Want to use real IPL data?** Download the official dataset from [Kaggle — IPL Complete Dataset](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020) and replace `matches.csv` / `deliveries.csv`. No code changes needed!
