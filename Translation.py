class Translation(object):
    def __init__(self):
        self.androidKey = None
        self.iosKey = None
        self.comment = None
        self.group = None
        self.translations = []

    def __str__(self):
        return "Translation androidKey: {} iosKey: {} comment: {} group: {} translations: {}".format(
            self.androidKey, self.iosKey, self.comment, self.group, self.translations)

