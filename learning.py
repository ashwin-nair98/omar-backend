import pandas as pd
from watson_developer_cloud import AssistantV1
import numpy as np
from sklearn.model_selection import KFold
import pixiedust
import json
from urllib.parse import urlparse, parse_qs
import itertools
import matplotlib.pyplot as plt
import datetime, dateutil.parser
import seaborn as sns
%matplotlib inline
import warnings
import openpyxl
warnings.filterwarnings("ignore")
from pprint import pprint
ctx = {
  "url": "https://gateway.watsonplatform.net/conversation/api",
  "username": "user",
  "password": "password"
}

workspace_id = "worlspace_id"
conversation = AssistantV1( username=ctx.get('username'), password=ctx.get('password'), version='2018-02-18', url=ctx.get('url'))

extractedLogs = []
response1 = { 'pagination': 'DUMMY' } #This is set to start the loop
cursor = None
counter = 0
fltr = None  # Can be used to get a specific date

while response1['pagination']:
    print ("Reading Logs for Page: ", counter)
    counter = counter + 1
    response1 = conversation.list_logs(workspace_id=workspace_id, page_limit = 1000, cursor=cursor)
    extractedLogs.append(response1['logs'])
    
    #The API has a limit of a 100 logs to pull
    #To get the full log You need to update the cursor variable with a new cursor pointing to the next page
    #The cursor is fetched using the next_url variable
    
    if 'pagination' in response1 and 'next_url' in response1['pagination']:
        p = response1['pagination']['next_url']
        u = urlparse(p) 
        query = parse_qs(u.query)
        cursor = query['cursor'][0]
print("Reading logs completed.")


extraction = []
for logs in extractedLogs:
    for elem in logs:
        userinput = elem['response']['input']
        logID = elem['response']['context']['conversation_id']
        if not elem['response']['intents']:
            intentss = [{'confidence': 0, 'intent': 'No Intent Detected'}]
            intentss = intentss[0]
        else:
            intentss = elem['response']['intents'][0]
        
    
        wcsoutput = elem['response']['output']
        userInput = userinput.get('text')
        wcsOutput = wcsoutput.get('text')
        time = elem['request_timestamp']
        row = {
            'Log_ID': logID,
            'Request_TimeStamp': dateutil.parser.parse(time),
            'User_Input': userInput,
            'Watson_Output': wcsOutput,
            'Confidence_Level': intentss['confidence'] * 100,
            'Intent_Detected': intentss['intent']
        }
        extraction.append(row)
df = pd.DataFrame(extraction, columns=['Log_ID', 'User_Input', 'Intent_Detected','Confidence_Level','Watson_Output', 'Request_TimeStamp'])
display(df)



extractedID = {}
for logs in extractedLogs:
    for elem in logs:
        userinput = elem['response']['input']
        logID = elem['response']['context']['conversation_id']
        if not elem['response']['intents']:
            intentss = [{'confidence': 0, 'intent': 'No Intent Detected'}]
            intentss = intentss[0]
        else:
            intentss = elem['response']['intents'][0]
        
    
        wcsoutput = elem['response']['output']
        userInput = userinput.get('text')
        wcsOutput = wcsoutput.get('text')
        time = elem['request_timestamp']
        row = {
            'Log_ID': logID,
            'Request_TimeStamp': dateutil.parser.parse(time),
            'User_Input': userInput,
            'Watson_Output': wcsOutput,
            'Confidence_Level': intentss['confidence'] * 100,
            'Intent_Detected': intentss['intent']
        }
        extractedID.setdefault(logID, []).append(row)

for log in extractedID:
    extractedID[log].sort(key=lambda x: x['Request_TimeStamp'], reverse=False)

pprint(extractedID)

# Use extractedId object for further learning