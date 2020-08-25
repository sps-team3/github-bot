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
    def execute(self):
        url = 'https://api.github.com/repos/%s/%s/pulls/%d/reviews' % (self.owner, self.repo,self.pull_number)
        headers = {
            "Authorization": "token %s" % TOKEN,
            "Accept": "application/vnd.github.golden-comet-preview+json"
        }
        commit= {        
        }
        payload = json.dumps(commit)
        r = requests.request("POST", url, data=payload, headers=headers)
        res_dict=r.json()
        self.review_id=res_dict['id']

        url = 'https://api.github.com/repos/%s/%s/pulls/%d/reviews/%d/events' % (self.owner, self.repo,self.pull_number,self.review_id)
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
    

class ClosePullRequestEntity:
    def __init__(self, owner, repo, pr_number, title, body):
        self.owner = owner
        self.repo = repo
        self.pr_number = pr_number
        self.title = title
        self.body = body
    def execute(self):
        url = 'https://api.github.com/repos/%s/%s/pulls/%d' % (self.owner, self.name,pull_number)
        headers = {
            "Authorization": "token %s" % TOKEN,
            "Accept": "application/vnd.github.golden-comet-preview+json"
        }  
        data = {
                'title':self.title,
                'body' :self.body,
                'state':'closed',
                }
        payload = json.dumps(data)
        r = requests.request("POST", url, data=payload, headers=headers)
        return r.content    
