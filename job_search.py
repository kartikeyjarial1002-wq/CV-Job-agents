import json
import os
from pathlib import Path

import requests


TAVILY_API_URL = "https://api.tavily.com/search"


def load_sources():
    path = Path("job_sources.json")

    if not path.exists():
        raise FileNotFoundError(
            "job_sources.json was not found."
        )

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def search_tavily(query, max_results=5):
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise RuntimeError(
            "TAVILY_API_KEY environment variable was not found."
        )

    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "max_results": max_results,
        "include_answer": False
    }

    response = requests.post(
        TAVILY_API_URL,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    return response.json()


def collect_jobs():
    configuration = load_sources()

    all_results = []

    for source in configuration["sources"]:

        if not source.get("enabled", True):
            continue

        source_name = source["name"]

        for query in source["queries"]:

            print(
                f"Searching {source_name}: {query}"
            )

            search_query = query

            data = search_tavily(
                search_query,
                max_results=5
            )

            results = data.get("results", [])

            for result in results:

                all_results.append(
                    {
                        "source": source_name,
                        "query": query,
                        "title": result.get(
                            "title",
                            ""
                        ),
                        "url": result.get(
                            "url",
                            ""
                        ),
                        "content": result.get(
                            "content",
                            ""
                        ),
                        "score": result.get(
                            "score",
                            0
                        )
                    }
                )

    return all_results


def remove_duplicates(results):

    unique = {}

    for result in results:

        url = result.get("url", "").strip()

        if not url:
            continue

        if url not in unique:
            unique[url] = result

    return list(unique.values())


def save_results(results):

    output = Path("job_results.json")

    with open(
        output,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False
        )


def create_report(results):

    output = Path("job_search_results.md")

    lines = [
        "# Job Search Results",
        "",
        f"Total unique results: **{len(results)}**",
        "",
    ]

    for index, result in enumerate(
        results,
        start=1
    ):

        lines.append(
            f"## {index}. {result['title']}"
        )

        lines.append("")

        lines.append(
            f"**Source:** {result['source']}"
        )

        lines.append("")

        lines.append(
            f"**Search query:** {result['query']}"
        )

        lines.append("")

        lines.append(
            f"**URL:** {result['url']}"
        )

        lines.append("")

        lines.append(
            f"**Search relevance score:** "
            f"{result['score']}"
        )

        lines.append("")

        lines.append(
            "**Description / Search snippet:**"
        )

        lines.append("")

        lines.append(
            result["content"]
        )

        lines.append("")

        lines.append("---")

        lines.append("")

    output.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )


def main():

    print("Starting live job search...")

    results = collect_jobs()

    print(
        f"Collected {len(results)} raw results."
    )

    results = remove_duplicates(results)

    print(
        f"After removing duplicates: "
        f"{len(results)} results."
    )

    save_results(results)

    create_report(results)

    print(
        "Job search results saved successfully."
    )


if __name__ == "__main__":
    main()
