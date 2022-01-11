import sys
from src.Directoriess import Directoriess
from src.Repository import Repository
from src.LinkwebModel import Linkweb
from src.Utilitarios import Utilitarios as Util
from colorama import Fore

dir_os = Directoriess()
repository = Repository()
util = Util()


def guardar_link_app():
    try:
        link_input: str = input(
            "Agregar un enlace:\nExample: myKey 'https://www.google.com' --tags param1,param2,paramN  --title  'My Title Web'\n-> "
        )
        util.clean_console()
        link_input_formated_toDict = Linkweb().to_Key_JSON(link_input)

        if link_input_formated_toDict != {}:

            key_hash = util.to_hash_256(link_input_formated_toDict["key"])

            data_linkList = repository.listarDATA(key_hash)
            data_linkList.append(link_input_formated_toDict["result"])

            is_success = repository.guardarData(key_hash, data_linkList)

            if(is_success):
                print(Fore.GREEN +"\n*Guardado con éxito ✅"+Fore.WHITE)

    except Exception as e:
        print(e)


def listar_link_app():
    try:

        link_input = input("Recuperar enlaces:\n-> ")

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
