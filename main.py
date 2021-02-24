import library


def main():
    try:
        library.open_file_to_read(library.filename)
    except:
        library.open_file_to_write([], library.filename)  # Создание дефолтного пустого списка если файл пустой

    library.main_menu()
    while True:
        res = library.choose_menu()
        if res == "exit":
            # library.clear_all_library()  # Удаление всех данных при каждом ране
            exit()
        if res == "search":
            while res != "stop":
                res = library.find_book()[0]
            if res == "stop":
                res = "exit"


if __name__ == '__main__':
    main()
