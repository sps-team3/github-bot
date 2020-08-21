from entity import *

def execute_issue_receive(repo, issue):
    title = 'GitHub: Issue Created'

    text = '[[%s]](%s)\n\n' % (repo['name'], repo['html_url'])
    text += '[Issue](%s) created by [%s](%s) \n\n' % (issue['html_url'], issue['user']['login'], issue['user']['html_url'])
    text += '%s\n\n' % (issue['title'])
    text += '%s\n\n' % (issue['body'])

    # get related configs

    configs = [{
        'token': 'moke_token',
        'remiders': [],
        'is_at_all': False,
    }]

    for config in configs:
        im_request = IMSenderEntity(config['token'], title, text, config['remiders'], config['is_at_all'])
        print(im_request)
        #send_msg(im_request)
