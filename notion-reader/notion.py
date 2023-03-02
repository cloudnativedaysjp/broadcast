import json
import os
import sys
from notion_client import Client

args = sys.argv
if len(args) <= 1:
    print('Usage: notion.py <database_id>')
    exit()

notion = Client(auth=os.environ["NOTION_TOKEN"])

result = notion.databases.query(
    **{
        'database_id' : args[1]
       }
)

print(json.dumps(result))
