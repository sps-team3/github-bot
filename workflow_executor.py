from entity import IMSenderEntity, ApprovePullRequestEntity, CreateWebhookEntity
from sender import send_dingding_msg, approve_pull_request, create_repo_webhook
from config import ConfigDataBase, Config

config_store = ConfigDataBase()

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

    configs = config_store.get_configs(repo['name'], repo['owner']['login'])

    for config in configs:
        token = config.bot_web_hook
        im_request = IMSenderEntity(token, title, text, config.remiders, config.is_at_all)
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

    configs = config_store.get_configs(repo['name'], repo['owner']['login'])

    for config in configs:
        token = config.bot_web_hook
        im_request = IMSenderEntity(token, title, text, config.remiders, config.is_at_all)
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

    configs = config_store.get_configs(repo['name'], repo['owner']['login'])

    for config in configs:
        token = config.bot_web_hook
        im_request = IMSenderEntity(token, title, text, config.remiders, config.is_at_all)
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

        configs = config_store.get_configs(repo['name'], repo['owner']['login'])

        for config in configs:
            token = config.bot_web_hook
            im_request = IMSenderEntity(token, title, text, config.remiders, config.is_at_all)
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

    configs = config_store.get_configs(repo['name'], repo['owner']['login'])

    for config in configs:
        im_request = IMSenderEntity(config['token'], title, text,
                config['remiders'], config['is_at_all'])
        print(im_request)
        send_dingding_msg(im_request)


def check_config_exist(repo, owner, group_id):
    """Check whether the gourp has set config, return true if exist"""
    configs = config_store.get_configs(repo, owner)
    for config in configs:
        data = config.data
        if data['group id'] == group_id:
            return True
    return False


def execute_approve_pull_request(body):
    repo = body['repo']
    owner = body['owner']
    pr_number = body['pr_number']
    content = body['content']
    group_id = body['group_id']

    if check_config_exist(repo, owner. group_id):
        entity = ApprovePullRequestEntity(owner, repo, pr_number, content)
        return approve_pull_request(entity)
    
    return 'No config exist'


def execute_receive_configuration(configuration):
    token = configuration['token']
    repo = configuration['repo']
    owner = configuration['owner']
    is_at_all = configuration['at_all']
    reminders = configuration['reminders']

    webhook = CreateWebhookEntity(owner, repo)
    response = create_repo_webhook(webhook)

    # if create webhook successfully, save config
    config = Config(token, repo, owner, is_at_all, reminders)
    config_store.add_config(config)
