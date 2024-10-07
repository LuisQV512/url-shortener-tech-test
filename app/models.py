from pydantic import BaseModel, AnyHttpUrl

class ShortenRequest(BaseModel):
    url: AnyHttpUrl  # Ensures the input is a valid HTTP/HTTPS URL
