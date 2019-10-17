from pprint import pprint


def exercise_decorator(text):
    """
    Exercise decorator to show the introduction text of the query
    :param text: Text ot be shown
    """
    def execute(function):
        def query(collection):
            string_to_expand = '-'
            new_text = "#### **{0}**: {1}".format(collection.name.upper(), text)
            header = (string_to_expand * (int(len(new_text) / len(string_to_expand)) + 1))[:len(new_text)]
            print("\n{0}\n{1}\n".format(header, new_text))
            return function(collection)
        return query
    return execute


def print_elements(function):
    """
    Decorator used to show the documents returned by the query
    """
    def wrapper(collection):
        input("Enter para ver >> ")
        res = function(collection)
        print('```json')
        for i in res:
            pprint(i)
        print('```')
        return res
    return wrapper


def count_decorator(function):
    """
    Decorator used to show the count of documents retuned by the query
    """
    def wrapper(collection):
        res = function(collection)
        print("\n{0} documento/s".format(res.count()))
        return res
    return wrapper


