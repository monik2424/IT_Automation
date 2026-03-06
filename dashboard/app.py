import streamlit as st
import requests
import time

st.set_page_config(page_title="Auto-Ops Dashboard", layout="wide")

st.title("Auto-Ops: Intelligent IT Ticket Resolution")
st.caption("Live view of automated ticket processing")

# --- Fetch data from API ---
try:
    response = requests.get("http://localhost:8000/tickets", timeout=3)
    tickets = response.json()
except requests.exceptions.ConnectionError:
    st.error("Cannot reach API at localhost:8000 — is uvicorn running?")
    st.stop()

# --- Calculate stats ---
total = len(tickets)
resolved = sum(1 for t in tickets.values() if t["status"] == "resolved")
needs_human = sum(1 for t in tickets.values() if t["status"] == "needs_human")
open_tickets = sum(1 for t in tickets.values() if t["status"] == "open")
automation_rate = int((resolved / total) * 100) if total > 0 else 0

# --- Row 1: Stats ---
st.subheader("Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tickets", total)
col2.metric("Auto-Resolved", resolved)
col3.metric("Needs Human", needs_human)
col4.metric("Automation Rate", f"{automation_rate}%")

st.divider()

# --- Row 2: System Health ---
st.subheader("System Health")

sources = ["Server-A", "Server-B", "VPN-Gateway"]
cols = st.columns(3)

for i, source in enumerate(sources):
    source_tickets = [t for t in tickets.values() if t["source"] == source]
    if not source_tickets:
        status = "No Data"
        color = "gray"
    else:
        last = sorted(source_tickets, key=lambda x: x["id"])[-1]
        if last["status"] == "needs_human":
            status = "Needs Attention"
            color = "red"
        else:
            status = "Healthy"
            color = "green"

    cols[i].markdown(
        f"""
        <div style="padding:20px; border-radius:10px; background-color:{'#1a3a1a' if color == 'green' else '#3a1a1a' if color == 'red' else '#2a2a2a'}; text-align:center;">
            <h3 style="color:{'#00cc44' if color == 'green' else '#ff4444' if color == 'red' else 'gray'}">{source}</h3>
            <p style="color:white; font-size:16px">{status}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# --- Row 3: Live Ticket Feed ---
st.subheader("Live Ticket Feed")

if not tickets:
    st.info("No tickets yet. Start the alert generator to create tickets.")
else:
    for ticket_id, ticket in sorted(tickets.items(), key=lambda x: x[0], reverse=True):
        status = ticket["status"]

        if status == "resolved":
            color = "#1a3a1a"
            badge = "✅ Resolved"
        elif status == "needs_human":
            color = "#3a1a1a"
            badge = "🔴 Needs Human"
        else:
            color = "#2a2a1a"
            badge = "🟡 Open"

        with st.container():
            st.markdown(
                f"""
                <div style="padding:12px 16px; border-radius:8px; background-color:{color}; margin-bottom:8px;">
                    <b style="color:white">Ticket #{ticket_id}</b> &nbsp;|&nbsp;
                    <span style="color:#aaa">{ticket['source']}</span> &nbsp;|&nbsp;
                    {badge}<br/>
                    <span style="color:#ddd">{ticket['issue']}</span><br/>
                    <small style="color:#888">{ticket.get('resolution_note', '') or 'Pending...'}</small>
                </div>
                """,
                unsafe_allow_html=True
            )

st.divider()
st.caption(f"Last refreshed: {time.strftime('%H:%M:%S')} — refreshes every 5 seconds")

# --- Auto-refresh ---
time.sleep(5)
st.rerun()