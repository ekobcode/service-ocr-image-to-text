import os

# Maximum allowed file size in megabytes
MAX_FILE_SIZE_MB = 5

# Accepted image MIME types
ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/jpg",
    "image/webp"
}

# API Keys (include env var fallback for local dev)
API_KEYS = list(filter(None, [
    "app_prod_0f8fad5b-d9cb-469f-a165-70867728950e_Y8a2XW",
    "app_dev_1c6c7cbe-bdbb-41d2-a1e0-1cfb10ec93d4_Qz9PpK",
    os.getenv("API_KEY_ENV")  # Only include if present
]))
