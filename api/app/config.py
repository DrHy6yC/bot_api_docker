from os import getenv
from dotenv import load_dotenv

load_dotenv()

clientID = getenv('clientID')
redirect_us_uri = getenv('redirect_us_uri')
