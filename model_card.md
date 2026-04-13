# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**YourJams**

---

## 2. Intended Use  

This system recommends up to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It assumes each user has a single, stable taste profile so it's best fit as a project meant for learning at the moment. Eventually, it could be scaled for more users to use.

---

## 3. How the Model Works  

Each song is labeled with a genre, a mood, and an energy level (0 = very calm, 1 = very intense). The user also provides those three preferences. The system then gives each song a score: genre match earns the most points, mood match earns a bit less, and energy earns points based on how close the song's energy is to what the user asked for. Songs are ranked by total score and the top 5 are returned.

---

## 4. Data  

The catalog has 18 songs in `data/songs.csv`. Genres include lofi, pop, rock, ambient, jazz, hip-hop, classical, country, r&b, metal, reggae, funk, synthwave, and blues. Moods range from chill and happy to intense, sad, angry, and romantic. No songs were added or removed. The catalog skews heavily toward Western genres and leaves out many global styles (e.g., bossa nova, K-pop, Afrobeats).

---

## 5. Strengths  

The system works best when a user's genre and mood both appear in the catalog. When those match, the energy score cleanly separates strong matches from weak ones. It is fully transparent, every score can be traced back to the three weighted components, which makes it easy to understand why a song ranked where it did.

---

## 6. Limitations and Bias 

**Unknown genres create a silent failure.** When a user's preferred genre does not exist in the catalog (e.g., "bossa nova"), the genre weight contributes zero to every song's score. 

**Energy proximity creates a mid-energy filter bubble.** Because the energy score is `1 - |song - target|`, users who want moderate energy (~0.40–0.60) always receive high scores for a large cluster of mid-range songs, regardless of genre or mood. In my experiment, switching to `energy=0.5` caused lofi, country, and blues songs to all land in the top 5 with nearly identical scores, even though they sound nothing alike. 

**Conflicting preferences are not handled — the system just picks the lesser mismatch.** The "Angry Crier" profile (`blues/sad/energy=0.9`) exposed this clearly. The only blues/sad song in the catalog (3am Confession) has energy=0.33, not 0.9. The system still recommends it #1 because categorical matches outweigh the energy gap. When the energy weight was doubled, high-energy rock and pop songs with *no* categorical match started closing in on the score, meaning the ranking becomes unstable for profiles with internal contradictions.

**Genre weight reduction amplifies cross-genre leakage.** After halving genre's weight from 2.0 to 1.0, Storm Runner (rock) jumped from #3 to #2 for a "High-Energy Pop" user, and Spacewalk Thoughts (ambient) moved ahead of a lofi song for a "Chill Lofi" user. A lower genre weight means the system is easier to "trick" into recommending songs from the wrong category if they are close in energy.

**The catalog is too small to distinguish similar moods.** Moods like `chill`, `relaxed`, and `peaceful` feel similar to a human listener but are treated as completely different labels by the scorer. A user searching for `peaceful` will score `chill` and `relaxed` songs at zero for the mood component, even though those songs would likely satisfy them in practice.

---

## 7. Evaluation  

Six user profiles were tested: three standard (High-Energy Pop, Chill Lofi, Deep Intense Rock) and three adversarial edge cases (Angry Crier, Unknown Genre, Middle of the Road). For each, the top 5 results were inspected to check whether they matched intuition and where the scoring broke down.

**Standard profiles, what worked:**  
The system worked best when the catalog had multiple songs matching both genre and mood. The Chill Lofi profile returned two near-perfect scores (4.47 and 4.46), showing the system can distinguish close matches. Deep Intense Rock hit a perfect 4.50 on Storm Runner, the only song in the catalog that matched all three features exactly. The large score gap to #2 (2.48) is a good sign since it means the system correctly signals that the second result is a much weaker match.

**The weight shift experiment, what surprised me:**  
Halving genre from 2.0 to 1.0 and doubling energy to 2.0 caused Storm Runner (rock) to jump to #2 for a High-Energy Pop user with a score of 3.48. This was unexpected since genre feels like the most fundamental preference. Yet, the math showed a nearly-matching energy score can compensate for the wrong genre entirely. This means the original weights were doing more work than they appeared to, and that small weight changes can flip rankings in non-obvious ways.

**Adversarial profiles — what failed:**  
The Angry Crier profile (blues/sad but energy=0.9) made clear a conflict the system cannot resolve. It picks the only blues/sad song correctly at #1, but that song has energy=0.33 far from the 0.9 target and the system never flags this tension. The Unknown Genre profile (bossa nova) showed  degradation: genre contributed zero points for every song, yet the output looked confident with no warning. The Middle of the Road profile (energy=0.5) confirmed the mid-energy filter bubble songs from unrelated genres clustered within 0.04 of each other in score, making the ranking feel arbitrary.

**Profile pair comparisons:**

*High-Energy Pop vs. Deep Intense Rock:* Both want high energy and an intense mood, the only difference is genre. In the original weights, this difference was important. Rock got Storm Runner at 4.50 while Pop got Gym Hero at 4.47. But after the weight shift, Storm Runner appeared in the Pop top 5 at #2. 

*Chill Lofi vs. Middle of the Road:* The Lofi user got two strong matches near the top of the list. The Middle of the Road user (ambient/peaceful/energy=0.5) got no song above 2.78 — because "peaceful" and "ambient" never appear together in the catalog. This comparison shows how a user with a niche combination of preferences is penalized by a small catalog, while a user whose preferences happen to be well represented (lofi + chill) gets much better results. In other words, the system is not equally useful to all users.

*Angry Crier vs. Unknown Genre:* Both profiles are "broken" in different ways. The Angry Crier has conflicting preferences that exist in the catalog but not together. The Unknown Genre has preferences that simply don't exist. Interestingly, the Angry Crier still gets a reasonable #1 result (3.93) because genre and mood match even if energy doesn't. The Unknown Genre user's best score is only 2.42 — and that top result only won because of a mood match, not genre. A user who doesn't know their preferred genre isn't in the catalog would have no idea the system was failing them.

---

## 8. Future Work  

- Add more songs and genres to reduce catalog gaps, especially for niche or global styles.
- Show a warning when no genre or mood match is found instead of silently falling back.
- Support multiple preferred moods or genres so users with mixed tastes aren't penalized.
- Use song similarity (tempo, valence, acousticness) as a tiebreaker to improve diversity in the top results.

---

## 9. Personal Reflection  

Building this system showed me that even simple rules can produce surprisingly reasonable results, but also broken ones. The most unexpected discovery was how much the genre weight was holding the rankings together: one small change flipped the order in ways that felt off but were still entirely valid. This project made me think differently about apps like Spotify, and made me more aware of the importance of machine learning.
