import os
import requests
import vt
from dotenv import load_dotenv

load_dotenv()

VT_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")


def check_virustotal(ip: str) -> str:
    """Check an IP address using VirusTotal."""

    client = vt.Client(VT_API_KEY, timeout=10)

    try:
        ip_info = client.get_object(f"/ip_addresses/{ip}")

        stats = ip_info.last_analysis_stats

        return (
            f"Malicious: {stats.get('malicious', 0)}\n"
            f"Suspicious: {stats.get('suspicious', 0)}\n"
            f"Harmless: {stats.get('harmless', 0)}\n"
            f"Undetected: {stats.get('undetected', 0)}"
        )

    except Exception as e:
        return f"VirusTotal error: {str(e)}"

    finally:
        client.close()


def check_abuseipdb(ip: str) -> str:
    """Check an IP address using AbuseIPDB."""

    url = "https://api.abuseipdb.com/api/v2/check"

    headers = {
        "Key": ABUSEIPDB_API_KEY,
        "Accept": "application/json"
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()["data"]

        return (
            f"Abuse Confidence Score: {data['abuseConfidenceScore']}\n"
            f"Total Reports: {data['totalReports']}\n"
            f"Country: {data['countryCode']}\n"
            f"ISP: {data['isp']}\n"
            f"Domain: {data['domain']}"
        )

    except Exception as e:
        return f"AbuseIPDB error: {str(e)}"