from entity import *
from Sender import *

def execute_issue_receive(repo, issue):
    title = 'GitHub: Issue Created'

    text = '[[%s]](%s)\n\n' % (repo['name'], repo['html_url'])
    text += '[Issue](%s) created by [%s](%s) \n\n' % (issue['html_url'], issue['user']['login'], issue['user']['html_url'])
    text += '%s\n\n' % (issue['title'])
    text += '%s\n\n' % (issue['body'])

    # get related configs by repo full_name

    configs = [{
        'token': 'moke_token',
        'remiders': [],
        'is_at_all': False,
    }]

    for config in configs:
        token = config['token']
        im_request = IMSenderEntity(token, title, text, config['remiders'], config['is_at_all'])
        print(im_request)
        send_dingding_msg(im_request)


def execute_comment_issue(body):
    # straightforward call sender?
    print(body)


def execute_approve_issue(body):
    # straightforward call sender?
    print(body)


def execute_close_pullrequest(body):
    # straightforward call sender?
    print(body)


def execute_receive_configuration(configuration):
    # call config function
    print(configuration)
