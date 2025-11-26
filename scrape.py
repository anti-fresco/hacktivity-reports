import requests
import sys

def fetch_hackerone_report(report_id):
    url = f"https://hackerone.com/reports/{report_id}.json"
    resp = requests.get(url)
    resp.raise_for_status()
    report = resp.json()

    data = {
        "report_id": report.get("id"),
        "title": report.get("title"),
        "severity": None,
        "reported_by": report.get("reporter", {}).get("username"),

        "reported_to": report.get("team", {})
                           .get("profile", {})
                           .get("name"),

        "reported_on": report.get("created_at"),
        "disclosed_on": report.get("disclosed_at"),
        "bounty": report.get("formatted_bounty"),
        "weakness_name": report.get("weakness", {}).get("name")
    }

    severity_info = report.get("severity", {})
    if severity_info:
        data["severity"] = {
            "rating": severity_info.get("rating"),
            "score": severity_info.get("score"),
        }

    return data


if __name__ == "__main__":
    # Expect: script.py <report_id> <partial|full>
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} <report_id> <partial|full>")
        sys.exit(1)

    report_id = sys.argv[1]
    disclosure_mode = sys.argv[2].lower()

    # Validate second argument
    if disclosure_mode not in ["partial", "full"]:
        print("Error: Disclosure must be either 'partial' or 'full'")
        sys.exit(1)

    # Format it nicely for output
    disclosure_formatted = disclosure_mode.capitalize()

    report_data = fetch_hackerone_report(report_id)

    # ---- Format fields ----
    title = report_data.get("title")
    rid = report_data.get("report_id")
    bounty = report_data.get("bounty")
    reported_by = report_data.get("reported_by")
    reported_to = report_data.get("reported_to")
    weakness_name = report_data.get("weakness_name", "None")

    # Format severity
    severity = report_data.get("severity")
    if severity and severity.get("rating"):
        severity_formatted = severity.get("rating").capitalize()
    else:
        severity_formatted = "None"

    # Extract dates only (YYYY-MM-DD)
    reported_on = report_data.get("reported_on")
    disclosed_on = report_data.get("disclosed_on")

    if reported_on:
        reported_on = reported_on.split("T")[0]
    if disclosed_on:
        disclosed_on = disclosed_on.split("T")[0]

    # ---- Markdown Output ----
    print(f"""### {title}
- Disclosure: {disclosure_formatted}
- Link: https://hackerone.com/reports/{rid}
### Details
- Severity: {severity_formatted}
- Weakness: {weakness_name}
- Bounty: {bounty}
- Reported by: {reported_by}
- Reported to: {reported_to}
### Timeline
- Reported on: {reported_on}
- Disclosed on: {disclosed_on}
----
""")


