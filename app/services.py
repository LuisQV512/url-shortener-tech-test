from fastapi import Request, HTTPException
import redis, random
from .utils import generate_short_url
from redis.exceptions import ConnectionError
# Redis connection setup (Could be refactored into a config if needed)
redis_client = redis.StrictRedis(host="redis", port=6379, db=0, decode_responses=True)


def generate_unique_short_url(original_url: str) -> str:
    """Generate a unique short URL and ensure there are no collisions in Redis."""
    short_url = generate_short_url(original_url).lower()

    # Step 1: Check if the generated short URL already exists and points to a different URL
    while redis_client.exists(short_url):
        existing_original_url = redis_client.get(short_url)
        if existing_original_url == original_url:
            # If the short URL already maps to the same original URL, return it
            return short_url
        
        # Step 2: If there's a collision, regenerate a new short URL
        # Append random characters to resolve the collision
        short_url = generate_short_url(original_url + str(random.randint(0, 9999))).lower()

    return short_url

def shorten_url(original_url: str, req: Request) -> dict:
    """Shortens the URL and returns the shortened URL"""

    # Convert the Pydantic URL object to a string
    original_url_str = str(original_url)


    try:
        # Check if the original URL is already shortened
        existing_short_url = redis_client.get(f"url:{original_url_str}")
        if existing_short_url:
            return {"short_url": f"{req.base_url}r/{existing_short_url.lower()}"}
        
        # Generate a new short URL
        short_url = generate_unique_short_url(original_url_str)

        # Store both mappings (short_url -> original_url, and original_url -> short_url)
        redis_client.set(short_url, original_url_str)
        redis_client.set(f"url:{original_url_str}", short_url)

        return {"short_url": f"{req.base_url}r/{short_url}"}
    
    except ConnectionError:
        # If Redis is down, return a 503 Service Unavailable error
        raise HTTPException(status_code=503, detail="Redis is unavailable. Please try again later.")
 

def resolve_url(short_url: str) -> str:
    """Resolves a shortened URL to its original URL"""
    try:
        original_url = redis_client.get(short_url.lower())
        return original_url  # Return the original URL or None if not found

    except ConnectionError:
        # If Redis is down, raise a 503 error
        raise HTTPException(status_code=503, detail="Redis is unavailable. Please try again later.")