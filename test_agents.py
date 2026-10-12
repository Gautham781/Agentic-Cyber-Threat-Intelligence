from agents import vt_agent, abuse_agent, mitre_agent


def run_agent(agent, prompt):
    response = agent.invoke({
        "messages": [("user", prompt)]
    })

    return response["messages"][-1].content


print("\n===== VIRUSTOTAL AGENT =====")
print(
    run_agent(
        vt_agent,
        "Investigate the IP address 8.8.8.8 using VirusTotal. "
        "Return only the factual results from the tool."
    )
)


print("\n===== ABUSEIPDB AGENT =====")
print(
    run_agent(
        abuse_agent,
        "Investigate the IP address 8.8.8.8 using AbuseIPDB. "
        "Return only the factual results from the tool."
    )
)


print("\n===== MITRE AGENT =====")
print(
    run_agent(
        mitre_agent,
        "No specific attacker behavior has been identified. "
        "Do not infer or guess a MITRE ATT&CK technique."
    )
)