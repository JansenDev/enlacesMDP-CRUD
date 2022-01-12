import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
import json
from src.Directoriess import Directoriess
from src.Constants.Constantes import CARPETA_DATA_NAME

dir_os = Directoriess()


class Repository:
    def __init__(self) -> None:
        pass

    def listarDATA(self, key: str, prettyJson=False) -> list:
        try:

            path = f"./{CARPETA_DATA_NAME}/{key}.json".format(key=key)

            with open(path, "r", encoding="utf-8") as file:
                dataList = json.load(file)

            if prettyJson:
                return json.dumps(dataList, indent=4, ensure_ascii=False)

            return dataList
        except:
            # print("No existe el archivo json Solicitado")
            print("Opps! intentalo denuevo con otros parametros: URL")
            return []

    def guardarData(self, key, data) -> any:
        try:
            # dir_os.exists_file(f"{key}.json")
            path = f"./{CARPETA_DATA_NAME}/{key}.json"
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            return True
        except:
            return False

    def listart_per_page(
        self, dataList: list, current_page: int = 0, limit_per_page: int = 25
    ) -> dict:
        docs = []
        count = 0
        dict_page_body_output = {}
        total_docs = len(dataList)
        limit_per_page = limit_per_page if limit_per_page else total_docs
        items_transcurridos = current_page * limit_per_page

        if items_transcurridos < 0:
            print("Page not must be a negative number")
            return []

        if dataList == 0:
            print("Data is empty ❌")
            return []

        # if limit > total_data:
        #     items_per_page = total_data
        #     print("Limit must be less than total data 👎")

        if items_transcurridos >= total_docs:
            print("Page not found ❌")
            return []

        dict_page_body_output["total_docs"] = total_docs
        # dict_page_body_output["items_transcurridos"] = items_transcurridos
        dict_page_body_output["current_page"] = current_page
        dict_page_body_output["limit_per_page"] = limit_per_page

        # * prev/next page
        is_next_page = (
            not items_transcurridos > total_docs
            and not (current_page + 1) * limit_per_page >= total_docs
        )

        is_prev_page = (
            not items_transcurridos == 0 and not items_transcurridos > total_docs
        )

        dict_page_body_output["is_next_page"] = is_next_page
        dict_page_body_output["is_prev_page"] = is_prev_page

        # *total page
        resto = 0
        total_pages = 0
        if not items_transcurridos == 0:
            resto = 1 if total_docs % limit_per_page > 0 else 0
        else:
            resto = 1 if total_docs % limit_per_page > 0 else 0

        total_pages = int((total_docs / limit_per_page) + resto)

        dict_page_body_output["total_pages"] = total_pages

        for index in range(items_transcurridos, total_docs):

            # print(f"[{index}]: ", dataList[index])
            link_item = dataList[index]

            docs.append(link_item)
            count += 1
            if limit_per_page and count == limit_per_page:
                break

        # dict_page_body_output["docs_size"] = count
        dict_page_body_output["docs"] = docs

        return dict_page_body_output

    #! Deprecated: listart_per_page_filter
    def listart_per_page_filter(
        self,
        dataList: list,
        current_page: int = 0,
        limit_per_page: int = 25,
        filter_tags_per: list = None,
        search_all_tags: bool = False,
    ) -> dict:
        docs = []
        count = 0
        dict_page_body_output = {}
        total_docs = len(dataList)
        limit_per_page = limit_per_page if limit_per_page else total_docs
        items_transcurridos = current_page * limit_per_page

        if items_transcurridos < 0:
            print("Page not must be a negative number")
            return []

        if dataList == 0:
            print("Data is empty ❌")
            return []

        if items_transcurridos >= total_docs:
            print("Page not found ❌")
            return []

        # dict_page_body_output["total_docs"] = total_docs
        # dict_page_body_output["items_transcurridos"] = items_transcurridos
        dict_page_body_output["current_page"] = current_page
        dict_page_body_output["limit_per_page"] = limit_per_page

        # * Set docs and docs_size
        for index in range(items_transcurridos, total_docs):

            # print(f"[{index}]: ", dataList[index])
            link_item = dataList[index]
            tags_found = self.exist_tag(
                dataList[index], args=filter_tags_per, search_all_tags=search_all_tags
            )

            if tags_found:
                docs.append(link_item)
                count += 1

            # if limit_per_page and count == limit_per_page:
            #     break

        dict_page_body_output["docs_size"] = count
        dict_page_body_output["docs"] = docs

        # *total page
        resto = 0
        total_pages = 0
        if not items_transcurridos == 0:
            resto = 1 if count % limit_per_page > 0 else 0
        else:
            # resto = 1 if count % total_docs > 0 else 0
            resto = 0

        total_pages = int((count / limit_per_page) + resto)

        dict_page_body_output["total_pages"] = total_pages

        # * prev/next page
        is_next_page = (
            not items_transcurridos > count
            and not (current_page + 1) * limit_per_page >= count
        )

        is_prev_page = not items_transcurridos == 0 and not items_transcurridos > count

        dict_page_body_output["is_next_page"] = is_next_page
        dict_page_body_output["is_prev_page"] = is_prev_page

        return dict_page_body_output

    def exist_tag(
        self, tags_dict: dict, args: list = [], search_all_tags: bool = False
    ) -> bool:
        tag_found = False
        count = 0
        total_tags = len(args)

        for tag in tags_dict["tags"]:

            if tag in args and not search_all_tags:
                tag_found = True
                break

            elif tag in args and search_all_tags:
                count += 1

                if count == total_tags:
                    tag_found = True

        return tag_found

    def filter_byTags(
        self,
        dataList: list,
        current_page: int = 0,
        limit_per_page: int = 25,
        filter_tags_per: list = None,
        search_exact_tags: bool = False,
    ):
        link_web_result = []
        count_tags = 0
        tags_filtered_byTagsList = []
        limit_per_page = limit_per_page if limit_per_page else 25

        # * return all data
        if filter_tags_per == None:
            # *paginar data
            link_web_result = self.listart_per_page(
                dataList,
                current_page=current_page,
                limit_per_page=limit_per_page,
            )
            return link_web_result

        # * Filter by tags
        for link_web in dataList:
            count_tags = 0
            for tag in link_web["tags"]:

                if tag in filter_tags_per and not search_exact_tags:
                    tags_filtered_byTagsList.append(link_web)
                    break

                # * filtrar 1 o mas tags en el mismo objeto link_web
                elif tag in filter_tags_per and search_exact_tags:
                    count_tags = count_tags + 1

                    if count_tags == len(filter_tags_per):
                        tags_filtered_byTagsList.append(link_web)

        # * paginar data filtrada
        link_web_result = self.listart_per_page(
            dataList=tags_filtered_byTagsList,
            current_page=current_page,
            limit_per_page=limit_per_page,
        )

        return link_web_result

    def existUrlValue_inList(self, link_web_List: str, newDict: dict, keyToFound="url"):

        found = False
        tmp_link_web_dict:dict = {}
        new_link_web_List:list=[]

        for index, link in enumerate(link_web_List):

            if(link[keyToFound] == newDict[keyToFound]):

                if('title' in newDict):
                    if(newDict['title'].strip() == ""):
                        del link['title']

                    # link['title'] = newDict['title']
                    tmp_link_web_dict['title']= newDict['title'].strip()

                tmp_link_web_dict['url'] = link['url']
                tmp_link_web_dict['tags'] = newDict['tags']
                tmp_link_web_dict['created_at'] = link['created_at']

                # link['tags'] = newDict['tags']
                link_web_List[index] = tmp_link_web_dict

                found = True
                # tmp_link_web = link
                new_link_web_List=link_web_List
                break

        return found, tmp_link_web_dict, new_link_web_List


# data = Repository().listarDATA("juan")
# # print(data)
# item = data[-1]
# item['title']="cambiado perrro"

# found = Repository().existUrlValue_inList(data, item)


# # print(data)
# print(found)


# x = Repository().filter_byTags(
#     data,
#     current_page=1,
#     limit_per_page=1,
#     filter_tags_per=["abc"],
#     search_exact_tags=False,
# )
# print(x)
# print("ab" in ["ab", "b"])


# data = Repository().listarDATA("juan")
# # print(data)
# x = Repository().listart_per_page_filter(
#     data, current_page=1, limit_per_page=1, filter_tags_per=["a"]
# )
# print(x)


# def tag_exists(tags_dict: dict, *args, search_all_tags: bool = False) -> bool:
# tag_found = False
# count = 0
# total_tags = len(args)

# for tag in tags_dict["tags"]:
#     print(tag)

#     if tag in args and not search_all_tags:
#         tag_found = True
#         break

#     elif tag in args and search_all_tags:
#         count += 1

#         if count == total_tags:
#             tag_found = True

#         continue

# return tag_found
