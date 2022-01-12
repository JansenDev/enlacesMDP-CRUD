import sys
from src.Directoriess import Directoriess
from src.Repository import Repository
from src.LinkwebModel import Linkweb
from src.Utilitarios import Utilitarios as Util
from colorama import Fore

dir_os = Directoriess()
repository = Repository()
util = Util()

SAVE_LINK_TEXT_OUTPUT = "\nAgregar un enlace:\nExample: myKey 'https://www.google.com' --tags param1,param2,paramN  --title  'My Title Web'\n-> "
EDIT_LINK_TEXT_OUTPUT = "\nEditar un enlace:\nExample: myKey 'https://www.google.com' --tags param1,param2,paramN  --title  'My Title Web'\n-> "
LIST_LINK_TEXT_OUTPUT = "\nRecuperar enlaces:myKey --tags tag1,tag2 --per-page 4\n-> "

def guardar_link_app(replace_mode:bool=False) -> bool:
    try:
        TEXT_OUPUT = SAVE_LINK_TEXT_OUTPUT if not replace_mode else EDIT_LINK_TEXT_OUTPUT

        link_input: str = input(TEXT_OUPUT)

        util.clean_console()
        link_input_formated_toDict = Linkweb().to_Key_JSON(link_input)

        if link_input_formated_toDict != {}:
            result_dict: dict = link_input_formated_toDict["result"]
            url_input: str = link_input_formated_toDict["result"]['url']
            key_hash = util.to_hash_256(link_input_formated_toDict["key"])

            data_linkList = repository.listarDATA(key_hash)

            # ^replace_mode: If url exist in db = Exception and replace_mode = True

            status, new_dataLink_dict, new_dataLink_list = repository.existUrlValue_inList(
                data_linkList, result_dict)

            if(replace_mode):

                if not status:
                    raise Exception(f"URL: '{ url_input }' no encontrada")

                is_success = repository.guardarData(
                    key_hash, new_dataLink_list)

                if(is_success):
                    print(Fore.GREEN + "\n*Editado con éxito ✅"+Fore.WHITE)

                return True

            if status and not replace_mode:
                raise Exception(f"Url: '{url_input}' exist!.")
            # ^replace_mode END

            data_linkList.append(result_dict)

            is_success = repository.guardarData(key_hash, data_linkList)

            if(is_success):
                print(Fore.GREEN + "\n*Guardado con éxito ✅"+Fore.WHITE)
                return True

        return False
    except Exception as e:
        print(Fore.RED + f"\n*{e}"+Fore.WHITE)
        # print(e)



def listar_link_app():
    try:

        link_input = input(LIST_LINK_TEXT_OUTPUT)

        if link_input == "q" or link_input == "Q" or link_input.strip() == "":
            util.clean_console()
            raise Exception("")

        key_tags_tuple = util.get_key_And_tags_ofString(link_input)

        if key_tags_tuple == None or key_tags_tuple == ():

            print(f"{util.bar_template(50)}")
            listar_link_app()

        key, tagsList, page = key_tags_tuple

        util.clean_console()
        key_hash = util.to_hash_256(key)

        data_linkList = repository.listarDATA(key_hash)

        data_Result = repository.filter_byTags(
            data_linkList,
            current_page=0,
            limit_per_page=page,
            filter_tags_per=tagsList,
        )
        # * Print in console
        current_page = str(1)
        total_pages = data_Result["total_pages"]
        page_totalPages = f"{current_page}/{total_pages}"

        util.page_bar_template(page_totalPages)
        util.pretty_print_listOfDict(data_Result["docs"])

        if data_Result["is_next_page"]:
            keyboard = True
            num_page = 1
            while keyboard and data_Result["is_next_page"]:

                print("\n+Enter para la siguiente página...")

                key_pressed = input("+'q' para salir-> ")
                print("")

                if key_pressed == "q" or key_pressed == "Q":
                    keyboard = False
                    util.clean_console()
                    break

                data_Result = repository.filter_byTags(
                    data_linkList,
                    current_page=num_page,
                    limit_per_page=page,
                    filter_tags_per=tagsList,
                )
                # * Print in console
                current_page = str((num_page + 1))
                page_totalPages = f"{current_page}/{total_pages}"

                util.page_bar_template(page_totalPages)
                util.pretty_print_listOfDict(data_Result["docs"])
                num_page += 1
                # print(data_Result['docs'])

        if not data_Result["is_next_page"]:
            print(f"\n-Fin de la lista\n{util.bar_template(50)}\n")

    except Exception as e:
        print(e)


# guardar_link_app(True)
