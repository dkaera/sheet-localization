class Plural(object):
    def __init__(self):
        self.androidKey = None
        self.iosKey = None
        self.comment = None
        self.group = None
        self.plurals = {}

    def __str__(self):
        return "Plural group: {} androidKey: {} iosKey: {} comment: {} translations: {}".format(self.group,
            self.androidKey, self.iosKey, self.comment, self.plurals)

