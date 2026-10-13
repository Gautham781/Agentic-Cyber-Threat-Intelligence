from agents import (
    vt_agent,
    abuse_agent,
    mitre_agent,
    analyst_agent
)


def run_agent(agent, prompt):
    response = agent.invoke({
        "messages": [("user", prompt)]
    })

    for message in response["messages"]:
        if message.type == "tool":
            return message.content

    return response["messages"][-1].content



def investigate_ip(ip, behavior=None):
    vt_result = run_agent(
        vt_agent,
        f"Check IP {ip} using VirusTotal. Return raw statistics: Malicious, Suspicious, Harmless, Undetected."
    )

    abuse_result = run_agent(
        abuse_agent,
        f"Check IP {ip} using AbuseIPDB. Return raw fields: Abuse Confidence Score, Total Reports, Country, ISP, Domain."
    )

    if behavior:
        mitre_result = run_agent(
            mitre_agent,
            f"Map only explicitly observed behavior to MITRE ATT&CK. Do not guess.\nBehavior: {behavior}"
        )
    else:
        mitre_result = "No MITRE ATT&CK technique identified from the provided evidence."

    analyst_prompt = f"""
You are a CTI analyst.
Based on the evidence, briefly explain whether the IP appears malicious
and assign an overall risk: LOW, MEDIUM, or HIGH.
Keep the interpretation concise and factual.

VirusTotal:
{vt_result}

AbuseIPDB:
{abuse_result}

MITRE ATT&CK:
{mitre_result}
"""

    interpretation = run_agent(analyst_agent, analyst_prompt)

    report = {
        "ip": ip,
        "virustotal": vt_result,
        "abuseipdb": abuse_result,
        "mitre": mitre_result,
        "interpretation": interpretation
    }

    print("\n========== FINAL CTI REPORT ==========")
    for section, content in report.items():
        print(f"\n{section.upper()}\n{content}")

    return report
