class IMSenderEntity:
    def __init__(self, token, title, text, reminders, is_at_all):
        self.token = token
        self.title = title
        self.text = text
        self.reminders = reminders
        self.is_at_all = is_at_all

    def __str__(self):
        text = 'token: %s \n' % (self.token)
        text += 'reminders: %s \n' % (self.reminders)
        text += 'is_at_all: %s \n' % (self.is_at_all)
        text += 'title: %s \n' % (self.title)
        text += 'text: %s \n' % (self.text)
        return text

class IMReplyEntity:
    def __init__(self, url, content):
        self.url = url
        self.content = content

class CommentIssueEntity:
    def __init__(self, owner, repo, issue_number, body):
        self.owner = owner
        self.repo = repo
        self.issue_number = issue_number
        self.body = body


class ApprovePullRequestEntity:
    def __init__(self, owner, repo, pr_number, body):
        self.owner = owner
        self.repo = repo
        self.pr_number = pr_number
        self.body = body
    

class ClosePullRequestEntity:
    def __init__(self, owner, repo, pr_number, title, body):
        self.owner = owner
        self.repo = repo
        self.pr_number = pr_number
        self.title = title
        self.body = body

    
class CreateWebhookEntity:
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
