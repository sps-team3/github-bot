from google.cloud import datastore

class Config:
    def __init__(self, bot_web_hook, repo_url, watch_list):
        self.bot_web_hook = bot_web_hook
        self.repo_url = repo_url
        self.watch_list = watch_list
    
    def get_web_hook(self):
        return self.bot_web_hook
    
    def get_watch_list(self):
        return self.watch_list

    def get_repo_url(self):
        return self.repo_url

    def __str__(self):
        config_str = "config:\n"
        config_str += "\tWebhook = " + self.bot_web_hook + "\n"
        config_str += "\trepo url = " + self.repo_url + "\n"
        config_str += "\twatch list = ["
        for item in self.watch_list:
            config_str += item + ", "
        config_str += "]\n"
        return config_str

datastore_client = datastore.Client()

def get_configs(repo_url: str):
    query = datastore_client.query(kind='Config')
    query.add_filter('repo_url', '=', repo_url)
    results = list(query.fetch()) # list of Entity
    configs = []
    for entity in results:
        bot_web_hook = entity['bot_web_hook']
        watch_list = entity['watch_list']
        configs.append(Config(bot_web_hook, repo_url, watch_list))
    return configs

def add_config(config: Config):
    entity = datastore.Entity(key=datastore_client.key('Config'))
    entity.update({
        'bot_web_hook': config.bot_web_hook,
        'repo_url': config.repo_url,
        'watch_list': config.watch_list
    })

    datastore_client.put(entity)

if  __name__ == "__main__":
    # config = Config("http://www.test.com", "github.com/tt/tt", ["commit", "pull request"])
    # print(config)
    # add_config(config)
    url = "github.com/tt/tt"
    configs = get_configs(url)
    for c in configs:
        print(c)