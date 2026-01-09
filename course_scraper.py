import requests
from bs4 import BeautifulSoup
import re


def scrape_courses(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    course_divs = soup.select("div.divTable")

    courses = []

    for div in course_divs:
        cells = div.select("div.divTableCell")
        if not cells:
            continue

        course = {}

        # First bold strong — contains code + components + credits
        header = cells[0].get_text(strip=True)
        match = re.match(r"(CS \d{3})\s+(.+?)\s+([0-9]\.[0-9]+)$", header)
        if not match:
            continue

        course["code"] = match.group(1)
        course["components"] = match.group(2).replace(",", " ").split()
        course["credits"] = float(match.group(3))

        # Course ID
        id_cell = div.select_one(".crseid")
        if id_cell:
            id_match = re.search(r"Course ID:\s*(\d+)", id_cell.text)
            if id_match:
                course["course_id"] = id_match.group(1)

        # Title — second strong
        strong_tags = div.find_all("strong")
        if len(strong_tags) >= 2:
            course["title"] = strong_tags[1].get_text(strip=True)

        # Pull the remaining descriptive info
        description_parts = []
        prereq = None
        antireq = None

        for cell in cells:
            text = cell.get_text(" ", strip=True)

            if text.startswith("Prereq:"):
                prereq = text.replace("Prereq:", "").strip()
            elif text.startswith("Antireq:"):
                antireq = text.replace("Antireq:", "").strip()
            elif (
                    text and
                    not text.startswith("Course ID:") and
                    not text == course.get("title", "") and
                    not re.match(r"^CS \d{3}", text)
            ):
                description_parts.append(text)

        # Join description intelligently
        if description_parts:
            course["description"] = " ".join(description_parts).split("Prereq:")[0].strip()

        if prereq:
            course["prerequisites"] = prereq
        if antireq:
            course["antirequisites"] = antireq

        courses.append(course)

    return courses