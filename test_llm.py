from dotenv import load_dotenv
import anthropic

load_dotenv()                  # reads your .env file
client = anthropic.Anthropic() # finds the key automatically

response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=200,
    messages=[{"role": "user", "content": "Say hello"}]
)

print(response.content[0].text)