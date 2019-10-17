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
from mongo.projects.ej1_arts import execute as ej1_arts
from mongo.projects.ej2_restaurant import execute as ej2_restaurant
from mongo.projects.ej3_twitter import execute as ej3_twitter
from mongo.projects.ej4_primer_dataset import execute as ej4_primer_dataset
from mongo.projects.ej5_inventory import execute as ej5_inventory
from mongo.projects.ej6_primer_dataset import execute as ej6_primer_dataset


# =======================
#     MENUS FUNCTIONS
# =======================


# Main menu
def main_menu():
    os.system('clear')

    print("Bienvenido,\n")
    print("Selecciona la ejecución deseada:\n")
    print("1. PRÁCTICA FINAL")
    print("2. Ejercicios día 1 (arts)")
    print("3. Ejercicios día 2 (restaurant)")
    print("4. Ejercicios día 3 (tweet)")
    print("5. Ejercicios día 4 (full-primer_dataset)")
    print("6. Ejercicios día 5 (inventory)")
    print("7. Ejercicios día 6 (full-primer_dataset)")
    print("\n0. Quitar")
    choice = input(" >>  ")
    exec_menu(choice)

    return


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


# MenUs
def menu1():
    print("Ejecutando práctica final !\n")
    practica()
    print("\n9. Atrás")
    print("0. Quitar")
    choice = input(" >>  ")
    exec_menu(choice)
    return


def menu2():
    print("Ejercicios día 1 !\n")
    ej1_arts()
    print("\n9. Atrás")
    print("0. Quitar")
    choice = input(" >>  ")
    exec_menu(choice)
    return


def menu3():
    print("Ejercicios día 2 !\n")
    ej2_restaurant()
    print("\n9. Atrás")
    print("0. Quitar")
    choice = input(" >>  ")
    exec_menu(choice)
    return


def menu4():
    print("Ejercicios día 3 !\n")
    ej3_twitter()
    print("\n9. Atrás")
    print("0. Quitar")
    choice = input(" >>  ")
    exec_menu(choice)
    return


def menu5():
    print("Ejercicios día 4 !\n")
    ej4_primer_dataset()
    print("\n9. Atrás")
    print("0. Quitar")
    choice = input(" >>  ")
    exec_menu(choice)
    return


def menu6():
    print("Ejercicios día 5 !\n")
    ej5_inventory()
    print("\n9. Atrás")
    print("0. Quitar")
    choice = input(" >>  ")
    exec_menu(choice)
    return


def menu7():
    print("Ejercicios día 6 !\n")
    ej6_primer_dataset()
    print("\n9. Atrás")
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
    '3': menu3,
    '4': menu4,
    '5': menu5,
    '6': menu6,
    '7': menu7,
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

