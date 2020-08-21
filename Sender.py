import sys
import importlib
importlib.reload(sys)

import os
import requests
import json
def make_issue_comment(REPO_OWNER, REPO_NAME,TOKEN,issue_number,body):
    
    url = 'https://api.github.com/repos/%s/%s/issues/%d/comments' % (REPO_OWNER, REPO_NAME,issue_number)
    
    # Headers
    headers = {
        "Authorization": "token %s" % TOKEN,
        "Accept": "application/vnd.github.golden-comet-preview+json"
    }
    
    # Create our issue
    comment = {'body': body
             }
    # Add the issue to our repository
    payload = json.dumps(comment)

   
    r = requests.request("POST", url, data=payload, headers=headers)
    return r.content

    
def pull_request_approve(REPO_OWNER, REPO_NAME,TOKEN,pull_number,commit_title):
    
    url = 'https://api.github.com/repos/%s/%s/pulls/%d/merge' % (REPO_OWNER, REPO_NAME,pull_number)
    
    # Headers
    headers = {
        "Authorization": "token %s" % TOKEN,
        "Accept": "application/vnd.github.golden-comet-preview+json"
    }
    
    commit= {
                'commit_title': commit_title}
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    r = session.post(url, json.dumps(commit))
    return r.content
    
def close_pull_requests(REPO_OWNER, REPO_NAME,TOKEN,pull_number,title,body):
    url = 'https://api.github.com/repos/%s/%s/pulls/%d' % (REPO_OWNER, REPO_NAME,pull_number)
    
    # Headers
    headers = {
        "Authorization": "token %s" % TOKEN,
        "Accept": "application/vnd.github.golden-comet-preview+json"
    }
    
    data = {
                'title':title,
                'body' :body,
                'state':'closed',
                }
   
    payload = json.dumps(data)

   
    r = requests.request("POST", url, data=payload, headers=headers)
    return r.content

def send_msg(url, reminders, text,title,link):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
    "msgtype": "link", # 发送消息类型为文本
    "at": {
    "atMobiles": reminders,
    "isAtAll": False, # 不@所有人
    },
    "link": {
        "text": text,
        "title":title,
        "picUrl": "", 
        "messageUrl": link
        }
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.text
