from pathlib import Path
from datetime import datetime


def find_cv():
    cv_files = list(Path(".").glob("*.pdf")) + list(Path(".").glob("*.docx"))

    if not cv_files:
        raise FileNotFoundError("No CV file found in the repository.")

    return cv_files[0]


def read_preferences():
    path = Path("job_preferences.txt")

    if not path.exists():
        raise FileNotFoundError("job_preferences.txt was not found.")

    return path.read_text(encoding="utf-8")


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

        document = Document(str(cv_path))

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    return ""


def create_initial_report(cv_path, cv_text, preferences):
    today = datetime.now().strftime("%d %B %Y")

    report = f"""# Weekly Job Search Report

**Generated:** {today}

## Candidate Profile

CV detected: `{cv_path.name}`

CV text successfully extracted: **Yes**

## Job Preferences

{preferences}

## Current Status

The job-search system is successfully reading:

- Your CV
- Your job preferences

### Search Sources

The job-search system is configured to search for relevant opportunities from:

- LinkedIn
- Indeed
- Naukri
- CSRBOX
- DevNet
- Government job portals and government websites

### Next Stage

The job-search system will:

1. Search multiple job sources.
2. Collect relevant vacancies.
3. Remove duplicate listings.
4. Compare each vacancy with your CV.
5. Match jobs against your preferred roles.
6. Check location and remote/hybrid suitability.
7. Consider salary information when available.
8. Produce a relevance-based report.
9. Run automatically every week.

**Initial setup test completed successfully.**
"""

    Path("weekly_jobs.md").write_text(
        report,
        encoding="utf-8"
    )


def main():
    print("Starting job agent...")

    # Step 1: Find CV
    cv_path = find_cv()
    print(f"CV found: {cv_path}")

    # Step 2: Read job preferences
    preferences = read_preferences()
    print("Job preferences found.")

    # Step 3: Extract CV text
    cv_text = extract_cv_text(cv_path)

    if not cv_text.strip():
        raise ValueError(
            "CV was found, but no readable text could be extracted."
        )

    print("CV text extracted successfully.")

    # Step 4: Create initial report
    create_initial_report(
        cv_path,
        cv_text,
        preferences
    )

    # Step 5: Generate job-search plan
    from job_search import generate_searches, save_search_plan

    searches = generate_searches()

    save_search_plan(searches)

    print(
        f"Generated {len(searches)} job searches."
    )

    print(
        "Job search plan created successfully."
    )

    print(
        "Job agent test completed successfully."
    )


if __name__ == "__main__":
    main()
