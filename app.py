from action import listar_link_app, guardar_link_app
from src.Directoriess import Directoriess
from src.Utilitarios import Utilitarios as utils

util = utils()


def init_app():
    action = input("Que desea hacer?\n1. Listar\n2. Guardar\n>")

    if action:
        if action == "1":
            listar_link_app()
            again_menu(listar_link_app)
        elif action == "2":
            guardar_link_app()
            again_menu(guardar_link_app)
        else:
            print("Opcion inválida ❌")


def again_menu(func=None):
    again = input("Desea volver al menu?\n1. Si\n2. No\n->")
    if again == "1":
        util.clean_console()
        init_app()
    elif again == "2":
        if(func):
            util.clean_console()
            func()
            again_menu(func)
        print("Fin del programa")
    else:
        print("Opcion invalida ❌")


def main():
    util.clean_console()
    init_app()


if __name__ == "__main__":
    Directoriess().create_folder()
    main()
