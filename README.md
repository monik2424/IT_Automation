# Auto-Ops: Intelligent IT Ticket Resolution System

A Python-based IT automation platform that simulates a real enterprise IT Operations Center. It automatically detects system alerts, resolves common issues without human intervention, and uses AI to diagnose problems it cannot fix on its own — all visible on a live dashboard.

---

## What It Does

Imagine you are an IT manager responsible for 3 servers. Problems happen constantly — disks fill up, services crash, CPU spikes. Normally a technician has to manually read each alert, figure out what is wrong, and fix it.

This system automates that entire workflow:

1. **Alerts come in** — a script generates random IT problems (high CPU, disk full, Apache down, VPN timeout) every 10–30 seconds and logs them as tickets
2. **Agent reads the tickets** — every 15 seconds, the remediation agent scans for open tickets
3. **Known problems are auto-fixed** — disk full? Cleared. Apache down? Restarted. CPU spike? Processes killed. Ticket marked resolved automatically.
4. **Unknown problems get AI-diagnosed** — if the agent cannot fix it (e.g. VPN timeout), it sends the ticket to OpenAI GPT-4o-mini, which reads your IT knowledge base and returns a category, likely cause, recommended action, and confidence level
5. **Everything is logged** — every action is timestamped and saved to `auto_ops.log`
6. **Dashboard shows it all live** — a Streamlit dashboard displays system health, automation rate, and every ticket in real time

---

## Architecture

```
alert_generator.py
      │
      │  POST /tickets  (creates alert as a ticket)
      ▼
  FastAPI  ─────────────────────────────────────────┐
  api/main.py                                       │
  (in-memory ticket store)                          │
      │                                             │
      │  GET /tickets  (agent polls every 15s)      │  PATCH /tickets/{id}
      ▼                                             │  (agent updates status)
  remediation/agent.py  ───────────────────────────┘
      │
      ├── Issue recognised? ──► actions.py  ──► auto-fix  ──► status: resolved ✅
      │
      └── Issue unknown?   ──► triage/bot.py (OpenAI GPT-4o-mini)
                                    │
                              knowledge.txt (SOP manual)
                                    │
                              AI diagnosis attached ──► status: needs_human 🔴

  dashboard/app.py  ──►  polls API every 5s  ──►  live stats + ticket feed
```

---

## Project Structure

```
IT_Automation/
├── api/
│   ├── main.py              # FastAPI server — create, read, and update tickets
│   ├── alert_generator.py   # Generates random IT alerts every 10–30 seconds
│   └── requirements.txt     # Python dependencies
├── remediation/
│   ├── agent.py             # Polls API, auto-fixes tickets, calls AI triage
│   └── actions.py           # Fix logic for disk, CPU, and service issues
├── triage/
│   ├── bot.py               # Sends unresolvable tickets to OpenAI for diagnosis
│   └── knowledge.txt        # IT Standard Operating Procedures knowledge base
├── dashboard/
│   └── app.py               # Live Streamlit operations dashboard
├── start.sh                 # One command to launch all 4 services
└── .env                     # Your API keys (never committed to git)
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/IT_Automation.git
cd IT_Automation
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn pydantic requests openai streamlit python-dotenv
```

### 4. Add your OpenAI API key

Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-your-actual-key-here
```

Get your key at [platform.openai.com](https://platform.openai.com/api-keys)

---

## Running the Project

### One command (recommended)

```bash
chmod +x start.sh    # only needed the first time
./start.sh
```

Starts all 4 services at once. Press `Ctrl+C` to stop everything cleanly.

### Or manually in 4 separate terminals

```bash
# Terminal 1 — API server
uvicorn api.main:app --reload

# Terminal 2 — Alert generator
python api/alert_generator.py

# Terminal 3 — Remediation agent
python remediation/agent.py

# Terminal 4 — Dashboard
streamlit run dashboard/app.py
```

---

## URLs

| Service | URL |
|---|---|
| Dashboard | http://localhost:8501 |
| API | http://localhost:8000 |
| API Interactive Docs | http://localhost:8000/docs |

---

## Example Log Output (`auto_ops.log`)

```
[2026-02-24 21:33] INFO: Processing Ticket #1: Disk space critical (95% full) on Server-A
[2026-02-24 21:33] INFO: Auto-resolved Ticket #1: Cleared 500MB of temp files on Server-A
[2026-02-24 21:33] INFO: Processing Ticket #2: High CPU usage (98%) on Server-B
[2026-02-24 21:33] INFO: Auto-resolved Ticket #2: Killed high-CPU processes on Server-B, usage reduced to ~45%
[2026-02-24 21:33] INFO: Processing Ticket #3: VPN connection timeout on VPN-Gateway
[2026-02-24 21:33] WARNING: Escalated Ticket #3 with AI triage — VPN connection timeout
Category: Network
Likely Cause: Expired VPN certificate or misconfigured client settings.
Recommended Action: Check VPN gateway logs. Verify SSL certificate expiry date. Confirm firewall allows UDP 1194.
Confidence: High
```

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| FastAPI | REST API for ticket management |
| OpenAI GPT-4o-mini | AI triage for unresolvable tickets |
| Streamlit | Live operations dashboard |
| python-dotenv | Secure environment variable loading |
