# файл для функций ввода и вывода
import text_fields as tf
import model


def main_menu() -> int:  # функция по выводу меню
    print(*tf.menu, sep='\n')
    return input_choice(len(tf.menu) - 1, tf.input_choice)


def input_choice(size: int, message: str):  # функция по выбору позиции меню
    while True:
        number = input(message)
        if number.isdigit() and 0 < int(number) < size + 1:
            return int(number)
        else:
            print(tf.wrong_choice(size))


def show_notes(book: model.NoteBook | list[str], message: str):  # функция по выводу заметок
    if book:
        print('\n' + '=' * 80)
        if isinstance(book, model.NoteBook):
            print(book)
        else:
            for i, note in enumerate(book, 1):
                book[i - 1] = f'{i: ^3} ' + book[i - 1]
            print('\n'.join(book))
        print('=' * 80 + '\n')
    else:
        print(message)


def print_message(message: str):  # функция по выводу сообщения
    print('\n' + '=' * len(message))
    print(message)
    print('=' * len(message) + '\n')


def input_notes(message: list[str]) -> dict[str, str]:  # функция по вводу данных для изменения заметки
    note = {}
    name = input(message[0])
    text = input(message[1])
    date = model.last_date()
    if name:
        note['name'] = name
    if text:
        note['text'] = text
    if date:
        note['date'] = date
    return note


def search_word() -> str:  # функция по вводу слова для поиска
    word = input(tf.search_key)
    return word


def input_date(message: list[str]) -> list[str]:  # функция по формированию списка из введенных года, месяца и даты
    date = [input(message[0]), input(message[1]), input(message[2])]
    return date

