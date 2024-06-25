from bot import Bot
import argparse
import os.path


def get_relations(bot, username, followers, filename="relations.txt"):
    if os.path.isfile("start_profile.txt"):
        start_profile = get_start_profile()
        print(f"Start scraping at profile {start_profile}")
    else:
        start_profile = 1
        with open("start_profile.txt", "w+") as outfile:
            outfile.write("1")

    bot.get_followers(followers, start_profile, filename)


def get_start_profile():
    with open("start_profile.txt") as f:
        return int(f.readline())


def write_followers(followers, filename="followers.txt"):
    with open(filename, "w+") as f:
        for follower in followers:
            f.write(follower + "\n")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--username", type=str)
    parser.add_argument("--password", type=str)

    config = parser.parse_args()

    b = Bot()
    b.setUp()

    b.login(config.username, config.password)

    followers = list(b.get_my_followers(config.username))
    write_followers(followers)

    # get_relations(b, config.username, followers)
    
    b.tear_down()
