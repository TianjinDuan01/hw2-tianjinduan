# Report: Customer Support Response Drafting

## Business Use Case

Customer support agents at e-commerce companies handle a high volume of repetitive messages — order delays, return requests, wrong items, and complaints. Drafting individual replies is time-consuming and inconsistent across agents. This prototype uses an LLM to generate a first-pass draft for each incoming customer message, which an agent reviews and sends. The goal is to reduce response time and improve consistency, not to remove the human from the loop.

## Model Choice

I used Gemini 2.5 Flash via the Google Generative AI API. I chose it because it was already available in my environment and offered a good balance of speed and quality for short-form text generation. I did not test other models directly, but based on the task — generating structured, professional short replies — a faster, smaller model like Flash is appropriate. A larger model would likely produce more nuanced output, but the added cost and latency is hard to justify for a drafting assist tool at this scale.

## Baseline vs. Final Design

The initial prompt gave the model a role, a tone, and a few guardrails. Outputs were polite and safe but vague — responses acknowledged the issue and apologized without offering a clear next step or telling the customer what information was needed.

Revision 1 added two explicit rules: acknowledge the specific issue in the opening sentence, and always include a concrete next step. This produced a noticeable improvement. For the order delay case, the model stated that support would investigate the shipment rather than just apologizing. Responses were more actionable and generally felt more balanced.

Revision 2 banned generic filler phrases and restructured the next-step rule into two explicit patterns. Responses became shorter and tighter, but the ban on filler sometimes removed the apology as well, making replies feel less empathetic. The tradeoff was real: more concise, but occasionally less complete than Revision 1.

Based on those results, Revision 1 was the better final version for this prototype. It was not perfect, but it gave a better balance between clarity, empathy, and safety than Revision 2.

## Where the Prototype Still Fails

The prototype handles safety escalation and ambiguous inputs better than the baseline, but it still struggles in a few areas. First, for normal cases like returns, wrong items, or defective products, the model can become too cautious and produce replies that are safe but not fully helpful. Second, it does not always respond strongly enough to urgency, such as when a customer needs a replacement quickly. Third, the balance between conciseness and empathy is still inconsistent. In Revision 2 especially, some replies became shorter but also less complete and less warm.

## Deployment Recommendation

I would not recommend deploying this as an autonomous reply system. The outputs are useful as drafts that reduce agent workload, but the model is still inconsistent on edge cases and can be either too cautious or too minimal depending on the prompt version. A reasonable deployment model would be: present the draft to the agent before sending, require agent approval for every message, and route any case flagged for escalation directly to a human queue without surfacing a draft at all. Under those conditions, this prototype is a reasonable starting point.
