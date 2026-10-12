TECHNIQUES = {
    "powershell": ("T1059.001", "PowerShell"),
    "command and scripting interpreter": ("T1059", "Command and Scripting Interpreter"),
    "phishing": ("T1566", "Phishing"),
    "process injection": ("T1055", "Process Injection"),
    "credential dumping": ("T1003", "OS Credential Dumping"),
    "persistence": ("T1547", "Boot or Logon Autostart Execution"),
}


def search_mitre(behavior: str) -> str:
    """Map observed attacker behavior to MITRE ATT&CK."""

    behavior = behavior.lower()

    matches = []

    for keyword, (tech_id, name) in TECHNIQUES.items():
        if keyword in behavior:
            matches.append(f"{tech_id} — {name}")

    if not matches:
        return "No MITRE ATT&CK technique identified from the provided evidence."

    return "\n".join(matches)