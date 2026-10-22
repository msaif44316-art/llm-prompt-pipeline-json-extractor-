
import os
import json
from google import genai
from pydantic import BaseModel, Field


# Define the output structure
class ResumeData(BaseModel):
    name: str = Field(description="Candidate name")
    email: str = Field(description="Email address")
    skills: list[str] = Field(description="Candidate skills")
    education: str = Field(description="Education details")


# Connect to Gemini API
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


# Extract structured data from text
def extract_resume(text):
    prompt = f"""
    Extract information from the resume below.
    Do not invent information.
    Use 'Not provided' for missing fields.

    Resume:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ResumeData,
        },
    )

    # Validate the JSON response
    data = ResumeData.model_validate_json(response.text)

    return data.model_dump()


# Test input
resume_text = """
Name: Rahul Kumar
Email: rahul@example.com
Skills: Python, SQL, Machine Learning
Education: B.E. Computer Science
"""


# Run the program
if __name__ == "__main__":
    try:
        result = extract_resume(resume_text)
        print(json.dumps(result, indent=4))

    except Exception as error:
        print("Error:", error)
