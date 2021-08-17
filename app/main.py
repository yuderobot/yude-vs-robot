#!/usr/bin/env python3
# coding: UTF-8

import tweepy
import os
from os.path import join, dirname
from dotenv import load_dotenv
import datetime
import json
import matplotlib.pyplot as plt

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
    print("[INFO] 💬 @yude_jp has {} tweets".format(yude))
    return yude

# Get @yuderobot tweet count
def get_robot():
    tweets = api.get_user("yuderobot").statuses_count
    robot = tweets
    print("[INFO] 💬 @yuderobot has {} tweets".format(robot))
    return robot

def timestamp():
    dt_now = datetime.datetime.now()
    return dt_now.strftime('%Y-%m-%d %H-%M-%S')

# Initialize "data/data.json" in case there's no file
def init():
    if os.path.isfile(path):
        print("[INFO] 💮 {} exists on filesystem. Skipping initialize step.".format(path))
        pass
    else:
        print("[INFO] 💥 {} does not exist! Generating.".format(path))
        
        data = {}
        data['timestamp'] = []
        data['yude'] = []
        data['robot'] = []
        
        with open(path, 'w') as outfile:
            json.dump(data, outfile)
        
# Load data from "data/data.json"
def load():
    print("[INFO] 💦 Loading data.")
    init()
    raw = open(path, 'r')
    parsed = json.load(raw)
    return parsed

# Save data to "data/data.json"
def save():
    print("[INFO] 💨 Storing data.")
    data = load()
    print(data)
    data['timestamp'].append(timestamp())
    data['yude'].append(get_yude())
    data['robot'].append(get_robot())
    
    with open(path, 'w') as outfile:
        json.dump(data, outfile)
    print("[INFO] ✅ The data has been successfully stored. Below is its content:\n{}".format(data))

# Show the graph by using matplotlib
def show_graph():
    print("💹 Trying to show the graph by using matplotlib.")
    data = load()
    plt.figure()
    
    # @yude_jp
    x = data['timestamp']
    y = data['yude']
    plt.plot(x, y, label='@yude_jp')
    
    # @yuderobot
    y = data['robot']
    plt.plot(x, y, label='@yuderobot')
    
    plt.legend()
    plt.title("@yude_jp vs @yuderobot")
    plt.xlabel('timestamp')
    plt.ylabel('tweets')
    
    plt.show()


def main():
    init()
    save()
    show_graph()

if __name__ == '__main__':
  main()