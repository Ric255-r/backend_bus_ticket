# install uvicorn : pip install uvicorn
# jwt_auth : https://k4black.github.io/fastapi-jwt/

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from router.routeUser import app as app_user
from router.routeTransaction import app as app_transaction
from router.routeAdmin import app as app_admin

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

#Buat Router main
main_router = APIRouter()

#include router2 yang dibuat ke main router
main_router.include_router(app_user)
main_router.include_router(app_transaction)
main_router.include_router(app_admin)

#masukkan main router ke fastapi app
app.include_router(main_router, prefix="/api")

# bawaan default
if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="192.168.1.7", port=5500)


#note for self.
# dalam url, wajib teliti, jgn smpe ada kelebihan slash
# contoh localhost/api/content/ <- url harus sangat teliti