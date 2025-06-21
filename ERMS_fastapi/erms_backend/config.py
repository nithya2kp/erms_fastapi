import dotenv
import os

dotenv.load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
DB_URI = os.getenv("DB_URI")
