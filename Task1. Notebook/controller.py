# файл, осуществляющий взаимодействие между model.py и view.py
from json import JSONDecodeError

import view
import model
import text_fields as tf


def start():
    nb = model.NoteBook()
    try:
        nb.open_file()  # записная книжка открывается при запуске программы
        view.print_message(tf.open_successful)
    except FileNotFoundError:
        view.print_message(tf.file_not_found)
    except JSONDecodeError:
        view.print_message(tf.note_book_empty)
    while True:
        choice = view.main_menu()
        match choice:
            case 1:  # Просмотреть все заметки
                if nb:  # здесь и далее - проверка на то, не пуста ли записная книжка
                    view.show_notes(nb, '')
                else:
                    view.print_message(tf.note_book_empty)
            case 2:  # Сделать выборку заметок по дате
                if nb:
                    while True:
                        view.print_message(tf.sampling_by_date_start)
                        user_date_start = view.input_date(tf.date)
                        if model.is_date_correct(user_date_start):
                            view.print_message(tf.sampling_by_date_finish)
                            user_date_finish = view.input_date(tf.date)
                            if model.is_date_correct(user_date_finish):
                                nb_sampled = model.NoteBook.search_notes_for_sample(nb, user_date_start, user_date_finish)
                                view.show_notes(nb_sampled, '')
                                break
                            else:
                                view.print_message(tf.wrong_date)
                        else:
                            view.print_message(tf.wrong_date)
                else:
                    view.print_message(tf.note_book_empty)
            case 3:  # Добавить заметку
                new_note = view.input_notes(tf.new_note)  # добавить заметку можно, даже если записная книжка пуста
                nb.add_note(new_note)
                view.print_message(tf.add_successful)
            case 4:  # Найти заметку
                if nb:
                    key_word = view.search_word()
                    note = nb.search_note(key_word)
                    view.show_notes(note, tf.dont_found)
                else:
                    view.print_message(tf.note_book_empty)
            case 5:  # Редактировать заметку
                if nb:
                    view.show_notes(nb, '')  # показываем список заметок
                    choice = view.input_choice(nb.size(), tf.change_choice) - 1  # выбираем, какую заметку изменить
                    change_note = view.input_notes(tf.change_note)  # пишем новые данные заметки
                    res = nb.change(choice, change_note)  # заменяем старые данные на новые
                    view.print_message(tf.changed(model.Note.note_name(res)))  # пишем, что данная заметка изменена
                else:
                    view.print_message(tf.note_book_empty)
            case 6:  # Удалить заметку
                if nb:
                    view.show_notes(nb, '')
                    choice = view.input_choice(nb.size(), tf.del_note) - 1
                    res = nb.delete_note(choice)
                    view.print_message(tf.deleted(model.Note.note_name(res)))
                else:
                    view.print_message(tf.note_book_empty)
            case 7:  # Сохранить заметку/изменения
                nb.save_file()
                view.print_message(tf.saved)
            case 8:  # Выход
                break
