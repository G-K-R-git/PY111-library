import library


def main():
    library.main_menu()
    while True:
        res = library.choose_menu()
        if res == "exit":
            # library.clear_all_library()
            exit()
        if res == "search":
            while res != "stop":
                res = library.find_book()[0]
            if res == "stop":
                res = "exit"


    # library.add_book("Homo sapiens", "Yuval Harari", 2011, "Dvir Publishing House Ltd.", 443)

if __name__ == '__main__':
    main()