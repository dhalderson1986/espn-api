from espn_api.basketball import League

# --- CONFIGURATION ---
LEAGUE_ID = 829595564       # Replace with your League ID
YEAR = 2025                # Current Season Year
ESPN_S2 = 'AECofcTSjYEWYyEmuqr3825b90SJcLmTvOnaabYsrR4tz6TKGtTzQOsktXETU2veNWUeis1TpdOgfOjxaks4QK%2B%2FitcZl3KkmrUsxT0DF2e5lniizxrdFT9UVuar%2B1rPj0RVYGlOV%2BAvzB09pjFlNvYIw%2BvpldSJNithFBa6x9kgc0M1tEYbyliAUHa%2F1agrJesZgOYv0GFgwTfkgx69vK8TYum2lLIEmmReNyccimYqX0tYHY9K7QIWLtfuPeXNoSu8wp5MSv5UOBr71u%2FqvseiNVtZbeYF9qGXW1KDoR5Z9g%3D%3D'   # From browser cookies
SWID = '{E1863CA9-CB83-11D3-820B-00A0C9E58E2D}'       # From browser cookies (include curly braces)

def main():
    try:
        print(f"Connecting to League ID: {LEAGUE_ID}...")
        
        # Initialize the League
        league = League(
            league_id=LEAGUE_ID, 
            year=YEAR, 
            espn_s2=ESPN_S2, 
            swid=SWID
        )
        
        print(f"Successfully connected to: {league.settings.name}")
        print("-" * 30)

        # distinct verification step: list teams
        for team in league.teams:
            print(f"{team.team_name} (Record: {team.wins}-{team.losses})")

    except Exception as e:
        print(f"Connection failed: {e}")
        print("Double-check your SWID (including brackets) and ESPN_S2 values.")

if __name__ == "__main__":
    main()