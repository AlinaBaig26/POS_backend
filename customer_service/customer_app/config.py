import os
from datetime import timedelta

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")

    # JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = False  # True in prod (HTTPS)
    # JWT_COOKIE_CSRF_PROTECT = True
    # JWT_ACCESS_COOKIE_PATH = "/"
    # JWT_REFRESH_COOKIE_PATH = "/api/auth/refresh"

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=12)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
