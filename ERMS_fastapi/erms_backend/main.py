from fastapi import FastAPI
import logging
from fastapi.security import OAuth2PasswordBearer
from assignment import assignment_router
from project import project_router
from auth import auth_router
from engineer import engineer_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login") 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


API_PREFIX = "/api"
app.include_router(project_router.router, prefix=API_PREFIX)
app.include_router(assignment_router.router, prefix=API_PREFIX)
app.include_router(auth_router.router, prefix=API_PREFIX)
app.include_router(engineer_router.router, prefix=API_PREFIX)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

# Enable CORS for cross-origin requests from FE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], #FE url
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)