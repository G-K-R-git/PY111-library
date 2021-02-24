import json
import os
import re


directory_path = os.path.dirname(__file__)  # Подразумевается, что фал будет лежать в каталоге проекта
filename = os.path.join(directory_path, "TestFile.json")
number_of_fields_for_one_book = 5


def main_menu():
    """
    Main menu
    """
    print("Hello! Here is a simple realisation of book library")
    library = open_file_to_read(filename)
    print(f"Now in library is about {len(library)} books")
    print("="*50)


def choose_menu():
    """
    Menu for choose btw find book | add book | exit
    :return: flag for main cycle
    """
    print("Here are some options:")
    print("1: Find book | 2: Add book | 0: Exit")
    answers = ["1", "2", "0"]
    print("Choose what do you want to do:", end=' ')
    while True:
        chose = input()
        while chose not in answers:
            print("Type int number 1, 2 or 0, please: ", end="")
            chose = input()
        chose_1 = chose
        if chose_1 not in answers:
            print("Incorrect input, try again")
        elif chose_1 == answers[0]:  # Поиск книги
            found_books = None
            while not found_books == "stop":
                found_books = find_book()
                return found_books[0]
        elif chose_1 == answers[1]:  # Добавление книги
            new_book = add_book_dialog()
            if not new_book:
                print("Book adding cancelled")
                print("=" * 50)
            else:
                library_data = open_file_to_read(filename)
                for book in library_data:
                    if book == new_book:
                        print("Such book already exists! Exiting book addition...")
                        print("=" * 50)
                        return "continue"
                library_data.append(new_book)
                open_file_to_write(library_data, filename)
                print("Book added!")
                print("=" * 50)
            return "continue"
        elif chose_1 == answers[2]:  # Выход
            print()
            print("="*50, "\n", "{:^50}".format("Bye-bye! See you"))
            return "exit"


def open_file_to_read(path):
    """
    Open file to read
    :param path: path to the file
    :return: list with all library data
    """
    with open(path, 'r') as file:
        library_data = json.load(file)
        return library_data


def open_file_to_write(data, path):
    """
    Open file to write
    :param data: data to write
    :param path: path to the file
    """
    with open(path, 'w') as file:
        json.dump(data, file)


def add_book_dialog():
    """
    Dialog and logic to ADD book
    :return: flag to main cycle
    """
    print("Enter book name :", end=" ")
    book_name = input()
    while not book_name:
        print("Enter something! Name can't be <blank>!", end='')
        book_name = input()
    print("Enter book author :", end=" ")
    author = input()
    while not author:
        print("Enter something! Author can't be <blank>!", end='')
        author = input()
    print("Enter the year of publishing (just press <enter> to skip):", end=" ")
    year = input()
    print("Enter publisher name (just press <enter> to skip):", end=" ")
    publisher = input()
    print("Enter pages count (just press <enter> to skip):", end=" ")
    pages_count = input()
    new_book = [book_name, author, year, publisher, pages_count]
    print("\nYou are trying to add the next book:")
    print(f"Book name: {new_book[0]}\nAuthor: {new_book[1]}\n"
          f"The year of publishing: {new_book[2]}\nPublisher name: {new_book[3]}\n"
          f"Pages count: {new_book[4]}\n")
    print("Type '1' to confirm or '0' to exit: ", end="")
    made_decision = input()
    while True:
        if made_decision == "1":
            return new_book
        elif made_decision == "0":
            return None
        else:
            print("Incorrect input, try again!")
            made_decision = input()


def find_book():
    """
    Dialog and logic for FIND book
    :return: flag to main cycle
    """
    print("To search book, type <book name> or <author name> or <year> or <publisher name>"
          " or <number of pages> or smth else.\n"
          "You can use as many words as you want.\n"
          "OR simply press <Enter> to exit search:")
    answered = None
    while not answered:
        search_phrase = input()
        if search_phrase:
            answered = True
        else:
            return continue_or_exit()
    search_pattern = search_phrase.split(" ")
    library_data = open_file_to_read(filename)
    found_books = []
    found_book_numbers = []
    book_number = 1  # Номера книг начинаем с первой
    for book in library_data:
        if book in found_books:
            pass
        else:
            for field in book:
                for part in search_pattern:
                    if re.search(part, field):
                        if book not in found_books:
                            found_books.append(book)
                            found_book_numbers.append(book_number-1)
        book_number += 1
    if not found_books:  # Книг по такому запросу не нашлось
        print("Nothing found! Try another inquiry?")
        return continue_or_exit()
    else:  # Книга(ги) найдена(ны)
        print("Here is what was found:")
        i = 1
        for book in found_books:
            print(f"{i}) {book}, (number in library: {found_book_numbers[i-1]+1})")
            i += 1
        print("Do you want to <edit> or <delete> one of the found books?")
        print("Type <1> to Edit, <2> to Delete or <3> to Continue: ", end="")
        decision_made = input()
        while decision_made not in ("1", "2", "3"):
            print(f"Try to type correct number, user!")
            decision_made = input()
        if decision_made == "1":  # Изменение книги
            edit_book(library_data, found_book_numbers)
            return continue_or_exit()
        elif decision_made == "2":  # Удаление книги
            delete_book(library_data, found_book_numbers)
            return continue_or_exit()
        else:
            return continue_or_exit()


