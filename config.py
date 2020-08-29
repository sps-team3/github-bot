import json
from google.cloud import datastore


class Config:
    def __init__(self, bot_web_hook: str, repo: str, owner: str, is_at_all: bool, reminders: list, data: dict):
        self.bot_web_hook = bot_web_hook
        self.repo = repo
        self.owner = owner
        self._is_at_all = is_at_all
        self.reminders = reminders
        self.data = data

    def get_web_hook(self) -> str:
        return self.bot_web_hook

    def is_at_all(self) -> bool:
        return self._is_at_all

    def get_reminders(self) -> list:
        return self.reminders

    def get_repo(self) -> str:
        return self.repo

    def get_owner(self) -> str:
        return self.owner

    def get_data(self) -> dict:
        return self.data

    def __str__(self):
        config_str = "config:\n"
        config_str += "\tWebhook = " + self.get_web_hook() + "\n"
        config_str += "\trepo = " + self.get_repo() + "\n"
        config_str += "\towner = " + self.get_owner() + "\n"
        config_str += "\tis_at_all = " + str(self.is_at_all()) + "\n"
        config_str += "\treminders = ["
        for item in self.get_reminders():
            config_str += item + ", "
        config_str += "]\n"
        config_str += "\tdata = " + str(self.get_data()) + "\n"
        return config_str


class ConfigDataBase:
    def __init__(self):
        self.datastore_client = datastore.Client()

    def get_configs(self, repo: str, owner: str):
        query = self.datastore_client.query(kind='Config')
        query.add_filter('repo', '=', repo)
        query.add_filter('owner', '=', owner)
        results = list(query.fetch())  # list of Entity
        configs = []
        for entity in results:
            bot_web_hook = entity['bot_web_hook']
            is_at_all = entity['is_at_all']
            reminders = entity['reminders']
            data = json.loads(entity['data'])
            configs.append(Config(bot_web_hook, repo, owner, is_at_all, reminders, data))
        return configs

    def add_config(self, config: Config):
        self.__delete_entity(config.get_web_hook(), config.get_repo(), config.get_owner())
        entity = datastore.Entity(key=self.datastore_client.key('Config'))
        entity.update({
            'bot_web_hook': config.get_web_hook(),
            'repo': config.get_repo(),
            'owner': config.get_owner(),
            'is_at_all': config.is_at_all(),
            'reminders': config.get_reminders(),
            'data' : json.dumps(config.get_data())
        })
        self.datastore_client.put(entity)

    def __get_entity(self, bot_web_hook: str, repo: str, owner: str):
        query = self.datastore_client.query(kind='Config')
        query.add_filter('bot_web_hook', '=', bot_web_hook)
        query.add_filter('repo', '=', repo)
        query.add_filter('owner', '=', owner)
        results = list(query.fetch())  # list of Entity
        if results:
            return results[0]
        else:
            return None

    def __delete_entity(self, bot_web_hook: str, repo: str, owner: str):
        query = self.datastore_client.query(kind='Config')
        query.add_filter('bot_web_hook', '=', bot_web_hook)
        query.add_filter('repo', '=', repo)
        query.add_filter('owner', '=', owner)
        results: list = list(query.fetch())  # list of Entity
        entity: datastore.Entity
        for entity in results:
            self.datastore_client.delete(entity.key)


if __name__ == "__main__":
    config_store = ConfigDataBase()
    config = Config("http://www.test1.com", "tt", "tt", False, ["Alice"], {"group id": "qwertyu", "user id": "poiuy"})
    print(config)
    config_store.add_config(config)
    configs = config_store.get_configs("tt", "tt")
    print("get configs:\n")
    for c in configs:
        print(c)
