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

    # 1. VirusTotal Agent
    vt_result = run_agent(
        vt_agent,
        f"""
        Check the IP address {ip} using VirusTotal.

        Return ONLY these raw statistics:
        - Malicious
        - Suspicious
        - Harmless
        - Undetected

        Do not interpret the results.
        Do not explain what they mean.
        """
    )

    # 2. AbuseIPDB Agent
    abuse_result = run_agent(
        abuse_agent,
        f"""
        Check the IP address {ip} using AbuseIPDB.

        Return ONLY these raw fields:
        - Abuse Confidence Score
        - Total Reports
        - Country
        - ISP
        - Domain

        Do not interpret the results.
        Do not explain what they mean.
        """
    )

        # 3. MITRE ATT&CK Agent
    if behavior:
        mitre_result = run_agent(
            mitre_agent,
            f"""
            Map the following observed attacker behavior to MITRE ATT&CK:

            {behavior}

            Only identify techniques explicitly supported by the behavior.
            Do not guess or infer additional techniques.
            Return the technique ID and name.
            """
        )
    else:
        mitre_result = "No MITRE ATT&CK technique identified from the provided evidence."

    # 4. Final Analyst Agent
    analyst_prompt = f"""
You are a CTI analyst.

Based on the evidence below, briefly explain:
1. Whether the IP appears malicious or not, and why.
2. The overall risk: LOW, MEDIUM, or HIGH.

Keep the interpretation concise and factual.

VirusTotal:
{vt_result}

AbuseIPDB:
{abuse_result}

MITRE ATT&CK:
{mitre_result}
"""

    interpretation = run_agent(
        analyst_agent,
        analyst_prompt
    )

    # 5. Build the final report using Python
    print("\n========== FINAL CTI REPORT ==========")

    print("\nVIRUSTOTAL")
    print(vt_result)

    print("\nABUSEIPDB")
    print(abuse_result)

    print("\nMITRE ATT&CK")
    print(mitre_result)

    print("\nINTERPRETATION")
    print(interpretation)


if __name__ == "__main__":
    ip = input("Enter IP address to investigate: ")
    behavior = input("Enter observed attacker behavior (or press Enter if none): ")

    investigate_ip(
        ip,
        behavior if behavior.strip() else None
    )