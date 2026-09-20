from pathlib import Path
from datetime import datetime

from job_search import collect_jobs, remove_duplicates
from job_search import save_results, create_report


def find_cv():
    cv_files = (
        list(Path(".").glob("*.pdf"))
        + list(Path(".").glob("*.docx"))
    )

    if not cv_files:
        raise FileNotFoundError(
            "No CV file found in the repository."
        )

    return cv_files[0]


def read_preferences():
    path = Path("job_preferences.txt")

    if not path.exists():
        raise FileNotFoundError(
            "job_preferences.txt was not found."
        )

    return path.read_text(
        encoding="utf-8"
    )


def extract_cv_text(cv_path):

    if cv_path.suffix.lower() == ".pdf":

        from pypdf import PdfReader

        reader = PdfReader(str(cv_path))

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    elif cv_path.suffix.lower() == ".docx":

        from docx import Document

        document = Document(
            str(cv_path)
        )

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    return ""


def create_initial_report(
    cv_path,
    cv_text,
    preferences
):

    today = datetime.now().strftime(
        "%d %B %Y"
    )

    report = f"""# Weekly Job Search Report

**Generated:** {today}

## Candidate Profile

CV detected: `{cv_path.name}`

CV text successfully extracted: **Yes**

CV characters extracted: **{len(cv_text)}**

## Job Preferences

{preferences}

## Search Status

The agent successfully read:

- Your CV
- Your job preferences

## Live Search

The agent is now searching configured job sources.

Results are being collected and prepared for matching.
"""

    Path(
        "weekly_jobs.md"
    ).write_text(
        report,
        encoding="utf-8"
    )


def main():

    print(
        "Starting job agent..."
    )

    # Find CV
    cv_path = find_cv()

    print(
        f"CV found: {cv_path}"
    )

    # Read preferences
    preferences = read_preferences()

    print(
        "Job preferences found."
    )

    # Extract CV
    cv_text = extract_cv_text(
        cv_path
    )

    if not cv_text.strip():

        raise ValueError(
            "CV was found, but no readable "
            "text could be extracted."
        )

    print(
        "CV text extracted successfully."
    )

    # Create initial report
    create_initial_report(
        cv_path,
        cv_text,
        preferences
    )

    # Perform live job search
    results = collect_jobs()

    print(
        f"Collected {len(results)} raw results."
    )

    # Remove duplicates
    results = remove_duplicates(
        results
    )

    print(
        f"Unique results: {len(results)}"
    )

    # Save raw results
    save_results(results)

    # Create readable report
    create_report(results)

    print(
        "Job search report created successfully."
    )

    print(
        "Job agent completed successfully."
    )


if __name__ == "__main__":
    main()
