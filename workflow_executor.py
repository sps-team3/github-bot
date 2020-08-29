from entity import IMSenderEntity
from sender import send_dingding_msg

configs = [{
    'token': 'mock_token',
    'remiders': [],
    'is_at_all': False,
    }]

def execute_issue_open(json):
    repo = json['repository']
    issue = json['issue']

    title = 'GitHub: Issue Created'
    text = ''
    text += '[[%s]](%s)\n\n' % (repo['name'], repo['html_url'])
    text += '[Issue](%s) created by [%s](%s) \n\n' % \
        (issue['html_url'], issue['user']['login'], issue['user']['html_url'])
    text += '%s\n\n' % (issue['title'])
    text += '%s\n\n' % (issue['body'])

    # get related configs by repo full_name

    for config in configs:
        token = config['token']
        im_request = IMSenderEntity(token, title, text, config['remiders'], config['is_at_all'])
        print(im_request)
        send_dingding_msg(im_request)


def execute_issue_comment(json):
    repo = json['repository']
    issue = json['issue']
    comment = json['comment']
    if 'pull_request' in issue.keys():
        title = 'GitHub: Pull Request Commented'
        tp = 'Pull Request'
    else:
        title = 'GitHub: Issue Commented'
        tp = 'Issue'
    text = ''
    text += '[[%s]](%s)\n\n' % (repo['name'], repo['html_url'])
    text += '[%s](%s) has a new [comment](%s) by [%s](%s) \n\n' % \
        (tp,
         issue['html_url'], comment['html_url'],
         issue['user']['login'], issue['user']['html_url'])
    text += '%s\n\n' % (comment['body'])

    for config in configs:
        token = config['token']
        im_request = IMSenderEntity(token, title, text, config['remiders'], config['is_at_all'])
        print(im_request)
        send_dingding_msg(im_request)


def execute_pull_request_open(json):
    repo = json['repository']
    pull_request = json['pull_request']

    title = 'GitHub: Pull Request Created'
    text = ''
    text += '[[%s]](%s)\n\n' % (repo['name'], repo['html_url'])
    text += 'new [pull request](%s) created by [%s](%s) \n\n' % \
        (pull_request['html_url'], pull_request['user']['login'], pull_request['user']['html_url'])
    text += '%s\n\n' % (pull_request['title'])
    text += '%s\n\n' % (pull_request['body'])

    for config in configs:
        token = config['token']
        im_request = IMSenderEntity(token, title, text, config['remiders'], config['is_at_all'])
        print(im_request)
        send_dingding_msg(im_request)


def execute_pull_request_close(json):
    repo = json['repository']
    pull_request = json['pull_request']
    merged = pull_request['merged']
    merged_by = pull_request['merged_by']

    # check if merge
    if merged:
        title = 'GitHub: Pull Request Merged'
        text = ''
        text += '[[%s]](%s)\n\n' % (repo['name'], repo['html_url'])
        text += '[pull request](%s) was merged by [%s](%s) \n\n' % \
            (pull_request['html_url'], merged_by['login'], merged_by['html_url'])
        text += '%s\n\n' % (pull_request['title'])
        text += '%s\n\n' % (pull_request['body'])

        for config in configs:
            im_request = IMSenderEntity(config['token'], title, text,
                                        config['remiders'], config['is_at_all'])
            print(im_request)
            send_dingding_msg(im_request)

def execute_pr_review_comment(json):
    repo = json['repository']
    pull_request = json['pull_request']
    comment = json['comment']
    user = comment['user']

    title = 'GitHub: Pull Request Review Commented'
    text = ''
    text += '[[%s]](%s)\n\n' % (repo['name'], repo['html_url'])
    text += '[Pull Request](%s) has a new review comment by [%s](%s)\n\n' % \
            (pull_request['html_url'], user['login'], user['html_url'])
    text += '%s\n\n' % (comment['body'])

    for config in configs:
        im_request = IMSenderEntity(config['token'], title, text,
                config['remiders'], config['is_at_all'])
        print(im_request)
        send_dingding_msg(im_request)

def execute_approve_issue(body):
    # straightforward call sender?
    print(body)


def execute_receive_configuration(configuration):
    # call config function
    print(configuration)
