import requests
import json

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
result = requests.get(url = "https://leetcode.com/graphql", json={'query' : query, 'variables' : variables}).json()

for res in list(result['data'].values()):
    for type in res['submitStats']['acSubmissionNum']:
        print(f'{type['difficulty']} : {type['count']}')