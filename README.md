# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real recommendation systems predict what you will like next by matching behavioral datasets with machine learning models that detect patterns in what you, and millions of others, consume. Real‑world recommenders like Spotify and YouTube use two kinds of data: features of the item (such as genre, mood, tempo, or video topic) and features of the user (their watch/listen history, skips, likes, and search behavior). The system first builds a representation of each item from its content features, then builds a representation of the user’s preferences based on the patterns in their past behavior. These inputs feed into a ranking model that scores every possible item and selects the ones the user is most likely to enjoy next. This separates the raw input data (item features and user history) from the learned preference profile (what the model thinks the user likes) and from the final ranking step (choosing which items to show). Two foundational approaches are collaborative-based filtering and content-based filtering, and many real platforms use a hybrid of both. 

### Song Features

Each `Song` is loaded from `data/songs.csv`. Our model uses three features:

- **genre** — categorical label (e.g. `lofi`, `pop`, `rock`, `ambient`)
- **mood** — categorical label (e.g. `chill`, `intense`, `happy`, `focused`)
- **energy** — how intense or active the song feels (0 = very calm, 1 = very intense)

---

### UserProfile

A `UserProfile` stores the user's target preferences as a single snapshot:

- `favorite_genre` — their preferred genre category
- `favorite_mood` — their preferred mood category
- `target_energy` — the energy level they want right now (0–1)

---

### Scoring a Song

For each song, the `Recommender` computes a **total score** as a weighted sum of partial scores:

```
total_score =
  2.0 × genre_match       (1.0 if genre matches, else 0.0)
  1.5 × mood_match        (1.0 if mood matches, else 0.0)
  1.0 × energy_proximity  (1 − |song.energy − user.target_energy|)
```

**Proximity scoring** is used for energy. Rather than rewarding high or low values, it rewards songs whose energy is *closest to the user's target*. A perfect match scores 1.0; the furthest possible value scores 0.0. This prevents the system from always pushing toward extremes (e.g. always recommending the highest-energy songs to someone who wants moderate energy).

---

### Choosing Recommendations

After scoring every song, the `Recommender`:

1. Sorts all songs by `total_score` in descending order
2. Returns the top `k` songs (default `k = 5`)

```
User Profile
    │
    ▼
Score every song  ──►  sort by score  ──►  return top k
```

Genre and mood carry the most weight because they represent the broadest musical identity. Energy refines the ranking within that category.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

