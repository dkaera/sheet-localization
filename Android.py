import os

ANDROID_LOCALIZATION_DIR_NAME_EN = "android/res/values"
ANDROID_LOCALIZATION_DIR_NAME_MASK = "android/res/values-{0}"
ANDROID_LOCALIZATION_FILE_NAME = "strings.xml"
ANDROID_PLURAL_LOCALIZATION_FILE_NAME = "plurals.xml"

ANDROID_LOCALIZATION_HEADER = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<resources " \
                              "xmlns:tools=\"http://schemas.android.com/tools\" tools:ignore=\"UnusedQuantity\">\n "
ANDROID_LOCALIZATION_FORMAT = "\t<string name=\"{0}\">{1}</string>\n"
ANDROID_PLURAL_LOCALIZATION_FORMAT = "\t<plurals name=\"{0}\">\n"
ANDROID_PLURAL_LOCALIZATION_END_FORMAT = "\t</plurals>\n"
ANDROID_PLURAL_ITEM_LOCALIZATION_END_FORMAT = "\t\t<item quantity=\"{0}\">{1}</item>\n"
ANDROID_LOCALIZATION_FOOTER = "</resources>"


def android_generate_localization_files(translations, languages):
    for languageId in range(0, len(languages)):
        language = languages[languageId]
        dirName = ANDROID_LOCALIZATION_DIR_NAME_EN
        if language != "en":
            if language == "es-419":
                language = language.replace("-419", "")
            dirName = ANDROID_LOCALIZATION_DIR_NAME_MASK.format(language)
        # Create localization directory if it does not exist.
        if not os.path.exists(dirName):
            # print("Creating directory '{0}'".format(dirName))
            os.makedirs(dirName)
        filePath = dirName + "/" + ANDROID_LOCALIZATION_FILE_NAME
        # print("Generating Android localization file '{0}'".format(filePath))
        with open(filePath, "w") as f:
            f.write(androidLocalization(translations, languageId))


def android_generate_plural_localization_files(plural_list, languages):
    for languageId in range(0, len(languages)):
        language = languages[languageId]
        dirName = ANDROID_LOCALIZATION_DIR_NAME_EN
        if language != "en":
            if language == "es-419":
                language = language.replace("-419", "")
            dirName = ANDROID_LOCALIZATION_DIR_NAME_MASK.format(language)
        # Create localization directory if it does not exist.
        if not os.path.exists(dirName):
            # print("Creating directory '{0}'".format(dirName))
            os.makedirs(dirName)
        filePath = dirName + "/" + ANDROID_PLURAL_LOCALIZATION_FILE_NAME
        # print("Generating Android plural localization file '{0}'".format(filePath))
        with open(filePath, "w") as f:
            f.write(androidPluralLocalization(plural_list, languageId))


def androidLocalization(translations, languageId):
    contents = ANDROID_LOCALIZATION_HEADER
    for tr in translations:
        # Ignore empty keys.
        if tr.androidKey is None or not tr.translations[languageId]:
            continue
        contents += ANDROID_LOCALIZATION_FORMAT.format(tr.androidKey, tr
                                                       .translations[languageId]
                                                       .replace('%i', '%d')
                                                       .replace('%@', '%s')
                                                       .replace("\'", "\\'")
                                                       .replace('&', '&amp;')
                                                       .encode('utf8'))
    contents += ANDROID_LOCALIZATION_FOOTER
    return contents


def androidPluralLocalization(pluralTranslations, languageId):
    contents = ANDROID_LOCALIZATION_HEADER
    for plrl in pluralTranslations:
        # Ignore empty keys.
        if plrl.androidKey is None:
            continue
        contents += ANDROID_PLURAL_LOCALIZATION_FORMAT.format(plrl.androidKey)
        plurals = plrl.plurals
        for key, value in plurals.iteritems():
            translation = value[languageId]
            if not translation:
                continue
            contents += ANDROID_PLURAL_ITEM_LOCALIZATION_END_FORMAT.format(key, translation
                                                                           .replace('%i', '%d')
                                                                           .replace('&', '&amp;')
                                                                           .replace("\'", "\\'"))
        contents += ANDROID_PLURAL_LOCALIZATION_END_FORMAT
    contents += ANDROID_LOCALIZATION_FOOTER
    return contents
