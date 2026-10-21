# FPL Squad Picker ⚽🤖

An AI-assisted Fantasy Premier League tool that builds a legal 15-player squad from **live FPL data**, then lets you ask an AI assistant questions about it, like "Who should I captain?" or "Who's the weak link in my defence?"

**Live app:** (https://fpl-team-picker-6xxtpifjpugvkimaukbklb.streamlit.app/)

---

## What it does

1. **Pulls live data** from the official Fantasy Premier League API (players, clubs, prices, form, minutes)
2. **Scores every player** on current form and how regularly they start
3. **Picks a legal squad** that follows every FPL rule:
   - 2 goalkeepers, 5 defenders, 5 midfielders, 3 forwards
   - £100m budget
   - a maximum of 3 players from any one club
4. **Answers questions about your squad** using Claude (Anthropic's LLM), grounded in the squad's actual data

## How it works

### Scoring

```
score = form × starts_fraction
```

- **form**: FPL's rolling measure of recent points
- **starts_fraction**: games started ÷ gameweeks played so far, so rotation-risk players are penalised

Only "regulars" (players who've started at least 50% of games) are considered.

### Squad picking

The picker goes through players from highest score to lowest and adds each one if they pass every rule: a free slot in their position, enough budget left, and fewer than 3 from their club. This is a **greedy algorithm**. It's fast and always produces a legal squad, though not necessarily the mathematically optimal one.

The rules are enforced by a `Squad` class:

```python
my_squad = Squad()
for player in regulars:
    if my_squad.can_add(player):
        my_squad.add(player)
```

### The AI layer: code for rules, LLM for reasoning

A key design decision: **the LLM never builds the squad.**

During testing, asking the model to "build the best team" produced squads that broke FPL rules (4 players from one club) and had incorrect budget totals. LLMs are probabilistic and weak at strict arithmetic and constraint satisfaction.

So the work is split:
- **Python code** handles anything with hard rules: budget, positions, club limits
- **Claude** handles explanation and advice: captaincy, weak spots, comparisons

The squad's data is formatted as text and passed to Claude with an instruction to answer **using only that data**. This grounding stops it inventing players or stats.

## Project structure

```
data.py           # fetches FPL API data, builds and scores players
squad.py          # Squad class: enforces FPL rules
assistant.py      # builds context from data and queries Claude
streamlit_app.py  # web front end
main.py           # command-line version
```

## Tech

- **Python**
- **FPL API** via `requests`
- **Anthropic API** (Claude)
- **Streamlit** for the front end, deployed on Streamlit Community Cloud

The backend logic (data processing, scoring, the `Squad` class and the LLM integration) is my own code. The Streamlit UI was built with AI assistance.

## Run it locally

```bash
git clone https://github.com/Scotty212/fpl-team-picker.git
cd fpl-team-picker
pip install -r requirements.txt
```

Create a `.env` file with your Anthropic API key:

```
ANTHROPIC_API_KEY=your-key-here
```

Then run:

```bash
streamlit run streamlit_app.py
```

## Limitations and roadmap

The current scoring is deliberately simple and misses a lot:

- [ ] **Better scoring:** add fixture difficulty, expected goals/assists (xG/xA) and injury flags
- [ ] **Tool calling:** let Claude call the app's functions (e.g. "find midfielders under £6m") instead of only seeing the squad
- [ ] **Conversation memory:** send chat history so follow-up questions work
- [ ] **Backtesting:** measure how the picker's squads would have scored over past gameweeks against the average manager
- [ ] **Smarter optimisation:** replace the greedy picker with a proper optimiser
- [ ] **Substitutions** currently unable to add any radnom player, due to the strict restrictions/rules in the code. (i.e. Your favourite midfielder has only started a few games this season so won't be added to the list of *top* players)
