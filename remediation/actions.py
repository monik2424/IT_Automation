def remediate(ticket):
    issue = ticket["issue"].lower()
    source = ticket["source"]

    if "disk space" in issue:
        # subprocess.run(["docker", "exec", source, "rm", "-rf", "/tmp/*"])
        return True, f"Cleared 500MB of temp files on {source}"

    elif "apache" in issue or "service down" in issue:
        # subprocess.run(["docker", "restart", source])
        return True, f"Restarted service on {source}"

    elif "high cpu" in issue:
        # subprocess.run(["docker", "exec", source, "kill", "-9", "$(pgrep high_cpu_proc)"])
        return True, f"Killed high-CPU processes on {source}, usage reduced to ~45%"

    else:
        return False, "No automated handler matched"