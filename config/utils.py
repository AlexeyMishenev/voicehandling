import json
import os
import time
from datetime import datetime
from os import mkdir
from os.path import dirname, exists


def most_common(lst):
    return max(lst, key=lst.count)


def cache_func(cache_file, lang):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            now = datetime.fromtimestamp(time.time())

            if not exists(dirname(cache_file)):
                mkdir(dirname(cache_file))

            data = None
            if os.path.exists(cache_file):
                with open(cache_file, 'r', encoding='utf8') as file:
                    data = json.load(file)

            if (data is not None and data["time"] == str(now.date())
                    and data['lang'] == lang):
                result = data["data"]
            else:
                result = function(*args, **kwargs)

                data = {'time': str(now.date()), 'lang': lang,
                        'data': result}
                with open(cache_file, 'w', encoding='utf8') as file:
                    json.dump(data, file, indent=4)
            return result

        return wrapper

    return real_decorator


