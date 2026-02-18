def remediate(ticket):
    issue = ticket["issue"].lower()
    source = ticket["source"]

    if "disk space" in issue:
        print(f" --> Clearing temp files on {source}...")
        # Simulated: subprocess.run(["docker", "exec", source, "rm", "-rf", "/tmp/*"])
        print(f" --> Freed 500MB on {source}")
        return True
        
    elif "apache" in issue or "service down" in issue:
        print(f" --> Restarting service on {source}...")
        # Simulated: subprocess.run(["docker", "restart", source])
        print(f" --> Service restarted on {source}")
        return True
        
    elif "high cpu" in issue:
        print(f" --> Killing high-CPU processes on {source}...")
        # Simulated fix
        print(f" --> Reduced CPU to 45%")
        return True
        
    else:
        # Unknown issue - needs human
        return False