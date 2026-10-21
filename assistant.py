from data import get_top, positions, regulars_p
from squad import Squad
from dotenv import load_dotenv
import anthropic

load_dotenv()                  
client = anthropic.Anthropic() 

def build_context():
    text = ""
    for pos in positions.values():
        for i in get_top(pos, 5):
            text += f"name: {i['name']}, team: {i['team']}, value: {i['value']}, price: {i['price']:.1f}m, position: {i['position']}, score: {i['score']}, form: {i['form']}, goals: {i['goals_scored']}, fpl points: {i['points']}, starts_frac: {i['starts_frac']}, assists: {i['assists']}\n"
    return text

def ask_q(question):
    context = build_context()
    prompt = f""" You are an fpl genius assistant, here's the data:

    {context}

    answer questions using only this data

    question: {question}"""

    response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=8000,
    messages=[{"role": "user", "content": prompt}])

    for block in response.content:
        if block.type == "text":
            return block.text
    return f"No answer came back (stop reason: {response.stop_reason})"


def squad_context(squad):
    text = ""
    for i in squad.picks:
        text += f"name: {i['name']}, team: {i['team']}, value: {i['value']}, price: {i['price']:.1f}, position: {i['position']}, score: {i['score']}, form: {i['form']}, goals: {i['goals_scored']}, fpl points: {i['points']}, starts_frac: {i['starts_frac']}, assists: {i['assists']}\n "
    text += f"Remaining budget: £{squad.budget:.1f}m\n"
    return text

def ask_squad(squad, question):
    context = squad_context(squad)
    prompt = f""" Here is the user's FPL squad, which is already legal. Do not suggest changes that break the rules.

    context: {context}

    This squad was picked by taking players in order of score (form × starts fraction), subject to FPL rules: 2 GK, 
    5 DEF, 5 MID, 3 FWD, a £100m budget, and a maximum of 3 players per club.
    
    Answer the question about this squad, Answer using only this data.
    
    question: {question}"""

    response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=8000,
    messages=[{"role": "user", "content": prompt}])

    for block in response.content:
        if block.type == "text":
            return block.text
    return f"No answer came back (stop reason: {response.stop_reason})"
