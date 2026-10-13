# Agentic CTI: Multi-Agent Cyber Threat Intelligence System

## Overview

Agentic CTI is a lightweight multi-agent Cyber Threat Intelligence (CTI) system that investigates an IP address using multiple threat-intelligence sources and produces a concise risk assessment.

The system combines:

- **VirusTotal** — IP reputation and detection statistics
- **AbuseIPDB** — abuse confidence and reporting information
- **MITRE ATT&CK** — mapping of explicitly observed attacker behavior to ATT&CK techniques
- **Qwen2.5 7B via Ollama** — local LLM used by the specialist agents and final CTI analyst

The project demonstrates how agentic AI can coordinate specialized investigation tasks instead of relying on a single LLM response.

## Architecture

```text
                    IP Address
                        |
                  Orchestrator
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
   VirusTotal Agent  AbuseIPDB Agent  MITRE Agent
          |             |             |
          +-------------+-------------+
                        |
                  Evidence Fusion
                        |
                 Analyst Agent
                        |
                        v
                 Final CTI Report
```

### Agent responsibilities

| Agent | Responsibility |
|---|---|
| VirusTotal Agent | Investigates IP reputation and detection statistics |
| AbuseIPDB Agent | Investigates abuse confidence and reporting information |
| MITRE Agent | Maps explicitly supplied attacker behavior to ATT&CK |
| Analyst Agent | Correlates collected evidence and assigns an overall risk |

The specialist agents are intentionally separated by domain so that each agent has a narrow, explainable responsibility.

## Why use agents?

Traditional automation can call APIs sequentially, but an agent can be given a role, access to a tool, and instructions for deciding how to use that tool.

In this project, the LLM agents are responsible for domain-specific investigation behavior, while deterministic Python code and APIs provide the factual evidence. This separation reduces the chance of an LLM rewriting raw security data.

## Tech Stack

- Python
- LangChain
- LangGraph/LangChain agent framework
- Ollama
- Qwen2.5 7B
- VirusTotal API
- AbuseIPDB API
- MITRE ATT&CK concepts
- python-dotenv
- Requests
- vt-py
- BeautifulSoup

## Project Structure

```text
cti-agent/
├── agents.py
├── tools.py
├── mitre_tool.py
├── orchestrator.py
├── agent.py
├── test_vt.py
├── test_abipdb.py
├── test_mitre.py
├── test_agents.py
├── test_llm.py
├── .gitignore
└── .env
```

`.env` contains API keys and is excluded from Git using `.gitignore`.

## Workflow

1. User enters an IP address.
2. The orchestrator invokes the VirusTotal specialist.
3. The orchestrator invokes the AbuseIPDB specialist.
4. Optional observed attacker behavior can be supplied to the MITRE specialist.
5. The collected evidence is passed to the analyst agent.
6. The analyst produces a short interpretation and overall risk rating.
7. Python prints the final report using a fixed structure.

## Example

### Benign IP

```text
VIRUSTOTAL
Malicious: 0
Suspicious: 0
Harmless: 53
Undetected: 39

ABUSEIPDB
Abuse Confidence Score: 0
Total Reports: 234
Country: US
ISP: Google LLC
Domain: google.com

MITRE ATT&CK
No MITRE ATT&CK technique identified from the provided evidence.

INTERPRETATION
The IP does not show significant malicious indicators. Overall risk: LOW.
```

### Suspicious IP

Example test IOC:

```text
185.220.101.47
```

Observed results during development included:

```text
VirusTotal:
Malicious: 16
Suspicious: 2

AbuseIPDB:
Abuse Confidence Score: 100
Total Reports: 237
```

The system classified the overall risk as HIGH.

## MITRE ATT&CK Handling

An IP address by itself does not identify an ATT&CK technique. Therefore, the MITRE agent does not infer TTPs from reputation data.

When explicit behavior is supplied, the agent maps that behavior to ATT&CK.

Example:

```text
Observed behavior:
The attacker used PowerShell to execute commands.

Result:
T1059.001 — PowerShell
```

This prevents unsupported technique hallucination.

## Installation

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install langchain langgraph python-dotenv requests langchain-ollama vt-py mitreattack-python beautifulsoup4
```

Install and run Ollama, then pull the model:

```powershell
ollama pull qwen2.5:7b
```

Create `.env`:

```text
VIRUSTOTAL_API_KEY=your_virustotal_key
ABUSEIPDB_API_KEY=your_abuseipdb_key
```

Never commit `.env`.

## Running

From the VS Code terminal:

```powershell
python orchestrator.py
```

Enter an IP address when prompted.

The system can also accept optional observed attacker behavior for MITRE mapping.

## Testing

Test the tools independently:

```powershell
python test_vt.py
python test_abipdb.py
python test_mitre.py
```

Test specialist agents:

```powershell
python test_agents.py
```

Test the complete workflow:

```powershell
python orchestrator.py
```

## Limitations

- The current MITRE implementation is a lightweight mapping prototype rather than a complete ATT&CK database integration.
- MITRE techniques are mapped only when explicit behavior is supplied.
- The analyst output is generated by a local 7B LLM and may vary slightly in wording.
- API results are live and can change over time.
- The system is an educational CTI prototype, not a production SOC platform.

## Future Improvements

- Replace the local MITRE keyword mapping with the official ATT&CK STIX dataset.
- Add domain and file-hash investigation.
- Add richer VirusTotal and AbuseIPDB evidence.
- Add confidence scoring and evidence provenance.
- Allow agents to dynamically decide which additional tools to call.
- Add persistent investigation history and audit logs.
- Add a web UI for analysts.
- Add automated report export.

## Security

API keys must remain in `.env` and must never be committed to GitHub.

The project uses external threat-intelligence APIs only for investigation. It does not execute malware or connect to suspicious infrastructure.

## License

Add a license appropriate for your intended GitHub use.
=======
# Agentic-Cyber-Threat-Intelligence
Cyber Threat Intelligence using a multi-agent AI Framework for IOC investigation, MITRE ATT&amp;CK mapping and risk assessment

23c8e0416e974010de979dd1454008e8b8962a04
