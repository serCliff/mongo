from pprint import pprint


def exercise_decorator(text):
    def execute(function):
        def query(collection):
            string_to_expand = '='
            new_text = "[{0}]: {1}".format(collection.name, text)
            header = (string_to_expand * (int(len(new_text) / len(string_to_expand)) + 1))[:len(new_text)]
            print("\n{0}\n{1}".format(header, new_text))
            return function(collection)
        return query
    return execute


def print_elements(function):
    def wrapper(collection):
        # input("Click Enter >> ")
        res = function(collection)
        for i in res:
            pprint(i)
        return res
    return wrapper


def count_decorator(function):
    def wrapper(collection):
        res = function(collection)
        print("\n{0} documento/s".format(res.count()))
        return res
    return wrapper


