import os
import json
import argparse
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# --- Configurable system prompt ---
SYSTEM_PROMPT = """You are a customer support assistant for an e-commerce company.
Your job is to draft a professional, empathetic reply to a customer message.

Rules:
- Be polite and concise.
- Do not promise specific outcomes (refunds, replacements, timelines) unless you are certain.
- If the issue is unclear, ask for clarification.
- If the issue involves safety or potential liability, flag it for human review.
- Do not invent order details, policies, or inventory information.
- Sign off as: Support Team"""

MODEL = "gemini-2.5-flash"


def load_cases(path="eval_set.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def draft_response(client, customer_message):
    prompt = (
        "Draft a customer support reply to the following message.\n\n"
        f"Customer message:\n{customer_message}"
    )
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.4,
        ),
    )
    return response.text


def save_results(results, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Customer Support Draft Results\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Model: {MODEL}\n\n")
        f.write("---\n\n")
        for r in results:
            f.write(f"## {r['id']} — {r['label']}\n\n")
            f.write(f"**Category:** {r['category']}\n\n")
            f.write(f"**Customer message:**\n\n{r['input']}\n\n")
            f.write(f"**Drafted response:**\n\n{r['draft']}\n\n")
            f.write(f"**Evaluation note:** {r['good_output_should']}\n\n")
            f.write("---\n\n")


def main():
    parser = argparse.ArgumentParser(description="Draft customer support responses using Gemini.")
    parser.add_argument("--output", default="output.md", help="Output file path (default: output.md)")
    parser.add_argument("--case", default=None, help="Run a single case by ID (e.g. case_01)")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set.")
        print("Set it in a .env file or with: export GEMINI_API_KEY=your_key_here")
        return

    client = genai.Client(api_key=api_key)
    cases = load_cases()

    if args.case:
        cases = [c for c in cases if c["id"] == args.case]
        if not cases:
            print(f"Error: No case found with id '{args.case}'")
            return

    results = []
    for case in cases:
        print(f"Running {case['id']} — {case['label']}...")
        try:
            draft = draft_response(client, case["input"])
        except Exception as e:
            draft = f"[Error generating response: {e}]"
            print(f"  Warning: API call failed for {case['id']}: {e}")
        result = {
            "id": case["id"],
            "label": case["label"],
            "category": case["category"],
            "input": case["input"],
            "draft": draft,
            "good_output_should": case["good_output_should"],
        }
        results.append(result)
        print(f"  Done.\n")

    save_results(results, args.output)
    print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()
