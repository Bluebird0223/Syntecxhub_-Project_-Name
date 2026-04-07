import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set aesthetic style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def analyze_data():
    # Load data
    matches = pd.read_csv('Sports data analysis/matches.csv')
    deliveries = pd.read_csv('Sports data analysis/deliveries.csv')

    print("Data loaded successfully.")

    # 1. Data Cleaning
    # Standardizing team names (some teams changed names)
    team_mapping = {
        'Rising Pune Supergiant': 'Rising Pune Supergiants',
        'Delhi Daredevils': 'Delhi Capitals'
    }
    matches.replace(team_mapping, inplace=True)
    deliveries.replace(team_mapping, inplace=True)

    # 2. Top Scorers
    top_scorers = deliveries.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10)
    
    # 3. Strike Rates
    # Filter for players who faced at least 500 balls to get meaningful strike rates
    balls_faced = deliveries.groupby('batsman')['ball'].count()
    runs_scored = deliveries.groupby('batsman')['batsman_runs'].sum()
    strike_rate = (runs_scored / balls_faced * 100).sort_values(ascending=False)
    top_strike_rates = strike_rate[balls_faced > 500].head(10)

    # 4. Team Win Rates
    total_matches = matches['team1'].value_counts() + matches['team2'].value_counts()
    wins = matches['winner'].value_counts()
    win_rate = (wins / total_matches * 100).sort_values(ascending=False)

    # 5. Seasonal Performance for Top 5 Players
    top_5_batsmen = top_scorers.head(5).index.tolist()
    # Join deliveries with matches to get the season
    merged_data = pd.merge(deliveries, matches[['id', 'season']], left_on='match_id', right_on='id')
    seasonal_runs = merged_data[merged_data['batsman'].isin(top_5_batsmen)].groupby(['season', 'batsman'])['batsman_runs'].sum().unstack()

    # --- Visualizations ---
    os.makedirs('Sports data analysis/visuals', exist_ok=True)

    # Plot 1: Top 10 Scorers
    plt.figure()
    sns.barplot(x=top_scorers.values, y=top_scorers.index, palette='viridis')
    plt.title('Top 10 IPL Scorers (2008-2019)')
    plt.xlabel('Total Runs')
    plt.savefig('Sports data analysis/visuals/top_scorers.png')
    plt.close()

    # Plot 2: Team Win Rates
    plt.figure()
    sns.barplot(x=win_rate.values, y=win_rate.index, palette='magma')
    plt.title('Overall Team Win Rates (%)')
    plt.xlabel('Win Rate (%)')
    plt.savefig('Sports data analysis/visuals/team_win_rates.png')
    plt.close()

    # Plot 3: Player Performance across Seasons (Top 5)
    plt.figure()
    seasonal_runs.plot(marker='o')
    plt.title('Performance of Top 5 Scorers Across Seasons')
    plt.ylabel('Runs per Season')
    plt.xlabel('Season')
    plt.legend(title='Player', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('Sports data analysis/visuals/player_trends.png')
    plt.close()

    # Plot 4: Top Strike Rates
    plt.figure()
    sns.barplot(x=top_strike_rates.values, y=top_strike_rates.index, palette='coolwarm')
    plt.title('Top 10 Strike Rates (Min. 500 balls faced)')
    plt.xlabel('Strike Rate')
    plt.savefig('Sports data analysis/visuals/strike_rates.png')
    plt.close()

    # Export Insights
    with open('Sports data analysis/insights.md', 'w') as f:
        f.write("# IPL Sports Data Analysis Insights\n\n")
        f.write("## 1. Top Scorers\n")
        f.write(f"The top-performing batsman overall is **{top_scorers.index[0]}** with **{top_scorers.values[0]}** runs.\n\n")
        f.write("## 2. Team Efficiency\n")
        f.write(f"**{win_rate.index[0]}** holds the highest win rate at **{win_rate.values[0]:.2f}%**.\n\n")
        f.write("## 3. Strike Rate Leader\n")
        f.write(f"Among consistent players, **{top_strike_rates.index[0]}** leads with a strike rate of **{top_strike_rates.values[0]:.2f}**.\n\n")
        f.write("## 4. Visual Summary\n")
        f.write("Refer to the 'visuals' directory for detailed charts.\n")

    print("Analysis complete. Visuals and insights generated.")

if __name__ == "__main__":
    analyze_data()
