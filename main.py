import datetime
import json
import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

DINGTALK_PREFIX = 'https://oapi.dingtalk.com/robot/send?access_token='
ACCESS_TOKEN = ''

@app.route('/', methods=['GET', 'POST'])
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    return render_template('index.html', 
            times=dummy_times)

@app.route('/webhook/bot', methods=['GET', 'POST'])
def receiver():
    print(request.headers)
 #   print(request.json)

    repo = request.json["repository"]
    issue = request.json["issue"]

    title = "GitHub: Issue created"

    text = ""
    text += '[[' + repo["name"] + ']](' + repo["html_url"] + ')'
    text += "Issue created by "
    text += '[' + issue["user"]["login"] + '](' + issue["user"]["html_url"] + ')'
    text += '\n\n'

    text += '[[issue link]](' + issue["html_url"] + ')'
    text += '\n\n'

    text += issue["title"] + '\n\n'
    text += issue["body"] + '\n\n'

    data = {
            "msgtype": "markdown",
            "markdown": { 
                "title": title,
                "text":  text
                }
            }
    url = DINGTALK_PREFIX + ACCESS_TOKEN
    headers = {
            "Content-Type": "application/json"
            }
    print(data)
    print(url)
    print(headers)

    content = requests.request("POST", url, data=json.dumps(data), headers=headers).content
    print(content)
    return content

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
