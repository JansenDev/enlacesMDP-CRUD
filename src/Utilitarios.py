import re
import os
import sys
from datetime import datetime, timezone
import hashlib
from colorama import Fore
import locale

from colorama.ansi import AnsiFore


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)


key_rgx = r"\w+"
url_rgx = r"(?<=[\w0-9])\s+(\"|\').+(\"|\')(?=\s+--tags)"
tags_rgx = r"(?<=(\s--tags))(\s*\w+\,?)+"
tags_rgx = r"(?<=(\s--tags))\s{1,}([\w,]+)\s"
title_rgx = r"(?<=--title)\s+(\"|\').+(\"|\')"

# * https://www.geeksforgeeks.org | www.google.com
validate_url_rgx  = "((http|https)://)?(www.)?[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)"


class Utilitarios:
    def __init__(self):
        pass

    def date_today_rfc3339(self) -> str:
        return datetime.now(timezone.utc).astimezone().isoformat()

    def get_keyName(self, web_link: str) -> str:
        try:
            key: str = re.search(key_rgx, web_link).group().strip()
            return key
        except BaseException as e:
            print(self.add_colorama(
                "#### KEY invalid ####", Fore.RED))

    def get_url(self, web_link: str) -> str:
        try:
            url: str = (
                re.search(url_rgx, web_link)
                .group()
                .strip()
                .replace('"', "")
                .replace("'", "")
            )
            return url
        except BaseException as e:
            print(self.add_colorama(
                "#### URL invalid ####", Fore.RED))

    def get_tagsList(self, web_link: str) -> list:
        web_link = web_link + " "
        try:
            tags: str = re.search(tags_rgx, web_link).group().strip()

            if(tags[-1] == ','):
                raise Exception("Tag invalid")

            tags_to_list = tags.replace(" ", "").split(",")
            tags_to_list = [tag for tag in tags_to_list if tag != ""]

            return [tags] if len(tags_to_list) == 0 else tags_to_list
        except BaseException as e:
            print(self.add_colorama(
                "#### TAGS invalids ####", Fore.RED))
            # print("#### TAGS invalids ####")

    def get_title(self, web_link: str) -> str:
        try:
            title: str = (
                re.search(title_rgx, web_link)
                .group()
                .strip()
                .replace('"', "")
                .replace("'", "")
            )

            if(title == " "):
                return None

            return title
        except BaseException:
            pass

    def clean_console(self):
        os.system("cls")

    def to_hash_256(self, text: str):
        text = text.strip().encode("utf-8")
        hash_result = hashlib.sha256(text).hexdigest()
        return hash_result

    def get_key_And_tags_ofString(self, text: str):

        text_splitedList = []
        text = text.lower() + " "

        text_splitedList = text.split(" ")
        text_splitedList = [x.strip() for x in text_splitedList if x != ""]

        text_splitedList_size = len(text_splitedList)

        # * mdplinks --tags empresa,programación,rode |
        # * mdplinks --tags |
        # * mdplinks --tags empresa,programación,rode -per-page 10
        regex = r"^([a-zA-Z0-9]+)\s+(--tags)(\s{1,}[áéíóúÁÉÍÓÚñÑA-Za-z,]+\s)?((-per-page) (\d+(?=\s)))?"

        try:

            matches: str = re.search(regex, text)

            if text_splitedList_size == 0:
                raise Exception("Empty values entered")

            if text_splitedList_size == 1:
                raise Exception("'--tags' is required")

            if text_splitedList_size == 2 and text_splitedList[1] == "--tags":
                key: str = matches.group(1).strip()
                return key, None, None

            elif text_splitedList_size == 3:

                if text_splitedList[2] == "-per-page":
                    raise Exception("Number page required")

                if matches.group(3):

                    key: str = matches.group(1)
                    tagsList: str = matches.group(3).split(",")

                    tagsList_filtered = [tag.strip()
                                         for tag in tagsList if tag != ""]

                    return key, tagsList_filtered, None
                else:
                    raise Exception(
                        "Tags must be only words and separated by commas")

            elif text_splitedList_size == 4:
                print(text_splitedList)

                if (
                    text_splitedList[1] == "--tags"
                    and text_splitedList[2] == "-per-page"
                ):

                    if not text_splitedList[3].isdigit():
                        raise Exception("Bad parameter> " +
                                        text_splitedList[3])

                    if not type(int(text_splitedList[3])) == int:
                        raise Exception("'-per-page' only accept integers")

                    if int(text_splitedList[3]) > 50 or int(text_splitedList[3]) < 1:
                        raise Exception(
                            "'-per-page' only accept integers 1-50")

                    key: str = matches.group(1)

                    page_num: int = int(text_splitedList[3])

                    return key, None, page_num

                if text_splitedList[3] == "-per-page":
                    raise Exception("'-per-page' need a number 1 to 50")
                else:
                    raise Exception("Bad modifier: " + text_splitedList[3])

            elif text_splitedList_size == 5:

                if not text_splitedList[3] == "-per-page":
                    raise Exception("Bad modifier: " + text_splitedList[3])

                if not matches.group(3):
                    raise Exception(
                        "Tags must be words and separated by commas")

                if not text_splitedList[4].isdigit():
                    raise Exception("Bad parameter> " + text_splitedList[4])

                if not type(int(text_splitedList[4])) == int:
                    raise Exception("'-per-page' only accept integers")

                if int(text_splitedList[4]) > 50 or int(text_splitedList[4]) < 1:
                    raise Exception("'-per-page' only accept integers 1-50")

                key: str = matches.group(1)

                tagsList: list = matches.group(3).split(",")
                tagsList_filtered = [tag.strip()
                                     for tag in tagsList if tag != ""]

                page_num: int = int(matches.group(6))

                return key, tagsList_filtered, page_num

            else:
                raise Exception("Bad modifier: " + text_splitedList[1])

        except Exception as e:
            self.clean_console()
            print(Fore.RED + str(e) + Fore.WHITE)
            return ()

    def bar_template(self, n: int = 50):
        return "-" * n

    def page_bar_template(self, n: str, prefix: str = "Página"):
        print(Fore.YELLOW+"\n"+"*"*20+f"{prefix} {str(n)}"+"*"*20+Fore.WHITE)

    def pretty_print_dict(self, dictI: dict):
        print("")
        for key, value in dictI.items():

            if key == "title":
                print(f"* {value}")

            if key == "url":
                print(f"URL: {value}")

            if key == "tags":
                separator = ", "
                tags = separator.join(value)
                print(f"Etiquetas: {tags}")

            if key == "created_at":
                locale.setlocale(locale.LC_ALL, "es_ES.utf8")
                fecha = datetime.fromisoformat(value)
                fecha = datetime.strftime(
                    fecha, "%A %d de %B de %Y %H:%M:%S -05:00")
                print(f"Fecha y hora de creación: {fecha}")

        print("")

    def pretty_print_listOfDict(self, listOfDicts: list):

        for dictI in listOfDicts:
            print("-" * 50)
            self.pretty_print_dict(dictI)

    def add_colorama(self, text: str, color_start: AnsiFore = Fore.WHITE, color_end: AnsiFore = Fore.WHITE, prefix="", sufix=""):
        text_acum: str = ""
        text_acum: str = f"{prefix}"+color_start+f"{text}"+color_end+f"{sufix}"
        return text_acum
