import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = {
            "genre":  user.favorite_genre,
            "mood":   user.favorite_mood,
            "energy": user.target_energy,
        }
        scored = []
        for song in self.songs:
            song_dict = {
                "genre":  song.genre,
                "mood":   song.mood,
                "energy": song.energy,
            }
            score, _ = score_song(song_dict, user_prefs)
            scored.append((song, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = {
            "genre":  user.favorite_genre,
            "mood":   user.favorite_mood,
            "energy": user.target_energy,
        }
        song_dict = {
            "genre":  song.genre,
            "mood":   song.mood,
            "energy": song.energy,
        }
        _, reasons = score_song(song_dict, user_prefs)
        return " | ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(song: Dict, user_prefs: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against the user's preferences.
    Returns a (score, reasons) tuple where reasons explains each contribution.
    """
    score = 0.0
    reasons = []

    # Genre match: exact category match is worth the most
    if song["genre"] == user_prefs["genre"]:
        score += 2.0
        reasons.append(f"genre match (+2.0)")
    else:
        reasons.append(f"genre mismatch — '{song['genre']}' vs '{user_prefs['genre']}' (+0.0)")

    # Mood match: second strongest signal
    if song["mood"] == user_prefs["mood"]:
        score += 1.5
        reasons.append(f"mood match (+1.5)")
    else:
        reasons.append(f"mood mismatch — '{song['mood']}' vs '{user_prefs['mood']}' (+0.0)")

    # Energy proximity: reward closeness to target, not high or low values
    energy_proximity = 1.0 - abs(song["energy"] - user_prefs["energy"])
    energy_points = round(1.0 * energy_proximity, 2)
    score += energy_points
    reasons.append(f"energy proximity (+{energy_points:.2f}) — song {song['energy']}, target {user_prefs['energy']}")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(song, user_prefs)
        explanation = " | ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
