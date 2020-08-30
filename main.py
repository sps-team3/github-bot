import datetime
import json
from flask import Flask, render_template, request, redirect
from workflow_executor import execute_issue_open, execute_issue_comment, execute_pull_request_open
from workflow_executor import execute_pull_request_close, execute_pr_review_comment, execute_approve_pull_request
from workflow_executor import execute_receive_configuration, execute_reply_message
from entity import IMSenderEntity
from sender import send_dingding_msg
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    return render_template('index.html', times=dummy_times)

@app.route('/webhook/bot', methods=['GET', 'POST'])
def receiver():
    print(request.headers)
    print(request.json)

    event = request.headers['X-GitHub-Event']
    action = request.json['action']
    print(event)
    event_map = {
        'issues': {
            'opened': execute_issue_open,
            },
        'issue_comment': {
            'created': execute_issue_comment,
            },
        'pull_request': {
            'opened': execute_pull_request_open,
            'closed': execute_pull_request_close
            },
        'pull_request_review_comment': {
            'created': execute_pr_review_comment
            },
        }
    event_map[event][action](request.json)
    return ''

@app.route('/webhook/im', methods=['GET', 'POST'])
def im_receiver():
    print(request.headers)
    print(request.json)

    data = request.json
    content = data['text']['content']
    group_id = data['conversationId']
  #  webhook = data['sessionWebhook']

    content = content.strip()

    print(content)
    print(group_id)

    words = content.split(' ')
    for i in range(len(words)):
        words[i] = words[i].strip()

    request_type = words[0]
    
    if request_type == 'approve_pr':
        execute_approve_pull_request(words, group_id)
    elif request_type == 'config':
        execute_receive_configuration(words, group_id)
    
    #execute_reply_message(webhook)
    reply = {
        'msgtype': 'hub text',
        'text': {
            'content': 'hubhubtestsssssss'
        }
    }

    response_content = 'Receive content: ' + content
    
    return json.dumps(reply)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.config['JSON_AS_ASCII'] = False
    app.run(host='127.0.0.1', port=8080, debug=True)
