"""Resource Agent Module.

Responsible for curating and providing learning resources for each subject.
Gathers URLs for videos, notes, interactive courses, and other learning materials.
"""

from typing import Dict, List
from pydantic import BaseModel, Field
from urllib.parse import urlencode


class ResourceLink(BaseModel):
    """Represents a single learning resource.
    
    Attributes:
        title: Title or description of the resource
        url: URL to the resource
        resource_type: Type of resource (video, notes, course, etc.)
    """
    title: str = Field(..., min_length=1, max_length=200)
    url: str = Field(..., min_length=10)
    resource_type: str = Field(..., description="Type of learning resource")


class SubjectResources(BaseModel):
    """Collection of resources for a specific subject.
    
    Attributes:
        subject: Name of the subject
        youtube_search: URL for YouTube course search
        pdf_search: URL for PDF notes search
        freecodecamp: URL for FreeCodeCamp learning path
        description: Brief description of available resources
    """
    subject: str = Field(..., min_length=1, max_length=100)
    youtube_search: str = Field(..., min_length=10)
    pdf_search: str = Field(..., min_length=10)
    freecodecamp: str = Field(..., min_length=10)
    description: str = Field(default="", max_length=500)


class ResourceAgent:
    """Agent responsible for curating learning resources.
    
    This agent gathers relevant learning resources for each subject,
    including video courses, study notes, and interactive platforms.
    """

    # Base URLs for resource platforms
    YOUTUBE_BASE = "https://www.youtube.com/results"
    GOOGLE_BASE = "https://www.google.com/search"
    FREECODECAMP_BASE = "https://www.freecodecamp.org/learn/"

    @staticmethod
    def generate_resources(subjects: List[str]) -> Dict[str, SubjectResources]:
        """Generate curated resources for each subject.
        
        Creates resource links for video courses, study notes, and
        interactive learning platforms for each subject.
        
        Args:
            subjects: List of subject names
            
        Returns:
            Dictionary mapping subject names to their resources
            
        Raises:
            ValueError: If subjects list is empty
        """
        if not subjects:
            raise ValueError("At least one subject is required")

        resources_dict = {}

        for subject in subjects:
            if not subject or not isinstance(subject, str):
                continue

            resources_dict[subject] = ResourceAgent._create_subject_resources(subject)

        return resources_dict

    @staticmethod
    def _create_subject_resources(subject: str) -> SubjectResources:
        """Create resource links for a specific subject.
        
        Args:
            subject: Subject name
            
        Returns:
            SubjectResources object with curated links
        """
        # Generate YouTube course search URL
        youtube_url = ResourceAgent._build_youtube_search_url(subject)
        
        # Generate PDF notes search URL
        pdf_url = ResourceAgent._build_pdf_search_url(subject)
        
        # FreeCodeCamp main learning path
        freecodecamp_url = ResourceAgent.FREECODECAMP_BASE

        return SubjectResources(
            subject=subject,
            youtube_search=youtube_url,
            pdf_search=pdf_url,
            freecodecamp=freecodecamp_url,
            description=f"Learning resources for {subject}"
        )

    @staticmethod
    def _build_youtube_search_url(subject: str) -> str:
        """Build a YouTube search URL for the given subject.
        
        Args:
            subject: Subject to search
            
        Returns:
            Complete YouTube search URL
        """
        query = f"{subject} course"
        params = urlencode({"search_query": query})
        return f"{ResourceAgent.YOUTUBE_BASE}?{params}"

    @staticmethod
    def _build_pdf_search_url(subject: str) -> str:
        """Build a Google search URL for PDF notes.
        
        Args:
            subject: Subject to search
            
        Returns:
            Complete Google search URL for PDFs
        """
        query = f"{subject} notes pdf"
        params = urlencode({"q": query})
        return f"{ResourceAgent.GOOGLE_BASE}?{params}"


# Public API for backward compatibility
def generate_resources(subjects: List[str]) -> Dict[str, SubjectResources]:
    """Generate resources for subjects (public API).
    
    This function maintains backward compatibility with the existing API.
    
    Args:
        subjects: List of subject names
        
    Returns:
        Dictionary of resources indexed by subject
    """
    return ResourceAgent.generate_resources(subjects)
