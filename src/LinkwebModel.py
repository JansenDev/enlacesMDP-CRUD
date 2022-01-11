# import sys, os

# sys.path.append(
#     os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# )

from src.Utilitarios import Utilitarios


class Linkweb:
    def __init__(self, link_web=None) -> None:
        self.link_web = link_web

    def to_Key_JSON(self, link_web=None) -> dict:
        result_dict = {}
        try:
            link_web = link_web if link_web else self.link_web

            key = Utilitarios().get_keyName(link_web)
            url = Utilitarios().get_url(link_web)
            tagsList = Utilitarios().get_tagsList(link_web)
            title = Utilitarios().get_title(link_web)
            date = Utilitarios().date_today_rfc3339()

            self.key = key
            self.url = url
            self.tagsList = tagsList
            self.title = title
            self.data = date

            if url is None or tagsList is None:
                return {}

            if title != None:
                result_dict["title"] = title

            result_dict["url"] = url
            result_dict["tags"] = tagsList
            result_dict["created_at"] = date

            return {"key": key, "result": result_dict}

        except:
            return {}