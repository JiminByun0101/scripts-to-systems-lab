import anthropic
import os

def call_claude(prompt: str, max_tokens: int=256) -> str:
  client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
  message = client.message.create(
    model="claude-sonnet-4-6",
    max_tokens=max_tokens,
    messages=[{"role": "user", "content": prompt}],
  )
  return message.content[0].text