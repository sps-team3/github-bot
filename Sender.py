import sys
import importlib
importlib.reload(sys)

import os
import requests
import json

def make_issue_comment(REPO_OWNER, REPO_NAME,Tissue_number,body):
    
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

def approve_pull_request(REPO_OWNER, REPO_NAME,pull_number):
    
    url = 'https://api.github.com/repos/%s/%s/pulls/%d/reviews' % (REPO_OWNER, REPO_NAME,pull_number)
    
    # Headers
    headers = {
        "Authorization": "token %s" % TOKEN,
        "Accept": "application/vnd.github.golden-comet-preview+json"
    }
    
    commit= {
                
        }
    payload = json.dumps(commit)

   
    r = requests.request("POST", url, data=payload, headers=headers)
    return r.content
    
def submit_pull_request(REPO_OWNER, REPO_NAME,pull_number,review_id):
    
    url = 'https://api.github.com/repos/%s/%s/pulls/%d/reviews/%d/events' % (REPO_OWNER, REPO_NAME,pull_number,review_id)
    
    # Headers
    headers = {
        "Authorization": "token %s" % TOKEN,
        "Accept": "application/vnd.github.golden-comet-preview+json"
    }
    
    commit= {
                'event':'APPROVE'
                
        }
    payload = json.dumps(commit)
    r = requests.request("POST", url, data=payload, headers=headers)
    return r.content
    
def close_pull_requests(REPO_OWNER, REPO_NAME,pull_number,title,body):
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

def send_dingding_msg(im_request):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % (im_request.token)
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": im_request.title,
            "text": im_request.text
        },
        "at": {
            "atMobiles": im_request.reminders,
            "isAtAll": im_request.is_at_all
        }
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.text
