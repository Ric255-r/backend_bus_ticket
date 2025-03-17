from datetime import timedelta
from fastapi import FastAPI, Security, HTTPException
from fastapi_jwt import (
  JwtAccessBearerCookie,
  JwtAuthorizationCredentials,
  JwtRefreshBearer
)

import os
var = os.getenv('python_backend_bushub') # mw di restart dlu laptop kalo baru declare env di windows
# print(var)

#Cek AccessToken dari header
access_security = JwtAccessBearerCookie(
  secret_key=str(var),
  auto_error=False,
  access_expires_delta=timedelta(hours=1)
)

refresh_security = JwtRefreshBearer(
  secret_key=str(var),
  auto_error=True # Otomatis raise HTTPException 401.
)