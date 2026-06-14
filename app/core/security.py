from datetime import timedelta

from fastapi_jwt import JwtAccessBearerCookie, JwtRefreshBearer

from app.core.config import JWT_SECRET_KEY


access_security = JwtAccessBearerCookie(
    secret_key=JWT_SECRET_KEY,
    auto_error=False,
    access_expires_delta=timedelta(hours=1),
)

refresh_security = JwtRefreshBearer(
    secret_key=JWT_SECRET_KEY,
    auto_error=True,
)
