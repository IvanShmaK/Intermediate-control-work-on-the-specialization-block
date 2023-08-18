import json
import os
import time


class Note:  # класс Заметка
    def __init__(self, name: str, note_text: str, date: str):
        self.name = name  # заголовок заметки
        self.note_text = note_text  # тело заметки
        self.date = date  # дата и время создания или последнего изменения заметки

    def __str__(self):
        return (f'Заголовок: {self.name}\n\tЗаметка: {self.note_text}\n'
                f'\tДата и время создания или последнего изменения заметки: {self.date}')

    def note_name(self) -> str:  # функция, которая возвращает название заметки
        return self.name

    def note_body(self) -> str:  # функция, которая возвращает тело заметки
        return self.note_text

    def note_date(self) -> str:  # функция, которая возвращает дату и время создания или последнего изменения заметки
        return self.date


class NoteBook:
    def __init__(self, path: str = 'Note_book.json'):
        self.path = path
        self.note: list[Note] = []

    def open_file(self):  # функция, которая извлекает список словарей-заметок из файла json, и формирует список
        # строк-заметок
        with open(self.path, 'r', encoding='UTF-8') as read_file:
            data = json.load(read_file)
        self.note = []
        for note in data:
            for key, value in note.items():
                self.note.append(Note(value[0], value[1], key))

    def size(self):  # функция, определяющая длину списка заметок
        return len(self.note)

    def __str__(self):  # функция, позволяющая напечатать записную книжку с нумерацией заметок
        note_list = []
        for i, note in enumerate(self.note, 1):
            note_list.append(note.__str__())
            note_list[i - 1] = f'{i: ^3} ' + note_list[i - 1]
        return '\n'.join(note_list) if self.note else ' ' * 24 + 'Записная книжка пуста!'

    def add_note(self, data: dict[str, str]):  # функция по добавлению заметки
        self.note.insert(0, Note(*[item for item in data.values()]))

    def change(self, ind: int, note: dict[str, str]) -> Note:  # функция по изменению заметки
        cur = self.note[ind]  # из списка заметок выбираем ту, которую нужно изменить
        cur_dict = {'name': Note.note_name(cur), 'text': Note.note_body(cur),  # и переводим её в словарь
                    'date': Note.note_date(cur)}
        cur_dict.update(note)  # дополняем заметку-словарь новыми данными
        result = self.note.pop(ind)  # удаляем выбранную заметку из списка
        self.note.insert(0, Note(*[item for item in cur_dict.values()]))  # и заменяем её на измененную
        return result  # возвращаем удаленную заметку

    def delete_note(self, ind: int):  # функция по удалению заметки
        return self.note.pop(ind)

    def search_note(self, word: str) -> list[str]:  # функция по поиску заметки
        notes_list = []
        for note in self.note:
            if word.lower() in Note.note_name(note).lower() or \
                    word.lower() in Note.note_body(note).lower() or \
                    word.lower() in Note.note_date(note).lower():
                notes_list.append(note.__str__())
        return notes_list

    def save_file(self):  # функция по сохранению заметок
        nb_list = []
        for note in self.note:
            temp_dict = {Note.note_date(note): [Note.note_name(note), Note.note_body(note)]}
            nb_list.append(temp_dict)
        with open('Note_book.json', 'w', encoding='UTF-8') as write_file:
            json.dump(nb_list, write_file, ensure_ascii=False)

    def search_notes_for_sample(self, date_less_year: list[str], date_big_year: list[str]) -> list[str]:
        # функция, которая формирует список заметок для выборки по дате
        notes_list = []
        for note in self.note:
            if int(date_less_year[0]) <= int(note.note_date()[:4]) <= int(date_big_year[0]) and \
                    int(date_less_year[1]) <= int(note.note_date()[5:7]) <= int(date_big_year[1]) and \
                    int(date_less_year[2]) <= int(note.note_date()[8:10]) <= int(date_big_year[2]):
                notes_list.append(note.__str__())
        return notes_list


def last_date():
    path = r"Note_book.json"
    ti_m = os.path.getmtime(path)
    m_ti = time.ctime(ti_m)
    t_obj = time.strptime(m_ti)  # Используем строку временной метки для создания временного объекта/структуры
    t_stamp = time.strftime("%Y-%m-%d %H:%M:%S", t_obj)  # Преобразуем объект time в временную метку в формате ISO 8601
    return t_stamp


def is_year_leap(year: int) -> bool:  # проверка года на високосность
    return year % 4 == 0 and (year % 400 == 0 or year % 100 != 0)


def is_date_correct(date: list[str]) -> bool:  # проверка правильности введенной даты
    return date[0].isdigit() and date[1].isdigit() and date[2].isdigit() and \
           int(date[0]) < 2024 and \
           0 < int(date[1]) < 13 and \
           0 < int(date[2]) and \
           ((int(date[2]) <= 31 and (int(date[1]) == 1 or int(date[1]) == 3 or int(date[1]) == 5 or int(date[1]) == 7
                                     or int(date[1]) == 8 or int(date[1]) == 10 or int(date[1]) == 12)) or
               (int(date[2]) <= 30 and (int(date[1]) == 4 or int(date[1]) == 6 or int(date[1]) == 9 or
                                        int(date[1]) == 11)) or
               (int(date[1]) == 2 and int(date[2]) <= 28 and not is_year_leap(int(date[0]))) or
               (int(date[1]) == 2 and int(date[2]) <= 29 and is_year_leap(int(date[0]))))

