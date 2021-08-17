import tweepy
import os
from os.path import join, dirname
from dotenv import load_dotenv
import datetime
import json

# Import keys from .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
CK = os.environ.get("CK")
CS = os.environ.get("CS")
AT = os.environ.get("AT")
AS = os.environ.get("AS")

# Generate Twitter objects
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)

# Variable for tweet counts
yude = 0
robot = 0

# File path for saving data
path = "./data/data.json"

# Get @yude_jp tweet count
def get_yude():
    tweets = api.get_user("yude_jp").statuses_count
    yude = tweets
    print("@yude_jp has {} tweets".format(yude))
    return yude

# Get @yuderobot tweet count
def get_robot():
    tweets = api.get_user("yuderobot").statuses_count
    robot = tweets
    print("@yuderobot has {} tweets".format(robot))
    return robot

def timestamp():
    dt_now = datetime.datetime.now()
    return dt_now.strftime('%Y-%m-%d %H-%M-%S')

# Initialize "data/data.json" in case there's no file
def init():
    if os.path.isfile(path):
        print("{} exists on filesystem. Skipping initialize step.".format(path))
        pass
    else:
        print("{} does not exist! Generating.".format(path))
        data = {}
        data['count'] = []
        with open(path, 'w') as outfile:
            json.dump(data, outfile)
        
# Load data from "data/data.json"
def load():
    raw = open(path, 'r')
    parsed = json.load(raw)
    return parsed

# Save data to "data/data.json"
def save():
    data = load()
    print(data)
    data['count'].append({
        "timestamp": timestamp(),
        "yude": get_yude(),
        "robot": get_robot()
    })
    with open(path, 'w') as outfile:
        json.dump(data, outfile)
    print("The data has been successfully stored. Below is its content:\n{}".format(data))

def main():
    init()
    save()

if __name__ == '__main__':
  main()