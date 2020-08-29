from google.cloud import datastore


class Config:
    def __init__(self, bot_web_hook: str, repo_url: str, is_at_all: bool, reminders: list):
        self.bot_web_hook = bot_web_hook
        self.repo_url = repo_url
        self.is_at_all = is_at_all
        self.reminders = reminders

    def get_web_hook(self) -> str:
        return self.bot_web_hook

    def is_at_all(self) -> bool:
        return self.is_at_all

    def get_reminders(self) -> list:
        return self.reminders

    def get_repo_url(self) -> str:
        return self.repo_url

    def __str__(self):
        config_str = "config:\n"
        config_str += "\tWebhook = " + self.bot_web_hook + "\n"
        config_str += "\trepo url = " + self.repo_url + "\n"
        config_str += "\tis_at_all = " + str(self.is_at_all) + "\n"
        config_str += "\treminders = ["
        for item in self.reminders:
            config_str += item + ", "
        config_str += "]\n"
        return config_str


class ConfigDataBase:
    def __init__(self):
        self.datastore_client = datastore.Client()

    def get_configs(self, repo_url: str):
        query = self.datastore_client.query(kind='Config')
        query.add_filter('repo_url', '=', repo_url)
        results = list(query.fetch())  # list of Entity
        configs = []
        for entity in results:
            bot_web_hook = entity['bot_web_hook']
            is_at_all = entity['is_at_all']
            reminders = entity['reminders']
            configs.append(Config(bot_web_hook, repo_url, is_at_all, reminders))
        return configs

    def add_config(self, config: Config):
        self.__delete_entity(config.bot_web_hook, config.repo_url)
        entity = datastore.Entity(key=self.datastore_client.key('Config'))
        entity.update({
            'bot_web_hook': config.bot_web_hook,
            'repo_url': config.repo_url,
            'is_at_all': config.is_at_all,
            'reminders': config.reminders
        })
        self.datastore_client.put(entity)

    def __get_entity(self, bot_web_hook: str, repo_url: str):
        query = self.datastore_client.query(kind='Config')
        query.add_filter('bot_web_hook', '=', bot_web_hook)
        query.add_filter('repo_url', '=', repo_url)
        results = list(query.fetch())  # list of Entity
        if results:
            return results[0]
        else:
            return None

    def __delete_entity(self, bot_web_hook: str, repo_url: str):
        query = self.datastore_client.query(kind='Config')
        query.add_filter('bot_web_hook', '=', bot_web_hook)
        query.add_filter('repo_url', '=', repo_url)
        results: list = list(query.fetch())  # list of Entity
        entity: datastore.Entity
        for entity in results:
            self.datastore_client.delete(entity.key)


if __name__ == "__main__":
    config_store = ConfigDataBase()
    config = Config("http://www.test3.com", "github.com/tt/tt", True, ["Alice", "Bob"])
    print(config)
    config_store.add_config(config)
    configs = config_store.get_configs("github.com/tt/tt")
    for c in configs:
        print(c)
