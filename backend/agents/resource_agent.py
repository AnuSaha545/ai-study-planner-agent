from typing import Dict
from pydantic import BaseModel


class SubjectResources(BaseModel):
    youtube_search: str
    pdf_search: str
    freecodecamp: str


def generate_resources(subjects) -> Dict[str, SubjectResources]:

    out = {}

    for subject in subjects:
        out[subject] = SubjectResources(
            youtube_search=f"https://www.youtube.com/results?search_query={subject}+course",
            pdf_search=f"https://www.google.com/search?q={subject}+notes+pdf",
            freecodecamp="https://www.freecodecamp.org/learn/",
        )

    return out
