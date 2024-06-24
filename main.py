from scrape.bot import Bot
import argparse
import os.path


def get_relations(bot, followers):
    bot.go_to_page("https://www.instagram.com/accounts/login/")

    my_followers_arr = followers
    if not os.path.isfile(relations_file):
        write_relations(relations_file, my_followers_arr, username)

    if os.path.isfile("start_profile.txt"):
        start_profile = get_start_profile()
        print("Start scraping at profile nr " + str(start_profile))
    else:
        start_profile = 1
        with open("start_profile.txt", "w+") as outfile:
            outfile.write("1")

    bot.get_followers(my_followers_arr, start_profile, relations_file)


def get_start_profile():
    with open("start_profile.txt") as f:
        return int(f.readline())


def write_followers(followers, filename="followers.txt"):
    with open(filename, "w+") as f:
        for follower in followers:
            f.write(follower + "\n")


def write_relations(my_followers_arr, username, filename="relations.txt"):
    with open(filename, "w+") as f:
        for key in my_followers_arr:
            line = (
                key
                + " "
                + "https://www.instagram.com/"
                + username
                + "/\n"
                + "https://www.instagram.com/"
                + username
                + "/ "
                + key
                + "\n"
            )
            f.write(line)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    # input parameters
    parser.add_argument("--username", type=str)
    parser.add_argument("--password", type=str)

    config = parser.parse_args()

    b = Bot()
    b.setUp()
    b.login(config.username, config.password)

    followers = b.get_my_followers(config.username)
    write_followers(followers)
