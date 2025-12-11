import config
import os
from espn_api.basketball import League
import datetime

# Define the output directory
OUTPUT_DIR = "outputs"

def get_league():
    print(f"Connecting to League {config.LEAGUE_ID}...")
    return League(
        league_id=config.LEAGUE_ID,
        year=config.YEAR,
        espn_s2=config.ESPN_S2,
        swid=config.SWID
    )

def create_rosters_md(league):
    """Generates Rosters.md for the AI."""
    filename = os.path.join(OUTPUT_DIR, "Rosters.md")
    print(f"Generating {filename}...")
    
    with open(filename, "w") as f:
        f.write(f"# Rosters (Updated: {datetime.date.today()})\n\n")
        
        for team in league.teams:
            f.write(f"## {team.team_name} (ID: {team.team_id})\n")
            f.write(f"**Record:** {team.wins}-{team.losses}-{team.ties}\n")
            f.write("**Roster:**\n")
            for player in team.roster:
                # Format: Player Name (Position) - ProTeam [Injury Status]
                inj = f"[{player.injuryStatus}]" if player.injuryStatus != 'ACTIVE' else ""
                f.write(f"- {player.name} ({player.position}) - {player.proTeam} {inj}\n")
            f.write("\n---\n\n")

def create_rankings_md(league):
    """Generates Rankings.md for the AI."""
    filename = os.path.join(OUTPUT_DIR, "Rankings.md")
    print(f"Generating {filename}...")
    
    # Sort teams by total wins
    standings = sorted(league.teams, key=lambda x: x.wins, reverse=True)
    
    with open(filename, "w") as f:
        f.write(f"# League Standings (Updated: {datetime.date.today()})\n\n")
        f.write("| Rank | Team Name | W-L-T | Pts For | Pts Against |\n")
        f.write("|---|---|---|---|---|\n")
        
        for i, team in enumerate(standings, 1):
            f.write(f"| {i} | {team.team_name} | {team.wins}-{team.losses}-{team.ties} | {team.points_for} | {team.points_against} |\n")
        
        f.write("\n\n*Note to AI: Use these standings to identify category gaps for the 'Punt 3PM/TO' strategy.*\n")

def main():
    try:
        # Safety check to ensure folder exists
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        league = get_league()
        
        # Only generating Rosters and Rankings as requested
        create_rosters_md(league)
        create_rankings_md(league)
        
        print(f"\nSUCCESS: 'Rosters.md' and 'Rankings.md' saved to '{OUTPUT_DIR}/'.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()