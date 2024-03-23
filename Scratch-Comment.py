import scratchattach as scratch3
from dotenv import load_dotenv, find_dotenv
from time import sleep
from base64 import b64decode
from requests import get
from bs4 import BeautifulSoup
import os

load_dotenv(find_dotenv())


User = os.environ.get("user")
Pass = os.environ.get("pass")

SleepTime = int(os.environ.get("intermission"))

session = scratch3.login(User, Pass)
profile = session.connect_user(User)

def GetSAuthCode():
    try:
        URL = f"https://auth-api.itinerary.eu.org/auth/getTokens?method=profile-comment&username={User}"
        res = get(URL).json()
        PubCode = res["publicCode"]
        PrivCode = res["privateCode"]
        return ( PubCode, PrivCode )
    except:
        return None

def CommentThenCheckThenDel(PubCode: str, PrivCode: str) -> bool:
    try:
        profile.toggle_commenting()
        CommentHTML = profile.post_comment(PubCode)
        CommentSoup = BeautifulSoup(CommentHTML, "html.parser")
        CommentId = CommentSoup.css.select("[data-comment-id]").get("data-comment-id")
        
        Verified = False
        try:
            URL = "https://auth-api.itinerary.eu.org/auth/verifyToken/" + PrivCode
            res = get(URL).json()
            Verified = res["valid"]
        except:
            pass

        profile.delete_comment(CommentId)
        profile.toggle_commenting()
        return Verified
    except:
        return False

while True:
    PubCode, PrivCode = GetSAuthCode()
    Verified = CommentThenCheckThenDel(PubCode, PrivCode)
    print(Verified)
    sleep(SleepTime)
