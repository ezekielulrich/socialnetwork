from dotenv import load_dotenv
from tqdm import tqdm
import instaloader
import json
import logging
import os

logging.getLogger("instaloader").setLevel(logging.WARNING)


def main():

    load_dotenv()

    L = instaloader.Instaloader()

    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    try:
        L.load_session_from_file(username=username, filename="session_file")
    except:
        login(L, username, password)

    profile = instaloader.Profile.from_username(L.context, "zkeulr")
    followers = get_followers(profile)

    common = {}
    for username in tqdm(followers, desc="Connecting followers", total=len(followers)):
        follower = instaloader.Profile.from_username(L.context, username)
        subfollowers = get_followers(follower)
        common_followers = set(followers).intersection(set(subfollowers))
        common[follower] = common_followers

    save(common)


def login(L, username, password):
    try:
        L.login(username, password)
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        two_factor_code = input("Enter 2FA code sent to your device: ")
        L.two_factor_login(two_factor_code)

    L.save_session_to_file(filename="session_file")


def get_followers(profile):
    return [follower.username for follower in profile.get_followers()]


def save(dict, filename="connections.json"):
    with open(filename, "w") as f:
        json.dump(dict, f)


if __name__ == "__main__":
    main()
