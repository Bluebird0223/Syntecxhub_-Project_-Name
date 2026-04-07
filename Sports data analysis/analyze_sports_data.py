import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set aesthetic style
sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams['figure.figsize'] = (12, 6)

def analyze_data():
    # Use absolute paths relative to the script location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    matches_path = os.path.join(base_dir, 'matches.csv')
    deliveries_path = os.path.join(base_dir, 'deliveries.csv')

    if not os.path.exists(matches_path) or not os.path.exists(deliveries_path):
        print(f"Error: CSV files not found in {base_dir}")
        return

    # Load data
    matches = pd.read_csv(matches_path)
    deliveries = pd.read_csv(deliveries_path)

    print("Data loaded successfully.")

    # 1. Data Cleaning & Mapping
    # Standardizing team names for consistency (rebrands and spelling)
    team_mapping = {
        'Rising Pune Supergiant': 'Rising Pune Supergiants',
        'Delhi Daredevils': 'Delhi Capitals',
        'Deccan Chargers': 'Sunrisers Hyderabad'  # Often grouped in historical analysis
    }
    matches.replace(team_mapping, inplace=True)
    deliveries.replace(team_mapping, inplace=True)

    # 2. Top Scorers
    top_scorers = deliveries.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10)
    
    # 3. Strike Rates (Corrected: Exclude wides from balls faced)
    valid_balls = deliveries[deliveries['wide_runs'] == 0]
    balls_faced = valid_balls.groupby('batsman')['ball'].count()
    runs_scored = deliveries.groupby('batsman')['batsman_runs'].sum()
    strike_rate = (runs_scored / balls_faced * 100).sort_values(ascending=False)
    # Filter for players who faced at least 500 balls for statistically significant values
    top_strike_rates = strike_rate[balls_faced > 500].head(10)

    # 4. Team Win Rates (Corrected: Handle missing teams in win counts)
    all_teams = pd.concat([matches['team1'], matches['team2']])
    match_counts = all_teams.value_counts()
    win_counts = matches['winner'].value_counts()
    win_rate = (win_counts / match_counts * 100).fillna(0).sort_values(ascending=False)

    # 5. Seasonal Performance for Top 5 Players
    top_5_batsmen = top_scorers.head(5).index.tolist()
    merged_data = pd.merge(deliveries, matches[['id', 'season']], left_on='match_id', right_on='id')
    seasonal_runs = merged_data[merged_data['batsman'].isin(top_5_batsmen)].groupby(['season', 'batsman'])['batsman_runs'].sum().unstack()

    # 6. Additional Metric: Player of the Match
    top_mom = matches['player_of_match'].value_counts().head(10)

    # 7. Additional Metric: Most Matches hosted by Venue
    top_venues = matches['venue'].value_counts().head(10)

    # --- Visualizations ---
    visuals_dir = os.path.join(base_dir, 'visuals')
    os.makedirs(visuals_dir, exist_ok=True)

    # Plot 1: Top 10 Scorers
    plt.figure()
    sns.barplot(x=top_scorers.values, y=top_scorers.index, hue=top_scorers.index, palette='viridis', legend=False)
    plt.title('Top 10 IPL Scorers (2008-2019)')
    plt.xlabel('Total Runs')
    plt.savefig(os.path.join(visuals_dir, 'top_scorers.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # Plot 2: Team Win Rates
    plt.figure()
    sns.barplot(x=win_rate.values, y=win_rate.index, hue=win_rate.index, palette='magma', legend=False)
    plt.title('Overall Team Win Rates (%)')
    plt.xlabel('Win Rate (%)')
    plt.savefig(os.path.join(visuals_dir, 'team_win_rates.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # Plot 3: Player Performance across Seasons (Top 5)
    plt.figure()
    seasonal_runs.plot(marker='o', linewidth=2)
    plt.title('Performance of Top 5 Scorers Across Seasons')
    plt.ylabel('Runs per Season')
    plt.xlabel('Season')
    plt.legend(title='Player', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(visuals_dir, 'player_trends.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # Plot 4: Top Strike Rates
    plt.figure()
    sns.barplot(x=top_strike_rates.values, y=top_strike_rates.index, hue=top_strike_rates.index, palette='plasma', legend=False)
    plt.title('Top 10 Strike Rates (Min. 500 legal balls faced)')
    plt.xlabel('Strike Rate')
    plt.savefig(os.path.join(visuals_dir, 'strike_rates.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # Plot 5: Player of the Match Awards
    plt.figure()
    sns.barplot(x=top_mom.values, y=top_mom.index, hue=top_mom.index, palette='coolwarm', legend=False)
    plt.title('Top 10 Player of the Match Recipients')
    plt.xlabel('Number of Awards')
    plt.savefig(os.path.join(visuals_dir, 'mom_awards.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # Export Insights
    insights_path = os.path.join(base_dir, 'insights.md')
    with open(insights_path, 'w') as f:
        f.write("# IPL Sports Data Analysis Insights (2008-2019)\n\n")
        f.write("## 1. Top Scorers\n")
        f.write(f"The top-performing batsman in this period is **{top_scorers.index[0]}** with **{int(top_scorers.values[0])}** runs.\n\n")
        f.write("## 2. Team Efficiency\n")
        f.write(f"**{win_rate.index[0]}** holds the highest win rate at **{win_rate.values[0]:.2f}%**.\n\n")
        f.write("## 3. Strike Rate Leader\n")
        f.write(f"Among consistent players (min 500 legal balls), **{top_strike_rates.index[0]}** leads with a strike rate of **{top_strike_rates.values[0]:.2f}**.\n\n")
        f.write("## 4. Most Impactful Player\n")
        f.write(f"**{top_mom.index[0]}** has received the most Player of the Match awards (**{top_mom.values[0]}**).\n\n")
        f.write("## 5. Most Popular Venue\n")
        f.write(f"The most matches were played at **{top_venues.index[0]}** with **{top_venues.values[0]}** matches.\n\n")
        f.write("> [!NOTE]\n")
        f.write("> Data limitations: The `deliveries.csv` file has missing records for some matches between 2014-2019, which may affect historical cumulative totals.\n")

    print(f"Analysis complete. Visuals and insights generated in: {base_dir}")

if __name__ == "__main__":
    analyze_data()
