# HW2: GenAI Workflow

## Workflow: Customer Support Response Drafting

**Chosen workflow:** Drafting responses to customer support emails for an e-commerce company.

**Who the user is:** A customer support agent who handles a high volume of incoming customer messages and needs to respond quickly and consistently.

**Input:** A raw customer email or message — for example, a complaint about a delayed order, a return request, or a question about a product.

**Output:** A drafted reply email that is professional, empathetic, and appropriate to the customer's situation. The agent reviews and sends it, or edits it before sending.

**Why automate this:** Support agents spend a significant portion of their day writing responses that follow similar patterns. An LLM can draft a first-pass response in seconds, reducing response time and letting agents focus on edge cases that genuinely need human judgment.

---

## Project Files

| File | Description |
|------|-------------|
| `app.py` | Main script. Loads eval cases, calls the Gemini API, and saves drafted responses to a markdown file. |
| `eval_set.json` | Evaluation set with 7 test cases: normal, edge, and failure-prone. |
| `prompts.md` | Three prompt versions (initial, revision 1, revision 2) with notes on what changed and why. |
| `report.md` | Written report covering model choice, prompt iteration, failure analysis, and deployment recommendation. |

---

## How to Run

1. Install dependencies:
   ```bash
   python3 -m pip install google-genai python-dotenv
   ```

2. Create a `.env` file in the project folder:
   ```
   GEMINI_API_KEY=your_key_here
   ```

3. Run the app:
   ```bash
   python3 app.py
   ```

Results are saved to `output.md` by default. To run a single case:
```bash
python3 app.py --case case_01
```

---

## Video Walkthrough

[Unlisted YouTube Video](https://youtu.be/YG15xjmzK0c)

