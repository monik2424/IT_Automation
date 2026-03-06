from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def load_knowledge_base():
    kb_path = os.path.join(os.path.dirname(__file__), "knowledge.txt")
    with open(kb_path, "r") as f:
        return f.read()

def triage_ticket(issue: str, source: str) -> str:
    knowledge_base = load_knowledge_base()

    prompt = f"""You are an IT Operations assistant for an enterprise infrastructure team.
    
A ticket has been raised that could not be automatically resolved:
- Issue: {issue}
- Affected system: {source}

Use the following Standard Operating Procedures knowledge base to guide your response:
---
{knowledge_base}
---

Respond in this exact format:
Category: [Network / Hardware / Software / Unknown]
Likely Cause: [one sentence]
Recommended Action: [one to two sentences from the SOP]
Confidence: [High / Medium / Low]"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.2
    )

    return response.choices[0].message.content.strip()