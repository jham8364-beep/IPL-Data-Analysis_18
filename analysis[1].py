"""
IPL Data Analysis — 18 Seasons (2008–2025)
Covers: Top Batsmen, Top Bowlers, Team Performance, Win %, Season Stats
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings, os
warnings.filterwarnings("ignore")

# ── Paths ──────────────────────────────────────────────────────────────────
BASE   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA   = os.path.join(BASE, "data")
VIZ    = os.path.join(BASE, "visualizations")
os.makedirs(VIZ, exist_ok=True)

# ── Load ───────────────────────────────────────────────────────────────────
matches    = pd.read_csv(f"{DATA}/matches.csv")
deliveries = pd.read_csv(f"{DATA}/deliveries.csv")

TEAM_COLORS = {
    "Mumbai Indians":              "#004C93",
    "Chennai Super Kings":         "#FDB913",
    "Royal Challengers Bangalore": "#EC1C24",
    "Kolkata Knight Riders":       "#3A225D",
    "Delhi Capitals":              "#17449B",
    "Sunrisers Hyderabad":         "#F7A721",
    "Rajasthan Royals":            "#EA1A8E",
    "Punjab Kings":                "#DCDDDF",
    "Lucknow Super Giants":        "#A72056",
    "Gujarat Titans":              "#1C4373",
}

sns.set_theme(style="darkgrid", palette="muted")
plt.rcParams.update({"figure.dpi": 130, "font.family": "DejaVu Sans"})

# ═══════════════════════════════════════════════════════════════════════════
# 1. TOP BATSMEN  (by total runs from deliveries)
# ═══════════════════════════════════════════════════════════════════════════
def plot_top_batsmen():
    runs = (deliveries.groupby("batsman")["batsman_runs"]
            .agg(Total_Runs="sum", Innings="count")
            .reset_index()
            .sort_values("Total_Runs", ascending=False)
            .head(15))

    fig, ax = plt.subplots(figsize=(13, 7))
    colors = plt.cm.YlOrRd(np.linspace(0.4, 0.9, len(runs)))
    bars = ax.barh(runs["batsman"][::-1], runs["Total_Runs"][::-1], color=colors[::-1], edgecolor="white", height=0.7)

    for bar, val in zip(bars, runs["Total_Runs"][::-1]):
        ax.text(bar.get_width() + 20, bar.get_y() + bar.get_height()/2,
                f"{val:,}", va="center", fontsize=9, fontweight="bold")

    ax.set_title("🏏 Top 15 Run Scorers — IPL 2008–2025", fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Total Runs", fontsize=12)
    ax.set_xlim(0, runs["Total_Runs"].max() * 1.12)
    ax.tick_params(axis="y", labelsize=10)
    plt.tight_layout()
    plt.savefig(f"{VIZ}/01_top_batsmen.png", bbox_inches="tight")
    plt.close()
    print("  ✅ 01_top_batsmen.png")
    return runs

# ═══════════════════════════════════════════════════════════════════════════
# 2. TOP BOWLERS  (by wickets)
# ═══════════════════════════════════════════════════════════════════════════
def plot_top_bowlers():
    wickets = (deliveries[deliveries["is_wicket"] == 1]
               .groupby("bowler")["is_wicket"]
               .sum()
               .reset_index()
               .rename(columns={"is_wicket": "Wickets"})
               .sort_values("Wickets", ascending=False)
               .head(15))

    # Economy rate
    econ = (deliveries.groupby("bowler")
            .apply(lambda x: (x["total_runs"].sum() / max(len(x)/6, 1)))
            .reset_index(name="Economy"))

    wickets = wickets.merge(econ, on="bowler")

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Wickets bar
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(wickets)))
    axes[0].barh(wickets["bowler"][::-1], wickets["Wickets"][::-1], color=colors[::-1], edgecolor="white")
    axes[0].set_title("🎯 Top 15 Wicket Takers", fontsize=14, fontweight="bold")
    axes[0].set_xlabel("Wickets")
    for i, (w, name) in enumerate(zip(wickets["Wickets"][::-1], wickets["bowler"][::-1])):
        axes[0].text(w + 0.3, i, str(w), va="center", fontsize=9, fontweight="bold")

    # Economy scatter
    top20_bowlers = wickets.head(20)
    sc = axes[1].scatter(top20_bowlers["Economy"], top20_bowlers["Wickets"],
                         s=120, c=top20_bowlers["Wickets"], cmap="RdYlGn_r",
                         edgecolors="white", linewidths=0.5, zorder=3)
    for _, row in top20_bowlers.iterrows():
        axes[1].annotate(row["bowler"].split()[-1], (row["Economy"], row["Wickets"]),
                         textcoords="offset points", xytext=(5, 3), fontsize=7)
    axes[1].set_title("Economy Rate vs Wickets (Top 20)", fontsize=14, fontweight="bold")
    axes[1].set_xlabel("Economy Rate")
    axes[1].set_ylabel("Wickets")
    plt.colorbar(sc, ax=axes[1], label="Wickets")

    plt.suptitle("🏏 Bowling Analysis — IPL 2008–2025", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(f"{VIZ}/02_top_bowlers.png", bbox_inches="tight")
    plt.close()
    print("  ✅ 02_top_bowlers.png")
    return wickets

# ═══════════════════════════════════════════════════════════════════════════
# 3. TEAM PERFORMANCE — Wins, Win%, Most Successful
# ═══════════════════════════════════════════════════════════════════════════
def plot_team_performance():
    all_teams = pd.concat([matches["team1"], matches["team2"]]).value_counts().reset_index()
    all_teams.columns = ["team", "matches_played"]

    wins = matches["winner"].value_counts().reset_index()
    wins.columns = ["team", "wins"]

    perf = all_teams.merge(wins, on="team", how="left").fillna(0)
    perf["wins"] = perf["wins"].astype(int)
    perf["losses"] = perf["matches_played"] - perf["wins"]
    perf["win_pct"] = (perf["wins"] / perf["matches_played"] * 100).round(1)
    perf = perf.sort_values("win_pct", ascending=False)

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # Stacked bar — wins vs losses
    x = range(len(perf))
    bar_colors = [TEAM_COLORS.get(t, "#888888") for t in perf["team"]]
    axes[0].bar(x, perf["wins"], color=bar_colors, label="Wins", edgecolor="white")
    axes[0].bar(x, perf["losses"], bottom=perf["wins"], color="#cccccc", alpha=0.5, label="Losses", edgecolor="white")
    axes[0].set_xticks(list(x))
    axes[0].set_xticklabels([t.replace(" ", "\n") for t in perf["team"]], fontsize=7.5)
    axes[0].set_title("Wins vs Losses per Team", fontsize=13, fontweight="bold")
    axes[0].set_ylabel("Matches")
    axes[0].legend()

    # Win percentage horizontal bar
    colors2 = [TEAM_COLORS.get(t, "#888888") for t in perf["team"]]
    axes[1].barh(perf["team"][::-1], perf["win_pct"][::-1], color=colors2[::-1], edgecolor="white", height=0.7)
    for i, (pct, name) in enumerate(zip(perf["win_pct"][::-1], perf["team"][::-1])):
        axes[1].text(pct + 0.3, i, f"{pct}%", va="center", fontsize=9, fontweight="bold")
    axes[1].set_xlim(0, 80)
    axes[1].axvline(50, color="red", linestyle="--", linewidth=1, alpha=0.6, label="50% line")
    axes[1].set_title("Win Percentage by Team", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Win %")
    axes[1].legend()

    plt.suptitle("🏆 Team Performance — IPL 2008–2025", fontsize=15, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{VIZ}/03_team_performance.png", bbox_inches="tight")
    plt.close()
    print("  ✅ 03_team_performance.png")
    return perf

# ═══════════════════════════════════════════════════════════════════════════
# 4. SEASON-WISE STATS
# ═══════════════════════════════════════════════════════════════════════════
def plot_season_stats():
    season_stats = (matches.groupby("season")
                    .agg(Total_Matches=("match_id","count"),
                         Avg_Team1_Score=("team1_score","mean"),
                         Avg_Team2_Score=("team2_score","mean"))
                    .reset_index())
    season_stats["Avg_Score"] = ((season_stats["Avg_Team1_Score"] + season_stats["Avg_Team2_Score"]) / 2).round(1)

    # Toss decision trend
    toss = (matches.groupby(["season","toss_decision"])
            .size().reset_index(name="count"))
    toss_piv = toss.pivot(index="season", columns="toss_decision", values="count").fillna(0)

    fig, axes = plt.subplots(2, 1, figsize=(14, 10))

    # Average scores per season
    axes[0].plot(season_stats["season"], season_stats["Avg_Team1_Score"],
                 marker="o", color="#1a73e8", linewidth=2, label="Batting First Avg")
    axes[0].plot(season_stats["season"], season_stats["Avg_Team2_Score"],
                 marker="s", color="#e83a1a", linewidth=2, label="Chasing Avg")
    axes[0].fill_between(season_stats["season"], season_stats["Avg_Team1_Score"],
                         season_stats["Avg_Team2_Score"], alpha=0.1, color="gray")
    axes[0].set_title("Average Innings Score per Season", fontsize=13, fontweight="bold")
    axes[0].set_ylabel("Average Runs")
    axes[0].legend()
    axes[0].set_xticks(season_stats["season"])

    # Toss decision
    if "bat" in toss_piv.columns and "field" in toss_piv.columns:
        axes[1].bar(toss_piv.index, toss_piv["bat"], label="Chose to Bat", color="#FDB913", edgecolor="white")
        axes[1].bar(toss_piv.index, toss_piv["field"], bottom=toss_piv["bat"],
                    label="Chose to Field", color="#004C93", edgecolor="white")
    axes[1].set_title("Toss Decision Trend per Season", fontsize=13, fontweight="bold")
    axes[1].set_ylabel("Number of Matches")
    axes[1].set_xlabel("Season")
    axes[1].legend()
    axes[1].set_xticks(toss_piv.index)

    plt.suptitle("📊 Season-wise Trends — IPL 2008–2025", fontsize=15, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{VIZ}/04_season_stats.png", bbox_inches="tight")
    plt.close()
    print("  ✅ 04_season_stats.png")

# ═══════════════════════════════════════════════════════════════════════════
# 5. IPL CHAMPIONS HISTORY
# ═══════════════════════════════════════════════════════════════════════════
def plot_champions():
    IPL_CHAMPIONS = {
        2008:"Rajasthan Royals", 2009:"Kolkata Knight Riders", 2010:"Chennai Super Kings",
        2011:"Chennai Super Kings", 2012:"Kolkata Knight Riders", 2013:"Mumbai Indians",
        2014:"Kolkata Knight Riders", 2015:"Mumbai Indians", 2016:"Sunrisers Hyderabad",
        2017:"Mumbai Indians", 2018:"Chennai Super Kings", 2019:"Mumbai Indians",
        2020:"Mumbai Indians", 2021:"Chennai Super Kings", 2022:"Gujarat Titans",
        2023:"Chennai Super Kings", 2024:"Kolkata Knight Riders", 2025:"Royal Challengers Bangalore",
    }
    champ_df = pd.DataFrame(list(IPL_CHAMPIONS.items()), columns=["Season","Champion"])
    titles = champ_df["Champion"].value_counts().reset_index()
    titles.columns = ["Team","Titles"]

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Title count
    colors = [TEAM_COLORS.get(t, "#888888") for t in titles["Team"]]
    axes[0].bar(titles["Team"], titles["Titles"], color=colors, edgecolor="white", width=0.6)
    for i, v in enumerate(titles["Titles"]):
        axes[0].text(i, v + 0.05, str(v), ha="center", fontsize=11, fontweight="bold")
    axes[0].set_xticklabels([t.replace(" ", "\n") for t in titles["Team"]], fontsize=8)
    axes[0].set_title("🏆 IPL Titles Won", fontsize=13, fontweight="bold")
    axes[0].set_ylabel("Titles")

    # Timeline
    champ_colors = [TEAM_COLORS.get(t, "#888888") for t in champ_df["Champion"]]
    axes[1].scatter(champ_df["Season"], [1]*len(champ_df), s=200, c=champ_colors, zorder=3, edgecolors="white", linewidths=1)
    for _, row in champ_df.iterrows():
        axes[1].annotate(row["Champion"].split()[-1], (row["Season"], 1),
                         textcoords="offset points", xytext=(0, 12),
                         ha="center", fontsize=7, rotation=40)
    axes[1].plot(champ_df["Season"], [1]*len(champ_df), color="gray", alpha=0.3, zorder=1)
    axes[1].set_yticks([])
    axes[1].set_title("🗓 Champions Timeline 2008–2025", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Season")

    legend_patches = [mpatches.Patch(color=TEAM_COLORS.get(t,"#888"), label=t) for t in titles["Team"]]
    axes[1].legend(handles=legend_patches, loc="lower right", fontsize=7, ncol=2)

    plt.suptitle("👑 IPL Champions History", fontsize=15, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{VIZ}/05_champions.png", bbox_inches="tight")
    plt.close()
    print("  ✅ 05_champions.png")
    return champ_df

# ═══════════════════════════════════════════════════════════════════════════
# 6. PLAYER OF THE MATCH LEADERS
# ═══════════════════════════════════════════════════════════════════════════
def plot_mom():
    mom = (matches["player_of_match"].value_counts().head(15)
           .reset_index())
    mom.columns = ["Player","Awards"]

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.Oranges(np.linspace(0.4, 0.9, len(mom)))
    ax.bar(mom["Player"], mom["Awards"], color=colors, edgecolor="white")
    ax.set_xticklabels(mom["Player"], rotation=35, ha="right", fontsize=9)
    for i, v in enumerate(mom["Awards"]):
        ax.text(i, v + 0.1, str(v), ha="center", fontsize=9, fontweight="bold")
    ax.set_title("⭐ Player of the Match Awards — Top 15", fontsize=14, fontweight="bold")
    ax.set_ylabel("Awards")
    plt.tight_layout()
    plt.savefig(f"{VIZ}/06_player_of_match.png", bbox_inches="tight")
    plt.close()
    print("  ✅ 06_player_of_match.png")

# ═══════════════════════════════════════════════════════════════════════════
# 7. VENUE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
def plot_venues():
    venue_stats = (matches.groupby("venue")
                   .agg(Matches=("match_id","count"),
                        Avg_Score=("team1_score","mean"))
                   .reset_index()
                   .sort_values("Matches", ascending=False)
                   .head(10))
    venue_stats["Short"] = venue_stats["venue"].str.split(",").str[0]

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    axes[0].barh(venue_stats["Short"][::-1], venue_stats["Matches"][::-1], color="#3A225D", edgecolor="white")
    axes[0].set_title("Top Venues by Matches Hosted", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Total Matches")

    axes[1].barh(venue_stats["Short"][::-1], venue_stats["Avg_Score"][::-1], color="#FDB913", edgecolor="white")
    axes[1].set_title("Average 1st Innings Score by Venue", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Avg Runs")

    plt.suptitle("🏟 Venue Analysis — IPL 2008–2025", fontsize=15, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{VIZ}/07_venue_analysis.png", bbox_inches="tight")
    plt.close()
    print("  ✅ 07_venue_analysis.png")

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("\n🏏 IPL Data Analysis — 18 Seasons (2008–2025)")
    print("=" * 50)
    print("\n📊 Generating visualizations...")
    batsmen = plot_top_batsmen()
    bowlers = plot_top_bowlers()
    teams   = plot_team_performance()
    plot_season_stats()
    champs  = plot_champions()
    plot_mom()
    plot_venues()

    print("\n📋 Summary Stats:")
    print(f"  Total Matches Analysed : {len(matches):,}")
    print(f"  Total Deliveries       : {len(deliveries):,}")
    print(f"  Seasons Covered        : 2008 – 2025  (18 seasons)")
    print(f"  Most Titles            : {champs['Champion'].value_counts().idxmax()} ({champs['Champion'].value_counts().max()} titles)")
    print(f"  Top Run Scorer         : {batsmen.iloc[0]['batsman']} ({batsmen.iloc[0]['Total_Runs']:,} runs)")
    print(f"  Top Wicket Taker       : {bowlers.iloc[0]['bowler']} ({int(bowlers.iloc[0]['Wickets'])} wickets)")
    print(f"  Best Win%              : {teams.iloc[0]['team']} ({teams.iloc[0]['win_pct']}%)")
    print("\n✅ All charts saved to /visualizations/")
