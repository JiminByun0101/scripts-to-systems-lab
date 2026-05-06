import argparse
import json
import sys
from llm import call_claude

VALID_LABELS = ("bug", "enhancement", "chore")

PROMPT_TEMPLATE = """You are a PR triage assistant for a payment backend service.
Given the PR title, description, and diff, respond with JSON only — no explanation, no markdown.

Respond with:
{{"label": "bug|enhancement|chore", "summary": "one sentence, plain English, what this PR does"}}

PR title: {title}
PR description: {body}
Diff (truncated at 6000 chars):
{diff}"""

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--title", required=True)
  parser.add_argument("--body", required="")
  parser.add_argument("--diff", required=True)
  args = parser.parse_args()

  prompt = PROMPT_TEMPLATE.format(
    title=args.title,
    body=args.body,
    diff=args.diff,
  )

  response = call_claude(prompt)

  try:
    result = json.loads(response)
  except json.JSONDecodeError:
    print(f"ERROR: Claude returned invalid JSON: {response}", file=sys.stderr)
    sys.exit(1)

  label = result.get("label")
  if label not in VALID_LABELS:
    print(f"ERROR: unexpected label: {label}", file=sys.stderr)
    sys.exit(1)

  print(f"label={label}")
  print(f"summary={result.get('summary', '')}")

if __name__ == "__main__" :
  main()