import json
import re
from pathlib import Path
from urllib.parse import quote


def load_sources():
    path = Path("job_sources.json")

    if not path.exists():
        raise FileNotFoundError("job_sources.json was not found.")

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def build_search_url(source_name, query):
    encoded_query = quote(query)

    if source_name == "LinkedIn":
        return f"https://www.google.com/search?q=site%3Alinkedin.com%2Fjobs%2F+{encoded_query}"

    if source_name == "Indeed":
        return f"https://www.google.com/search?q=site%3Aindeed.com%2Fviewjob+{encoded_query}"

    if source_name == "Naukri":
        return f"https://www.google.com/search?q=site%3Anaukri.com%2Fjob-listings+{encoded_query}"

    if source_name == "CSRBOX":
        return f"https://www.google.com/search?q=site%3Acsrbox.org+{encoded_query}"

    if source_name == "DevNet":
        return f"https://www.google.com/search?q=site%3Adevnetjobsindia.org+{encoded_query}"

    if source_name == "Government":
        return f"https://www.google.com/search?q={encoded_query}"

    return f"https://www.google.com/search?q={encoded_query}"


def generate_searches():
    configuration = load_sources()

    searches = []

    for source in configuration["sources"]:
        if not source.get("enabled", True):
            continue

        source_name = source["name"]

        for query in source["queries"]:
            searches.append(
                {
                    "source": source_name,
                    "query": query,
                    "search_url": build_search_url(source_name, query)
                }
            )

    return searches


def save_search_plan(searches):
    output = Path("job_search_plan.md")

    lines = [
        "# Job Search Plan",
        "",
        "The following searches will be performed for the weekly job search.",
        ""
    ]

    current_source = None

    for search in searches:
        if search["source"] != current_source:
            current_source = search["source"]
            lines.append(f"## {current_source}")
            lines.append("")

        lines.append(
            f"- **{search['query']}**  \n"
            f"  {search['search_url']}"
        )

    output.write_text("\n".join(lines), encoding="utf-8")


def main():
    print("Building job search plan...")

    searches = generate_searches()

    print(f"Generated {len(searches)} searches.")

    save_search_plan(searches)

    print("Job search plan created successfully.")


if __name__ == "__main__":
    main()
