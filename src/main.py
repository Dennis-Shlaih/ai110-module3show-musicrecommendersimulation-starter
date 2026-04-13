"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # "Late Night Focus" user — wants calm lofi with a focused mood
    # and low-moderate energy suitable for studying or deep work
    user_prefs = {
        "genre": "lofi",       # preferred genre category
        "mood": "focused",     # preferred mood category
        "energy": 0.40,        # target energy level (0 = calm, 1 = intense)
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 40)
    print("  Top Recommendations")
    print("=" * 40)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Score: {score:.2f} / 4.50")
        for reason in explanation.split(" | "):
            print(f"    - {reason}")
        print("-" * 40)


if __name__ == "__main__":
    main()
