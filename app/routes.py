from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from .models import ShortenRequest
from .services import shorten_url, resolve_url

router = APIRouter()

@router.post("/url/shorten")
async def url_shorten(request: ShortenRequest, req: Request):
    return shorten_url(request.url, req)

@router.get("/r/{short_url}")
async def url_resolve(short_url: str):
    original_url = resolve_url(short_url)
    if original_url:
        return RedirectResponse(original_url)
        #for testing purposes
        #return {"original_url": original_url}
    raise HTTPException(status_code=404, detail="Short URL not found")
