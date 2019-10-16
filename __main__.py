# -*- coding: utf-8 -*-
# title           :__main__.py
# description     :MenU para la ejecuciOn de las prActicas de Bases De Datos NoSQL
# author          :Sergio Del Castillo Baranda
# date            :
# version         :0.1
# usage           :python -m mongo
# notes           :
# python_version  :3.6
# =================================================================================

import sys
import os
from mongo.projects.practica import execute as practica


# =======================
#     MENUS FUNCTIONS
# =======================


# Main menu
def main_menu():
    os.system('clear')

    print("Welcome,\n")
    print("Please choose the menu you want to start:")
    print("1. Practica")
    print("2. Ejercicios día 1")
    print("\n0. Quitar")
    choice = input(" >>  ")
    exec_menu(choice)

    return


# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print("Selección incorrecta, intentalo de nuevo.\n")
            menu_actions['main_menu']()
    return


# Menu 1
def menu1():
    print("Ejecutando prActica !\n")
    practica()
    print("\n9. AtrAs")
    print("0. Quitar")
    choice = input(" >>  ")
    exec_menu(choice)
    return


# Menu 2
def menu2():
    print("Ejercicio dIa 1 !\n")
    print("\n9. AtrAs")
    print("0. Quitar")
    choice = input(" >>  ")
    exec_menu(choice)
    return


# Back to main menu
def back():
    menu_actions['main_menu']()


# Exit program
def exit():
    sys.exit()

# =======================
#    MENUS DEFINITIONS
# =======================


# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '9': back,
    '0': exit,
}

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    #  Launch main menu
    main_menu()