def continue_or_exit():
    """
    Short dialog for continue or exit
    :return:  flag to main cycle
    """
    print("Type <1> to search once more, or <0> to exit: ", end="")
    while True:
        decision_made = input()
        if decision_made == "1":
            return "search", None
        elif decision_made == "0":
            return ["stop"]
        else:
            print("Type <1> or <0>: ", end="")


def delete_book(library, book_numbers):
    """
    Dialog and logic for DELETE
    :param library: library data
    :param book_numbers: GLOBAL numbers of found books in library
    :return: flag
    """
    print("What book do you want to delete? Insert its' number: ", end="")
    correct = False
    while not correct:
        to_delete = input()
        for i in to_delete:
            if ord(i) < ord("0") or ord(i) > ord("9"):
                print("Incorrect input!")
                to_delete = input()
        if int(to_delete) < 0 or int(to_delete) > len(book_numbers):
            print("Out of range! Type correct number! ", end="")
        else:
            correct = True
    print(f"Are you shure you want to delete this book?:"
          f" {library[book_numbers[int(to_delete)-1]]}\nType Yes or No: ", end="")
    yes_or_no = input()
    while yes_or_no not in ("Yes", "No"):
        print("Type Yes or No")
        yes_or_no = input()
    if yes_or_no == "Yes":
        print("Book deleted")
        library = open_file_to_read(filename)
        library.pop(book_numbers[int(to_delete)-1])
        open_file_to_write(library, filename)
        print("=" * 50)
        return "deleted"
    else:
        print("Book did not deleted")
        print("=" * 50)
        return "not deleted"


def edit_book(library, book_numbers):
    """
    Dialog and logic for EDIT
    :param library: library data
    :param book_numbers: GLOBAL numbers of found books in library
    :return: flag
    """
    print("What book do you want to edit? Insert its' number or <0> to exit: ", end="")
    correct = False
    while not correct:
        to_edit = input()
        for i in to_edit:
            if ord(i) < ord("0") or ord(i) > ord("9"):
                print("Incorrect input!")
                to_edit = input()
        if int(to_edit) < 0 or int(to_edit) > len(book_numbers):
            print("Out of range! Type correct number! ", end="")
        elif to_edit == "0":
            return "stop_editing"
        else:
            correct = True
    edited_book = library[book_numbers[int(to_edit) - 1]]
    print("You want to edit this book:")
    print(f"Book name: {edited_book[0]}\nAuthor: {edited_book[1]}\n"
          f"The year of publishing: {edited_book[2]}\nPublisher name: {edited_book[3]}\n"
          f"Pages count: {edited_book[4]}\n")
    saved = False
    while not saved:
        print(f"What field do you want to edit (choose btw 1 - {number_of_fields_for_one_book}): ", end="")
        chose = input()
        answers = [f"{i+1}" for i in range(number_of_fields_for_one_book)]
        correct = False
        while not correct:
            if chose not in answers:
                print("Choose correct field number: ", end="")
                chose = input()
            else:
                correct = True
        print("Input new info: ", end="")
        edited_book[int(chose)-1] = input()
        print("Do you want to correct another field (<1>), save book (<2>) or exit (<0>)?: ", end="")
        decision_made = input()
        while decision_made not in ("1", "2", "0"):
            print(f"Try to type correct number, user!")
            decision_made = input()
        if decision_made == "1":  # Изменение другого поля
            saved = False
        elif decision_made == "2":  # Сохранение изменений
            saved = True
        else:  # Выход
            return "search"
    library[book_numbers[int(to_edit) - 1]] = edited_book
    open_file_to_write(library, filename)
    print("Book edited!")
    print("=" * 50)


def clear_all_library():  # Handle with care
    library_data = ""
    open_file_to_write(library_data, filename)
    print("† LIBRARY CLEARED †")
