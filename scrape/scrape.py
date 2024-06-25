from bot import Bot
import argparse
import os.path


def get_relations(bot, username, followers, filename="relations.txt"):
    start_profile = 1

    if os.path.isfile("start_profile.txt"):
        with open("start_profile.txt") as f:
            start_profile = int(f.readline())
        print(f"Started at profile {start_profile}")
    else:
        with open("start_profile.txt", "w+") as f:
            f.write("1")

    bot.get_followers(followers, start_profile, filename)    


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

    get_relations(b, config.username, followers)
    
    b.tear_down()
