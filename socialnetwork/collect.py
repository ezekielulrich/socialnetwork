import instaloader
import time
from random import uniform

try:
    from . import utils
except ImportError:
    import utils


def collect(username, password):
    L = instaloader.Instaloader(
        quiet=True,
    )

    try:
        L.load_session_from_file(
            username=username, filename="socialnetwork/session_file"
        )
    except:
        login(L, username, password)

    profile = instaloader.Profile.from_username(L.context, "zkeulr")
    followers = get_followers(profile)

    try:
        analyzed_data = utils.load_connections().copy()
    except:
        analyzed_data = {}
    common = {}

    try:
        i = 1
        for username in followers:
            if username in analyzed_data.keys():
                continue

            print(f"Analyzing {username}: {i}/{len(followers) - len(analyzed_data)}")

            follower = instaloader.Profile.from_username(L.context, username)
            subfollowers = get_followers(follower)
            common_followers = list(set(followers).intersection(set(subfollowers)))
            common[username] = common_followers
            utils.save_connections(common)

            if i == 5:
                now = time.time()
                wait = uniform(5, 15) * 60 * 60
                future = now + wait
                future_str = time.strftime("%H:%M:%S", time.localtime(future))
                print("Halting program to avoid lockout")
                print(f"Run again after {future_str} to resume")
                break

            i += 1
    except KeyboardInterrupt:
        print("Program paused")
        print(f"The last follower added was {username}")
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"The last follower added was {username}")
    finally:
        utils.save_connections(common)
        print("Followers saved")


def login(L, username, password):
    try:
        L.login(username, password)
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        two_factor_code = input("Enter 2FA code sent to your device: ")
        L.two_factor_login(two_factor_code)
    except instaloader.exceptions.BadCredentialsException:
        utils.collect_cookies()
        L.login(username, password)

    L.save_session_to_file(filename="vars/session_file")


def get_followers(profile):
    return [follower.username for follower in profile.get_followers()]


if __name__ == "__main__":
    collect(
        input("Enter your Instagram username: "),
        input("Enter your Instagram password: "),
    )
