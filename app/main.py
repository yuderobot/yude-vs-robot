#!/usr/bin/env python3
# coding: UTF-8

import tweepy
import os
from os.path import join, dirname
from dotenv import load_dotenv
import datetime
import json
import matplotlib.pyplot as plt
import sys

# Import keys from .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
CK = os.environ.get("CK")
CS = os.environ.get("CS")
AT = os.environ.get("AT")
AS = os.environ.get("AS")

# Generate Twitter object
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)

# Variable for tweet counts
yude = 0
robot = 0

# File path for saving data
data_path = "./data/data.json"
banner_path = "./data/fig.png"

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
    # Check if the file exists
    if os.path.isfile(data_path):
        print("[INFO] 🔷 {} exists on filesystem. Skipping initialize step.".format(data_path))
        # Check if the file has valid JSON string
        try:
            json.load(open(data_path, 'r'))
        except json.JSONDecodeError as e:
            print(e)
            sys.exit("❌ `data/data.json` is not a valid JSON file.")
            
    else:
        print("[INFO] 🔷 {} does not exist! Generating.".format(data_path))
        
        data = {}
        data['timestamp'] = []
        data['yude'] = []
        data['robot'] = []
        
        with open(data_path, 'w') as outfile:
            json.dump(data, outfile)

# Load data from "data/data.json"
def load():
    print("[INFO] 🔷 Loading data.")
    init()
    raw = open(data_path, 'r')
    parsed = json.load(raw)
    return parsed

# Save data to "data/data.json"
def save(data = None):
    print("[INFO] 🔷 Storing data.")
    if data is None:
        print("[INFO] 🔷 'data' variable is N/A. Loading data from {}.".format(data_path))
        data = load()
    else:
        print("[INFO] 🔷 'data' variable is specified. Using it.")
    data['timestamp'].append(timestamp())
    data['yude'].append(get_yude())
    data['robot'].append(get_robot())
    
    with open(data_path, 'w') as outfile:
        json.dump(data, outfile)

# Delete old data. Leaving the past 7 items.
def delete():
    data = load()
    
    del data['timestamp'][:-7]
    del data['yude'][:-7]
    del data['robot'][:-7]
    
    with open(data_path, 'w') as outfile:
        json.dump(data, outfile)

# Show or save the graph by using matplotlib
def graph():
    print("[INFO] 🔷 Trying to show the graph by using matplotlib.")
    data = load()
    plt.figure(figsize=(15,5)) # 1500x500 is Twitter's recommendation of header size.
    
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
    
    # plt.show()
    plt.savefig(banner_path, format='png')
    print("[INFO] ✅ Successfully saved graph.")

# Update @yuderobot header with './data/fig.png'.
def update_header():
    api.update_profile_banner(banner_path)
    print("[INFO] ✅ Successfully updated profile banner.")

def main():
    init()
    save()
    delete()
    graph()
    update_header()

if __name__ == '__main__':
  main()