import requests
import json

URL = "https://leetcode.com/graphql"

query_parts = []
with open("data/users.json") as f:
    users = json.load(f)
names = list(users.keys())
for i, uname in enumerate(names):
    alias = f"user{i+1}"
    query =f"""
    {alias}: matchedUser(username: "{uname}") {{
        username
        submitStats: submitStatsGlobal {{
            acSubmissionNum {{
                difficulty
                count
                submissions
            }}
        }}
    }}
    """
    query_parts.append(query)
query_body = "\n".join(query_parts)
query = f"""
query getUserProfiles{{
    {query_body}
}}
"""
variables = {"username" : names}
result = requests.get(url = URL, json={'query' : query, 'variables' : variables}).json()

stats = []
for res in list(result['data'].values()):
    user_info = {}
    user_info['username'] = res['username']
    user_info['act_name'] = users[user_info['username']]
    user_info['problems_solved'] = 0
    for type in res['submitStats']['acSubmissionNum']:
        user_info[type['difficulty']] = type['count']
        user_info['problems_solved'] += type['count']
    user_info['totalScore'] = user_info['Easy'] + 2*user_info['Medium'] + 3*user_info['Hard']
    stats.append(user_info)

sorted_stats = sorted(stats, key=lambda x : x['totalScore'], reverse=True)

# Markdown Update
with open("README.md", 'w') as file:
    file.write('# 🏆 Leetcode Leaderboard 🏆\n\n')
    file.write('| Rank | Score | Username       | Name | Problems Solved \n')
    for index, stat in enumerate(sorted_stats):
        index +=1
        rank_emoji = ""
        if index == 1:
            rank_emoji = "🥇 1"
        elif index == 2:
            rank_emoji = "🥈 2"
        elif index == 3:
            rank_emoji = "🥉 3"
        else:
            rank_emoji = f'{index}'
        file.write(f'| {rank_emoji} | {stat['totalScore']} | {stat['username']} | {stat['act_name']} | {stat['problems_solved']} \n')
    file.write("---")

