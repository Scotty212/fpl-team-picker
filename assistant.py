from data import get_top, positions
from dotenv import load_dotenv
import anthropic

load_dotenv()                  
client = anthropic.Anthropic() 

def build_context():
    text = ""
    for pos in positions.values():
        for i in get_top(pos, 5):
            text += f"name: {i['name']}, team: {i['team']}, value: {i['value']}, price: {i['price']:.1f}m, position: {i['position']}, score: {i['score']}, form: {i['form']} \n"
    return text

def ask_q(question):
    context = build_context()
    prompt = f""" You are an fpl genius assistant, here's the data:

    {context}

    answer questions using only this data

    question: {question}"""

    response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=500,
    messages=[{"role": "user", "content": prompt}])

    for block in response.content:
        if block.type == "text":
            return block.text
    

    