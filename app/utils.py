import hashlib

def generate_short_url(original_url: str) -> str:
    """Generate a short URL key based on a hash of the original URL."""
    hash_object = hashlib.sha256(original_url.encode())
    return hash_object.hexdigest()[:6]  # Use the first 6 characters of the hash
