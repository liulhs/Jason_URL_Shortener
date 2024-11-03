from fastapi import FastAPI, HTTPException, Request, APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel, HttpUrl
from datetime import datetime, timedelta
import uuid
import redis

# Initialize the FastAPI app
app = FastAPI()

# Initialize Redis client (make sure Redis is running on your machine)
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Model for URL data
class URLRequest(BaseModel):
    long_url: HttpUrl
    expiration_minutes: int = 1440  # Default expiration is 1 day

# Helper function to generate a unique short code
def generate_short_code():
    return str(uuid.uuid4())[:8]  # Creates an 8-character unique ID

# Initialize an APIRouter with the /url prefix
router = APIRouter(prefix="/url")

# Endpoint to shorten a URL
@router.post("/shorten")
async def shorten_url(url_request: URLRequest):
    # Generate short code
    short_code = generate_short_code()
    expiration_time = datetime.utcnow() + timedelta(minutes=url_request.expiration_minutes)
    
    # Store the short URL in Redis with expiration time
    redis_client.hset(short_code, mapping={
        "long_url": str(url_request.long_url),  # Convert URL to string
        "expiration_time": expiration_time.isoformat()  # Ensure datetime is a string
    })
    redis_client.expireat(short_code, int(expiration_time.timestamp()))

    # Use HTTPS with your custom domain name for the short URL
    return {"short_url": f"https://www.jasonurl.com/url/{short_code}"}

# Endpoint to redirect to the original URL
@router.get("/{short_code}")
async def redirect_url(short_code: str, request: Request):
    # Retrieve the URL data from Redis
    url_data = redis_client.hgetall(short_code)

    # Check if the URL data exists; if not, redirect to expired page
    if not url_data:
        return RedirectResponse(url="https://www.jasonurl.com/expired")

    # Use RedirectResponse to redirect to the original URL
    return RedirectResponse(url=url_data["long_url"])

# Include the router with the /url prefix in the FastAPI app
app.include_router(router)

@router.get("/check-expiration/{short_code}")
async def check_expiration(short_code: str):
    # Retrieve the URL data from Redis
    url_data = redis_client.hgetall(short_code)

    if not url_data:
        raise HTTPException(status_code=404, detail="URL not found or expired")

    # Parse the expiration time and return it
    expiration_time = url_data.get("expiration_time")
    if expiration_time:
        expiration_datetime = datetime.fromisoformat(expiration_time)
        return JSONResponse(content={"expiration_time": expiration_datetime.isoformat()})
    else:
        raise HTTPException(status_code=404, detail="Expiration time not found.")
