from scrape.bot import Bot
import argparse


def generate_file(followers, filename="followers.txt"):
    with open(filename, 'w+') as f:
        for follower in followers:
            f.write(follower + "\n")


def get_followers(config):
    username = config.username
    password = config.password

    b = Bot()
    b.setUp()
    b.login(username, password)

    my_followers = b.get_my_followers(username)
    generate_file(my_followers)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # input parameters
    parser.add_argument('--username', type=str)
    parser.add_argument('--password', type=str)

    config = parser.parse_args()

    get_followers(config)
