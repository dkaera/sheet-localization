from Translation import Translation
from Plural import Plural

CFG_KEY_ID = 0
CFG_VALUE_ID = 1
CFG_KEY_VALUE_COLUMNS_NB = 2


def configurationFromPage(page):
    cfg = {}
    rawValues = page.get_all_values()
    for row in rawValues:
        key = row[CFG_KEY_ID]
        # Only take those rows that
        # * have key value pairs
        # * have keys
        if len(key) and (len(row) >= CFG_KEY_VALUE_COLUMNS_NB):
            value = row[CFG_VALUE_ID]
            cfg[key] = value
    return cfg


def parse_page(page, cfg):
    # Get raw page values.
    raw = page.get_all_values()

    translationsColumnId = int(cfg["TRANSLATION_COLUMN"]) - 1

    # Get list of languages.
    languagesRowId = int(cfg["LANGUAGES_ROW"]) - 1
    langRow = raw[languagesRowId]
    languagesNb = len(langRow)
    languages = []
    for columnId in range(translationsColumnId, languagesNb):
        languages.append(raw[languagesRowId][columnId])

    translationRowId = int(cfg["TRANSLATION_ROW"]) - 1
    # Comments column ids.
    commentKeyColumnId = int(cfg["COMMENT_KEY_COLUMN"]) - 1
    groupKeyColumnId = int(cfg["GROUP_KEY_COLUMN"]) - 1
    # Key column ids.
    androidKeyColumnId = int(cfg["ANDROID_KEY_COLUMN"]) - 1
    iosKeyColumnId = int(cfg["IOS_KEY_COLUMN"]) - 1

    # Parse translations.
    group_name_var = ''
    translations = []
    for rowId in range(0, len(raw)):
        # Skip non-translation rows.
        if rowId < translationRowId:
            continue
        tr = Translation()
        # Comment keys.
        comment = raw[rowId][commentKeyColumnId]
        tr.comment = comment if len(comment) else None
        group_key = raw[rowId][groupKeyColumnId]
        group_name_var = group_key if len(group_key) else group_name_var
        # print('parsed group name {}'.format(group_name_var))
        tr.group = group_name_var
        # Platform keys.
        androidKey = raw[rowId][androidKeyColumnId]
        tr.androidKey = androidKey if len(androidKey) else None
        ios_key = raw[rowId][iosKeyColumnId]
        tr.iosKey = ios_key if len(ios_key) else None
        # Get translations.
        for columnId in range(translationsColumnId, languagesNb):
            tr.translations.append(raw[rowId][columnId])
        translations.append(tr)
    return languages, translations


def parse_plural_page(page, cfg):
    # Get raw page values.
    raw = page.get_all_values()
    translationRowId = int(cfg["PLURAL_TRANSLATION_ROW"]) - 1
    androidKeyColumnId = int(cfg["PLURAL_ANDROID_KEY_COLUMN"]) - 1

    languagesRowId = int(cfg["PLURAL_LANGUAGES_ROW"]) - 1
    langRow = raw[languagesRowId]
    languagesNb = len(langRow)

    translationsColumnId = int(cfg["PLURAL_TRANSLATION_COLUMN"]) - 1
    quantityColumnId = int(cfg["PLURAL_QUANTITY_COLUMN"]) - 1
    # Comments column ids.
    commentKeyColumnId = int(cfg["PLURAL_COMMENT_KEY_COLUMN"]) - 1
    groupKeyColumnId = int(cfg["PLURAL_GROUP_KEY_COLUMN"]) - 1
    # Key column ids.
    androidKeyColumnId = int(cfg["PLURAL_ANDROID_KEY_COLUMN"]) - 1
    iosKeyColumnId = int(cfg["PLURAL_IOS_KEY_COLUMN"]) - 1

    plurals = []
    plrlVar = Plural()
    plural_group = None
    for rowId in range(0, len(raw)):
        if rowId < translationRowId:
            continue
        android_key = raw[rowId][androidKeyColumnId]
        ios_key = raw[rowId][iosKeyColumnId]
        if (android_key and android_key != plrlVar.androidKey) or (ios_key and ios_key != plrlVar.iosKey):
            if plrlVar.androidKey is not None or plrlVar.iosKey is not None:
                # print("append : '{}'".format(plrlVar.group))
                plurals.append(plrlVar)
                plrlVar = Plural()
        plrlVar.androidKey = android_key if len(android_key) else plrlVar.androidKey
        plrlVar.iosKey = ios_key if len(ios_key) else plrlVar.iosKey
        # Comment keys.
        comment = raw[rowId][commentKeyColumnId]
        plrlVar.comment = comment if len(comment) else plrlVar.comment
        quantity = raw[rowId][quantityColumnId]
        group_key = raw[rowId][groupKeyColumnId]
        if group_key:
            plural_group = group_key
        plrlVar.group = plural_group
        # print("plrlVar.group : '{}'".format(plrlVar.group))
        # Get plurals.
        translations = []
        for columnId in range(translationsColumnId, languagesNb):
            # Parse plural translation value here
            translations.append(raw[rowId][columnId])
        plrlVar.plurals[quantity] = translations
    if plrlVar:
        # print("append : '{}'".format(plrlVar.group))
        plurals.append(plrlVar)
    return plurals
