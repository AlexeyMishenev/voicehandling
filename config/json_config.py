import json
from os import mkdir
from os.path import join, exists


class Config:
    def __init__(self, path) -> None:
        self.__path = path
        self.__abs_path = 'config'
        if not exists(self.__path):
            mkdir(path)
        self.config_json = "config"

    def set(self, key, value, paths=None) -> None:
        if not paths:
            paths = [self.config_json]
        if isinstance(paths, str):
            paths = [paths]
        paths[-1] += '.json'
        with open(join(self.__abs_path, self.__path, *paths), "r+", encoding='utf8') as fp:
            opt = json.load(fp)
            opt[key] = value
            fp.seek(0)
            fp.truncate()
            json.dump(opt, fp, indent=4)

    def get(self, key, fallback="", paths=None):
        if not paths:
            paths = [self.config_json]
        if isinstance(paths, str):
            paths = [paths]
        paths[-1] += '.json'
        with open(join(self.__abs_path, self.__path, *paths), "r", encoding='utf8') as f:
            try:
                value = json.load(f)[key]
            except KeyError:
                value = fallback
                self.set(key, fallback, paths)
            return value

    def get_all(self, paths=None) -> dict:
        if not paths:
            paths = [self.config_json]
        if isinstance(paths, str):
            paths = [paths]
        paths[-1] += '.json'
        with open(join(self.__abs_path, self.__path, *paths), "r", encoding='utf8') as f:
            values = json.load(f)
            return values


class JsonConfig(Config):
    def set(self, key, value, section=None) -> None:
        if not section:
            raise ValueError("section parameter mast be not None")
        lang = super().get('lang')
        super().set(key, value, [lang, section])

    def get(self, key, fallback="", section=None):
        if not section:
            raise ValueError("section parameter mast be not None")
        lang = super().get('lang')
        return super().get(key, fallback, [lang, section])

    def get_all(self, section=None) -> dict:
        if not section:
            raise ValueError("section parameter mast be not None")
        lang = super().get('lang')
        return super().get_all([lang, section])


config = Config("settings")
json_config = JsonConfig("settings")
