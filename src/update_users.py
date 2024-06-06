import sys
import json

if (len(sys.argv) > 1):
    username, act_name = sys.argv[1].split(',')
    username = username.strip()
    act_name = act_name.strip()
    with open("data/users.json") as f:
        try:
            users = json.load(f)
        except:
            SystemExit(1)
    with open("data/users.json", 'w') as f:
        users['username'] = act_name
        json.dump(users, f)