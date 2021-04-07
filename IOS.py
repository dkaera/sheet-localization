import os
import sys
from imp import reload
from itertools import groupby

reload(sys)
sys.setdefaultencoding("utf-8")

IOS_LOCALIZATION_DIR_NESTED_NAME_MASK = u"Strings/{0}/{1}.lproj"
IOS_LOCALIZATION_DIR_NAME_MASK = u"Strings/{0}.lproj"
IOS_LOCALIZATION_FILE_NAME = u"Localizable.strings"
IOS_COMMON_FILE_NAME = u"Common.strings"
IOS_LOCALIZATION_FILE_NAME_STRUCT = u"{}.strings"

IOS_PLURAL_FILE_NAME_STRUCT = u"{}_plural.stringsdict"
IOS_COMMON_PLURAL_FILE_NAME_STRUCT = u"Common_plural.stringsdict"

IOS_LOCALIZATION_GROUP_FORMAT = u"/* {0} */\n"
IOS_LOCALIZATION_FORMAT = u"\"{0}\" = \"{1}\";\n"

IOS_CONSTANTS_HEADER_HEADER = u"#import <Foundation/Foundation.h>\n\n"
IOS_CONSTANTS_HEADER_CONST_FORMAT = u"extern NSString * const {0};\n"
IOS_CONSTANTS_HEADER_DESC_START_FORMAT = u"\n/*!\n"
IOS_CONSTANTS_HEADER_DESC_END_FORMAT = u"*/\n"
IOS_CONSTANTS_HEADER_COMM_FORMAT = u"* {0}\n\n"
IOS_CONSTANTS_HEADER_LANG_FORMAT = u"* @b {0}@: {1}\n\n"

IOS_CONSTANTS_SOURCE_HEADER = u"#import \"LocalizationConstants.h\"\n\n"
IOS_CONSTANTS_SOURCE_FORMAT = u"NSString * const {0} = @\"{1}\";\n"

IOS_PLURAL_SOURCE_HEADER = u"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>\n"""
IOS_PLURAL_SOURCE_FOOTER = u"""\t</dict>
</plist>\n"""
IOS_PLURAL_SOURCE_ITEM_HEADER = """\t<key>{0}</key>
\t<dict>
\t\t<key>NSStringLocalizedFormatKey</key>
\t\t<string>%#@variable_0@</string>
\t\t<key>variable_0</key>
\t\t<dict>
\t\t\t<key>NSStringFormatSpecTypeKey</key>
\t\t\t<string>NSStringPluralRuleType</string>
\t\t\t<key>NSStringFormatValueTypeKey</key>
\t\t\t<string>d</string>\n"""
IOS_PLURAL_SOURCE_ITEM_FOOTER = u"""\t\t\t</dict>
\t\t</dict>\n"""

IOS_PLURAL_SOURCE_KEY = u"\t\t\t<key>{0}</key>\n"
IOS_PLURAL_SOURCE_STRING = u"\t\t\t<string>{0}</string>\n"


def ios_generate_localization_files(translations, languages):
    for translation in translations:
        group = translation.group
        for languageId in range(0, len(languages)):
            language = languages[languageId]
            fileName = ''
            if group:
                group_split = group.split('.')
                i = len(group_split)
                fileName = group_split[i - 1]
                dirNamePath = group.replace('.{}'.format(fileName), '')
                dirName = IOS_LOCALIZATION_DIR_NESTED_NAME_MASK.format(dirNamePath.replace('.', '/'), language)
            else:
                dirName = IOS_LOCALIZATION_DIR_NAME_MASK.format(language)
            dirName = dirName
            # Create localization directory if it does not exist.
            if not os.path.exists(dirName):
                # print("Creating directory '{0}'".format(dirName))
                os.makedirs(dirName)
            fullFileName = IOS_COMMON_FILE_NAME
            if fileName:
                fullFileName = IOS_LOCALIZATION_FILE_NAME_STRUCT.format(fileName)
            filePath = dirName + "/" + fullFileName
            # print("Generating iOS localization file '{0}' translation: {1}"
            # .format(filePath, translation.translations[languageId].encode("utf-8")))
            with open(filePath, "a") as f:
                f.write(ios_localization(translation, languageId))


def ios_localization(translation, language_id):
    contents = ""
    if translation.iosKey:
        contents += IOS_LOCALIZATION_FORMAT.format(translation.iosKey, translation.translations[language_id]).replace(
            "\n", u"\u000A")
    return contents.encode("utf-8")


def ios_generate_plural_localization_files(plural_list, languages):
    for key, groupIterator in groupby(plural_list, lambda x: x.group):
        group = list(groupIterator)
        for language_id in range(0, len(languages)):
            language = languages[language_id]
            fileName = ''
            if key:
                group_split = key.split('.')
                i = len(group_split)
                fileName = group_split[i - 1]
                dirNamePath = key[:-(len(fileName) + 1)]  # remove file name prefix from the path
                dirName = IOS_LOCALIZATION_DIR_NESTED_NAME_MASK.format(dirNamePath.replace('.', '/'), language)
            else:
                dirName = IOS_LOCALIZATION_DIR_NAME_MASK.format(language)
            # Create localization directory if it does not exist.
            if not os.path.exists(dirName):
                # print("Creating directory for plural '{0}'".format(dirName))
                os.makedirs(dirName)
            fullFileName = IOS_COMMON_PLURAL_FILE_NAME_STRUCT
            if fileName:
                fullFileName = IOS_PLURAL_FILE_NAME_STRUCT.format(fileName)
            filePath = dirName + "/" + fullFileName
            # print("plural filePath: {} group size: {}".format(filePath, len(group)))
            with open(filePath, "w") as f:
                f.write(ios_plural_localization_by_group(group, language_id))


def ios_plural_localization_by_group(group, language_id):
    contents = IOS_PLURAL_SOURCE_HEADER
    for groupItem in group:
        contents += IOS_PLURAL_SOURCE_ITEM_HEADER.format(groupItem.iosKey)
        for quantity, plural in groupItem.plurals.iteritems():
            translation = plural[language_id].encode('utf-8')
            if not translation:
                continue
            # print("key: {} quantity: {} translation: {}".format(groupItem.iosKey, quantity, translation))
            contents += IOS_PLURAL_SOURCE_KEY.format(quantity)
            contents += IOS_PLURAL_SOURCE_STRING.format(translation.replace("\n", u"\u000A"))
        contents += IOS_PLURAL_SOURCE_ITEM_FOOTER
    contents += IOS_PLURAL_SOURCE_FOOTER
    return contents
