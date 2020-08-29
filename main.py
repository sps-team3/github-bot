import datetime
from flask import Flask, render_template, request, redirect
from workflow_executor import execute_issue_open, execute_issue_comment, execute_pull_request_open
from workflow_executor import execute_pull_request_close, execute_pr_review_comment, execute_pr_approve

app = Flask(__name__)

DINGTALK_PREFIX = 'https://oapi.dingtalk.com/robot/send?access_token='
ACCESS_TOKEN = 'ef4bc3afd938ca0bc616c7e8fd4978ae978365d7832028c13e4e565a20f95bdf'

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
 #   print(request.json)

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
        'pull_request_review': {
            'submitted': execute_pr_approve
            },
        }
    event_map[event][action](request.json)
    return ''

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
