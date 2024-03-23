import scratchattach as scratch3
from dotenv import load_dotenv, find_dotenv
from time import sleep
from datetime import datetime
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
    URL = f"https://auth-api.itinerary.eu.org/auth/getTokens?redirect=aHR0cHM6Ly9zY3JhdGNoLm1pdC5lZHUv&method=profile-comment&username={User}"
    res = get(URL).json()
    PubCode = res["publicCode"]
    PrivCode = res["privateCode"]
    return ( PubCode, PrivCode )

def CommentThenCheckThenDel(PubCode: str, PrivCode: str) -> bool:
    profile.toggle_commenting()
    CommentHTML = profile.post_comment(PubCode)
    CommentSoup = BeautifulSoup(CommentHTML, "html.parser")
    CommentId = CommentSoup.select_one("[data-comment-id]").get("data-comment-id")

    Verified = False
    URL = "https://auth-api.itinerary.eu.org/auth/verifyToken/" + PrivCode
    res = get(URL).json()
    Verified = res["valid"]
    
    sleep(3)

    profile.delete_comment(comment_id=CommentId)
    profile.toggle_commenting()
    return Verified

while True:
    PubCode, PrivCode = GetSAuthCode()
    Verified = CommentThenCheckThenDel(PubCode, PrivCode)
    Now = datetime.now().strftime("%Y %b %d %H:%M:%S.%f") + " -- "
    if Verified:
        print(Now + "I was able to authenticate")
    else:
        print(Now + "I was not able to authenticate")
    sleep(SleepTime)
