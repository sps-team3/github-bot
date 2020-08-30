import json
import requests

TOKEN = 'ef4bc3afd938ca0bc616c7e8fd4978ae978365d7832028c13e4e565a20f95bdf'

def make_issue_comment(request_entity):

    url = 'https://api.github.com/repos/%s/%s/issues/%d/comments' % \
        (request_entity.owner, request_entity.repo, request_entity.issue_number)

    # Headers
    headers = {
        'Authorization': 'token %s' % TOKEN,
        'Accept': 'application/vnd.github.golden-comet-preview+json'
    }

    # Create our issue
    request_entity = {
        'body': request_entity.body
    }
    # Add the issue to our repository
    payload = json.dumps(request_entity)

    r = requests.request('POST', url, data=payload, headers=headers)
    return r.content

def approve_pull_request(approve_entity):

    url = 'https://api.github.com/repos/%s/%s/pulls/%d/reviews' % (approve_entity.owner, approve_entity.repo, approve_entity.pr_number)
    headers = {
        "Authorization": "token %s" % TOKEN,
        "Accept": "application/vnd.github.golden-comet-preview+json"
    }
    commit= {        
    }
    payload = json.dumps(approve_entity.body)
    r = requests.request("POST", url, data=payload, headers=headers)
    
    res_dict=r.json()
    review_id=res_dict['id']

    url = 'https://api.github.com/repos/%s/%s/pulls/%d/reviews/%d/events' % (approve_entity.owner, approve_entity.repo, approve_entity.pr_number,review_id)
    headers = {
        "Authorization": "token %s" % TOKEN,
        "Accept": "application/vnd.github.golden-comet-preview+json"
    }
    commit= {
         'event':'APPROVE'      
    }
    payload = json.dumps(commit)
    r = requests.request("POST", url, data=payload, headers=headers)
    
    #return r.content
    print (r.content)

def close_pull_requests(close_entity):
    url = 'https://api.github.com/repos/%s/%s/pulls/%d' % (close_entity.owner, close_entity.repo, close_entity.pr_number)

    # Headers
    headers = {
        'Authorization': 'token %s' % TOKEN,
        'Accept': 'application/vnd.github.golden-comet-preview+json'
    }

    data = {
        'title':close_entity.title,
        'body' :close_entity.body,
        'state':'closed',
        }

    payload = json.dumps(data)

    r = requests.request('POST', url, data=payload, headers=headers)
    return r.content

def send_dingding_msg(im_request):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % (im_request.token)
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
        'msgtype': 'markdown',
        'markdown': {
            'title': im_request.title,
            'text': im_request.text
        },
        'at': {
            'atMobiles': im_request.reminders,
            'isAtAll': im_request.is_at_all
        }
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.text

def reply_dingding_msg(reply):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
        'msgtype': 'text',
        'text': {
            'content': reply.content
        },
        'at': {
            'atMobiles': [],
            'isAtAll': False
        }
    }
    r = requests.post(reply.url, data=json.dumps(data), headers=headers)
    return r.text

def create_repo_webhook(webhook_entity):

    url = 'https://api.github.com/repos/%s/%s/hooks' % (webhook_entity.owner, webhook_entity.repo)
    webhook_url = 'summer20-sps-52.appspot.com/webhook/bot' 

    # Headers
    headers = {
        'Authorization': 'token %s' % TOKEN,
        'Accept': 'application/vnd.github.golden-comet-preview+json'
    }

    # Create our issue
    data={
        'config': {
        'url': webhook_url,
        #'secret': secret,
        'content_type': 'json',
        'insecure_ssl': '0',
            },
        'events':['*']
        }
    # Add the issue to our repository
    payload = json.dumps(data)

    r = requests.request('POST', url, data=payload, headers=headers)
    return r.content


