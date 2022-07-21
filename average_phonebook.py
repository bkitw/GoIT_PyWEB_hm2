import time
from collections import UserDict
from datetime import datetime, timedelta
from itertools import islice
import pickle
import os
import re
from pathlib import Path
from random import choice
from abc import abstractmethod, ABC


class PhonebookInterface(ABC):

    @abstractmethod
    def return_message(self, key, p_or_r, *args, **kwargs):
        pass

    @abstractmethod
    def return_error(self, key, p_or_r, *args, **kwargs):
        pass


class UkrainianLang(PhonebookInterface):
    commands_dict = {
        'messages': {
            'contact_added': '|Контакт (?0) було додано до телефонної книги.|',
            'number_appended': '|Номер (?0) було додано до контакта (?1).|',
            'greeting_string': 'Введіть "hello" або "help" для додаткової інформації.\n>>>>> ',
            'enter_to_proceed': '|Натисніть ENTER, щоб продовжити...|\n',
            'number_updated': '|Номер контакту (?0) було змінено.|',
            'contact_not_found': '|Контакт (?0) не знайдено.|',
            'empty_phonebook': '|Телефонна книга пуста.|',
            'number_deleted': '|Номер (?0) контакту (?1) було успішно видалено.|',
            'contact_deleted': '|Контакт (?0) було успішно видалено.|',
            'phonebook': '--- Телефонна книга ---',
            'how_much_recs': '|Натисніть ENTER щоб відобразити усі записи.|'
                             '\nАбо введіть, скільки записів відобразити за раз: \n>>>> ',
            'wrong_recs_count': '|Ви ввели (&0) записів для відображення, '
                                'але я не можу вивести менше одного.|',
            'show_all_contact': '***\nКонтакт -- (?0);',
            'show_all_numbers': '----------------\nТелефонні номери: ',
            'show_all_bd': 'Дата народження: ',
            'not_specified': "Не вказано.",
            'end_of_phonebook': '--- Кінець телефонної книги ---',
            'contact_search': '--- Пошук контакта ---',
            'search_input': 'Введіть частину номеру, імені або email: ',
            'found_in_record': 'Знайдено у записі: (?0).',
            'not_found': '|Нічого не знайдено.|',
            'search_result': '\n--- Пошук Завершено ---',
            'email_added': '|Email (?0) додано до контакта (?1).|',
            'email_appended': '|Email (?0) додадково додано (?1).|',
            'email_updated': ' | Email (?0) змінено у контакта (?1).|',
            'email_deleted': '|Email (?0) видалено у контакта (?1).|',
            'bd_added': '|День народження (?0) задано у контакта (?1).|',
            'no_number_of_days_to_search': '|Не вказана кількість днів для розрахунку.|',
            'search_for_bd': '--- Пошук по контактах з найближчим днем народження ---',
            'bd_search_result': '|Контакт (?0) народився(-лась) (?1), до його дня народження залишилось (?2) днів.|',
            'clear_phonebook': 'Ви впевнені, що хочете очистити телефонну книгу? (y/n) ',
            'phonebook_cleared': '|Телефонна книга очищена.|',
            'phonebook_not_cleared': '|Телефонна книга не очищена.|',
            'so_long': ('Гарного дня!', 'Побачимось!', 'До зустрічі!', 'На все добре!', 'Бережіть себе!',
                        'Бувайте!', 'Прощавайте!', 'До побачення!',),
            'help': '---\n'
                    'Доступні команди:\n'
                    'add contact <name> <phone> - додати запис;\n'
                    'show all - побачити усі доступні записи;\n'
                    'show near bd <days from today to> - знайти найближчі дні народження;\n'
                    'update number <name> <old number> <new number> - змінити номер телефона;\n'
                    'append number <name> <new number> - додати додатковий номер телефона;\n'
                    'delete number <name> <number> - видалити номер телефона;\n'
                    'add email <name> <email> - додати email;\n'
                    'append email <name> <email> - додати додатковий email;\n'
                    'delete email <name> <email> - видалити email;\n'
                    'add birthday <name> <birthday "dd.mm.yyyy"> - додати день народження;\n'
                    'help - побачити цю довідку;\n'
                    'hello, hi - вітання;\n'
                    'delete contact <name> - видалення контакта;\n'
                    'find - пошук контакта;\n'
                    'clear, cls - очистити вікно;\n'
                    'clear phonebook - очистити телефонну книгу;\n'
                    'quit, q  - закрити программу;\n---',
            'greeting': '---\nВітаю! Шукаєш інформацію?\nЧим я можу допомогти?\n---',
            'goodnight': '---\nДоброї ночі!\n---',
            'goodmorning': '---\nДоброго ранку!\n---',
            'goodafternoon': '---\nДобрий день!\n---',
            'goodevening': '---\nДобрий вечір!\n---',
            'welcome': 'І ласкаво прошу до телефонної книги!\n-----',
            'command_is_unknown': '-\n|Введена команда не розпізнана. Спробуйте "help" для довідки.|\n-',
        },
        'errors': {
            'lang_not_chosen': '|Мова не обрана!|',
            'wrong_name': '-\n|Неправильний формат імені.|\n-',
            'birthday_incorrect': '-\n|Неправильний формат дати народження.|\n-',
            'not_enough_arguments': '-\n|Передано недостатньо даних.|\n-',
            'not_a_number_for_count_of_records': '-\n|Введено не цифру або число.|\n-',
            'wrong_phone_number_format': '-\n|Введений номер містить небажані символи.|\n-',
            'not_right_phone_number_to_update': '-\n|Цей контакт не має такого номеру, щоб його змінити.|\n-',
            'wrong_email_format': '-\n|Неправильний формат email.|\n-',
            'name_already_exists': '-\n|Таке ім\'я вже існує.|\n-',
            'phone_already_exists': '-\n|Номер телефону вже є в телефонній книзі.|\n-',
            'email_already_exists': '-\n|Такий email вже є в телефонній книзі.|\n-',
            'no_email_update_to': '-\n|Здається щось пішло не так.|\n-',
            'this_mail_does_not_exist': '-\n|Ви намагаєтеся змінити неіснуючий email.|\n-',

        },
    }

    def get_something(self, something, key, args, kwargs):
        string = self.commands_dict[something][key]
        for i, j in enumerate(args):
            string = string.replace(f'(?{i})', j)

        return string

    def return_message(self, key, p_or_r: bool, *args, **kwargs):
        string = self.get_something('messages', key, args, kwargs)
        if p_or_r:
            print(string)
            return ''
        else:
            return string

    def return_error(self, key, p_or_r: bool, *args, **kwargs):
        string = self.get_something('errors', key, args, kwargs)
        if p_or_r:
            print(string)
            return ''
        else:
            return string


class EnglishLang(PhonebookInterface):
    commands_dict = {
        'messages': {
            'contact_added': '|Contact (?0) was added to phonebook.|',
            'number_appended': '|Number (?0) was appended to contact (?1).|',
            'greeting_string': 'Enter "hello" or "help" for more information.\n>>>>> ',
            'enter_to_proceed': '|Press ENTER to proceed...|\n',
            'number_updated': '|This contacts phone number (?0) updated.|',
            'contact_not_found': '|Contact (?0) not found.|',
            'empty_phonebook': '|Phonebook is empty.|',
            'number_deleted': '|Number (?0) of contact (?1) successfully deleted.|',
            'contact_deleted': '|Contact (?0) successfully deleted.|',
            'phonebook': '--- Phonebook ---',
            'how_much_recs': '|Press "ENTER" to show all the records.|'
                             '\nOr enter the required quantity: \n>>>> ',
            'wrong_recs_count': '|You entered (?0) records, but I cannot show less than 1 record.|',
            'show_all_contact': '***\nContact -- (?0);',
            'show_all_numbers': '----------------\nPhone numbers: ',
            'show_all_bd': 'Date of birth: ',
            'not_specified': "Not specified.",
            'end_of_phonebook': '--- End of phonebook ---',
            'contact_search': '---Contact Search---',
            'search_input': 'Enter the part of name, number or email: ',
            'found_in_record': 'Found in record: (?0).',
            'not_found': '|Not found anything.|',
            'search_result': '\n--- Search is Complete ---',
            'email_added': '|Email (?0) added to contact (?1).|',
            'email_updated': '| Email (?0) updated in contact (?1). |',
            'email_appended': '|Email (?0) appended to contact (?1).|',
            'email_deleted': '|Email (?0) deleted from contact (?1).|',
            'bd_added': '|Birthday (?0) added to contact (?1).|',
            'no_number_of_days_to_search': '|No number of days to search.|',
            'search_for_bd': '--- Search for contacts with the upcoming birthday ---',
            'bd_search_result': '|Contact (?0) was born (?1), until his birthday left (?2) days.|',
            'clear_phonebook': 'Are you sure you want to clear the phonebook? (y/n) ',
            'phonebook_cleared': '|Phonebook cleared.|',
            'phonebook_not_cleared': '|Phonebook not cleared.|',
            'so_long': ('Have a nice day!', 'See you later!', 'Bye!', 'Goodbye!', 'See you soon!', 'See you later!',
                        'Take care!'),
            'help':
                '---\n'
                'Available commands:\n'
                'add contact <name> <phone> - adding the record;\n'
                'show all - view all saved records;\n'
                'show near bd <days from today to> - finding out about upcoming birthdays;\n'
                'update number <name> <old number> <new number> - updating phone number;\n'
                'append number <name> <new number> - adding additional phone number;\n'
                'delete number <name> <number> - delete phone number;\n'
                'add email <name> <email> - adding email;\n'
                'append email <name> <email> - adding additional email;\n'
                'delete email <name> <email> - delete email;\n'
                'add birthday <name> <birthday "dd.mm.yyyy"> - adding birthday;\n'
                'help - view this help;\n'
                'hello, hi - greetings;\n'
                'delete contact <name> - deleting the contact;\n'
                'find - searching for record;\n'
                'clear, cls - clears the window;\n'
                'clear phonebook - clears the phonebook;\n'
                'quit, q  - closing the program;\n---',
            'greeting': '---\nHi, looking for some info?\nHow can I help you?\n---',
            'goodnight': '---\nGoodnight!\n---',
            'goodmorning': '---\nGood morning!\n---',
            'goodafternoon': '---\nGood afternoon!\n---',
            'goodevening': '---\nGood evening!\n---',
            'welcome': 'And welcome to the phonebook!\n-----',
            'command_is_unknown': '-\n|Entered command is unknown. Try "help" for more information.|\n-',

        },
        'errors': {
            'lang_not_chosen': '|Language not chosen!|',
            'wrong_name': '-\n|The name is not valid!|\n-',
            'birthday_incorrect': '-\n|The birthday is not valid!|\n-',
            'not_enough_arguments': '-\n|The number of arguments is not enough.|\n-',
            'not_a_number_for_count_of_records': '-\n|The number of records is not a number.|\n-',
            'wrong_phone_number_format': '-\n|The entered number contains forbidden characters.|\n-',
            'not_right_phone_number_to_update': '-\n|This contact doesn\'t have a phone number you tried to update .|\n-',
            'wrong_email_format': '-\n|The email is not valid.|\n-',
            'name_already_exists': '-\n|The name is already exist.|\n-',
            'phone_already_exists': '-\n|The phone number is already exist in this phonebook.|\n-',
            'email_already_exists': '-\n|The email is already exist in this phonebook.|\n-',
            'no_email_update_to': '-\n|Something went wrong, I guess.|\n-',
            'this_mail_does_not_exist': '-\n|You are trying to change a non-existent email address|\n-',

        },
    }

    def get_something(self, something, key, args, kwargs):
        string = self.commands_dict[something][key]
        for i, j in enumerate(args):
            string = string.replace(f'(?{i})', j)

        return string

    def return_message(self, key, p_or_r: bool, *args, **kwargs):
        string = self.get_something('messages', key, args, kwargs)
        if p_or_r:
            print(string)
            return ''
        else:
            return string

    def return_error(self, key, p_or_r: bool, *args, **kwargs):
        string = self.get_something('errors', key, args, kwargs)
        if p_or_r:
            print(string)
            return ''
        else:
            return string


class NoEmailUpdateTo(Exception):
    """
    Exception raised when there is no email update to.
    """
    pass


class EmailAlreadyExists(Exception):
    """
    Exception raised when trying to add an email that already exists.
    """
    pass


class NameAlreadyExists(Exception):
    """
        Exception raised when a name already exist in the phonebook.
    """
    pass


class PhoneAlreadyExists(Exception):
    """
        Exception raised when a phone number already exist in the phonebook.
    """
    pass


class WrongName(Exception):
    """
    Raised when the name is not valid
    """
    pass


class BirthdayIncorrect(Exception):
    """
    Raised when the birthday is not valid
    """
    pass


class NotEnoughArguments(Exception):
    """
    Raised when the number of arguments is not enough
    """
    pass


class NotANumberForCountOFRecords(Exception):
    """
    Raised when the number of records is not a number
    """
    pass


class WrongPhoneNumberFormat(Exception):
    """
    Raised when the phone number is not valid
    """
    pass


class NotRightPhoneNumberToUpdate(Exception):
    """
    Raised when the phone number is not exist
    """
    pass


class WrongEmailFormat(Exception):
    """
    Raised when the email is not valid
    """
    pass


class ThisMailDoesNotExist(Exception):
    """
    Raised when the email is not valid
    """
    pass


def exception_handler(function):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return function(*args, **kwargs)

            except WrongName:
                lang_obj().return_error('wrong_name', True)
                time.sleep(1)
                break
            except BirthdayIncorrect:
                lang_obj().return_error('birthday_incorrect', True)
                time.sleep(1)
                break
            except NotEnoughArguments:
                lang_obj().return_error('not_enough_arguments', True)
                time.sleep(1)
                break
            except NotANumberForCountOFRecords:
                lang_obj().return_error('not_a_number_for_count_of_records', True)
                time.sleep(1)
                break
            except WrongPhoneNumberFormat:
                lang_obj().return_error('wrong_phone_number_format', True)
                time.sleep(1)
                break
            except NotRightPhoneNumberToUpdate:
                lang_obj().return_error('not_right_number_to_update', True)
                time.sleep(1)
                break
            except WrongEmailFormat:
                lang_obj().return_error('wrong_email_format', True)
                time.sleep(1)
                break
            except NameAlreadyExists:
                lang_obj().return_error('name_already_exists', True)
                time.sleep(1)
                break
            except PhoneAlreadyExists:
                lang_obj().return_error('phone_already_exists', True)
                time.sleep(1)
                break
            except EmailAlreadyExists:
                lang_obj().return_error('email_already_exists', True)
                time.sleep(1)
                break
            except NoEmailUpdateTo:
                lang_obj().return_error('no_email_update_to', True)
                time.sleep(1)
                break
            except ThisMailDoesNotExist:
                lang_obj().return_error('this_mail_does_not_exist', True)
                time.sleep(1)
                break

    return wrapper


class Record:

    def __init__(self, name, phone=None, birthday=None, email=None):
        self.name = name
        self.phones = []
        self.emails = []
        self.birthday = birthday

        if phone:
            self.add_phone(phone)

        if email:
            self.add_email(email)

    def check_phone(self, phone) -> bool:
        if str(phone) in self.phones:
            return True
        return False

    def add_phone(self, phone) -> bool:
        if not self.check_phone(phone):
            self.phones.append(str(phone))
            return True
        return False

    def update_phone(self, phone, new_phone) -> bool:
        if self.check_phone(phone):
            self.delete_phone(phone)
            self.add_phone(new_phone.value)
            return True
        raise NotRightPhoneNumberToUpdate

    def delete_phone(self, phone) -> bool:
        if self.check_phone(phone):
            self.phones.remove(str(phone))
            return True
        return False

    def check_email(self, email) -> bool:
        if str(email) in self.emails:
            return True
        return False

    def add_email(self, email) -> bool:
        if not self.check_email(email):
            self.emails.append(str(email))
            return True
        return False

    def update_email(self, email, new_email) -> bool:
        if self.check_email(email):
            self.delete_email(email)
            self.add_email(new_email.value)
            return True
        raise ThisMailDoesNotExist

    def delete_email(self, email) -> bool:
        if self.check_email(email):
            self.emails.remove(str(email))
            return True
        return False

    def append_email(self, email):
        if not self.check_email(email):
            self.emails.append(str(email))
            return True

    def check_birthday(self, birthday) -> bool:
        if birthday is not None:
            self.birthday = birthday
            return True
        return False

    def add_birthday(self, birthday) -> bool:
        if not self.check_birthday(birthday):
            self.birthday = birthday
            return True
        return False

    def __repr__(self):
        return f'{self.name} -- {self.birthday} -- {self.phones} -- {self.emails}'


class Field:
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value


class Name(Field):

    def __repr__(self):
        return self.value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if re.match(r'^[a-zA-Zа-яА-Я]+$', value):
            self.__value = value.title()
        else:
            raise WrongName


class Phone(Field):

    def __repr__(self):
        return f'{self.__value}'

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, n_value):
        n_value = n_value.strip()
        for ch in n_value:
            if ch not in "0123456789()-+":
                raise WrongPhoneNumberFormat
        self.__value = n_value


class EMail(Field):
    def __repr__(self):
        return self.value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, n_value):
        n_value = n_value.strip()
        if not re.match(r'^[a-z\d_\-.]+@[a-z\d_\-.]+\.[a-z]+$', n_value):
            raise WrongEmailFormat
        self.__value = n_value


class Birthday(Field):
    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, b_value):
        if b_value:
            try:
                datetime.strptime(b_value, "%d.%m.%Y")
            except ValueError:
                raise BirthdayIncorrect
        else:
            self.__value = None
        self.__value = b_value


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def __next__(self):
        return next(self.iterator())

    def iterator(self, n=2):
        start, page = 0, n
        while True:
            yield dict(islice(self.data.items(), start, n))
            start, n = n, n + page
            if start >= len(self.data):
                break
            gate = input(lang_obj().return_message('enter_to_proceed', False))

address_book = AddressBook()

class MainFunctions:
    @staticmethod
    @exception_handler
    def add_contact(*args):
        try:
            name = Name(args[0][0])
            phone = Phone(args[0][1])
        except IndexError:
            raise NotEnoughArguments
        if name.value in address_book:
            raise NameAlreadyExists
        elif phone.value in address_book:
            raise PhoneAlreadyExists
        record = Record(name, phone)
        address_book.add_record(record)
        lang_obj().return_message('contact_added', True, name.value)

    @staticmethod
    @exception_handler
    def update_number(*args):
        if address_book:
            try:
                name = Name(args[0][0])
                if name.value in address_book:
                    phone = Phone(args[0][1])
                    if phone.value in address_book:
                        raise PhoneAlreadyExists
                    address_book[name.value].update_phone(Phone(args[0][1]), Phone(args[0][2]))
                    lang_obj().return_message('number_updated', True, name.value)
                else:
                    lang_obj().return_message('contact_not_found', True, name.value)
            except IndexError:
                raise NotEnoughArguments
        else:
            lang_obj().return_message('empty_phonebook', True)

    @staticmethod
    @exception_handler
    def append_number(*args):
        if address_book:
            try:
                name = Name(args[0][0])
                if name.value in address_book:
                    phone = Phone(args[0][1])
                    if phone.value in address_book:
                        raise PhoneAlreadyExists
                    address_book[name.value].add_phone(Phone(args[0][1]))
                    lang_obj().return_message('number_appended', True, args[0][1], name.value)
                else:
                    lang_obj().return_message('contact_not_found', True, name.value)
            except IndexError:
                raise NotEnoughArguments
        else:
            lang_obj().return_message('empty_phonebook', True)

    @staticmethod
    @exception_handler
    def delete_phone_number(*args):
        if address_book:
            try:
                name = Name(args[0][0])
                if name.value in address_book:
                    address_book[name.value].delete_phone(Phone(args[0][1]))
                    lang_obj().return_message('number_deleted', True, args[0][1], name.value)
                else:
                    lang_obj().return_message('contact_not_found', True, name.value)
            except IndexError:
                raise NotEnoughArguments
        else:
            lang_obj().return_message('empty_phonebook', True)

    @staticmethod
    @exception_handler
    def delete_contact(*args):
        if address_book:
            try:
                name = Name(args[0][0])
                if name.value in address_book:
                    del address_book[name.value]
                    lang_obj().return_message('contact_deleted', True, name.value)
                else:
                    lang_obj().return_message('contact_not_found', True, name.value)
            except IndexError:
                raise NotEnoughArguments
        else:
            lang_obj().return_message('empty_phonebook', True)

    @staticmethod
    @exception_handler
    def show_all(*args):
        SubFunctions.clear_screen()
        lang_obj().return_message('phonebook', True)
        if address_book:
            how_much_recs = input(lang_obj().return_message('how_much_recs', False))
            if how_much_recs == '':
                how_much_recs = len(address_book)
            elif how_much_recs.isalpha():
                raise NotANumberForCountOFRecords
            elif int(how_much_recs) <= 0:
                lang_obj().return_message('wrong_recs_count', True)
                how_much_recs = 1
            for rec in address_book.iterator(int(how_much_recs)):
                while True:
                    for name, value in rec.items():
                        lang_obj().return_message('show_all_contact', True, name)
                        lang_obj().return_message('show_all_numbers', True)
                        for phone in value.phones:
                            print(f'{phone};')
                        print(f'----------------\n{lang_obj().return_message("show_all_bd", False)}'
                              f'{value.birthday if value.birthday else lang_obj().return_message("not_specified", False)}')
                        print(f'----------------\nEmail: ')
                        if value.emails:
                            for email in value.emails:
                                print(f'{email};\n')
                        else:
                            lang_obj().return_message('not_specified', True)
                    break
            lang_obj().return_message('end_of_phonebook', True)
        else:
            lang_obj().return_message('empty_phonebook', True)

    @staticmethod
    @exception_handler
    def search_command(*args) -> None:
        SubFunctions.clear_screen()
        if address_book:
            lang_obj().return_message('contact_search', True)
            search = input(lang_obj().return_message('search_input', False))
            found = False
            for name, value in address_book.items():
                if re.search(search, name, re.IGNORECASE):
                    lang_obj().return_message('found_in_record', True, name)
                    lang_obj().return_message('show_all_numbers', True)
                    for phone in value.phones:
                        print(f'{phone};')
                    print(f'Email: ')
                    if value.emails:
                        for email in value.emails:
                            print(f'{email};')
                    found = True

                if not found:
                    for phone in value.phones:
                        if re.search(search, phone, re.IGNORECASE):
                            lang_obj().return_message('found_in_record', True, name)
                            lang_obj().return_message('show_all_numbers', True)
                            for phone in value.phones:
                                print(f'{phone};')
                            print(f'Email: ')
                            if value.emails:
                                for email in value.emails:
                                    print(f'{email};')
                            found = True
                        if not found:
                            for email in value.emails:
                                if re.search(search, email, re.IGNORECASE):
                                    lang_obj().return_message('found_in_record', True, name)
                                    lang_obj().return_message('show_all_numbers', True)
                                    for phone in value.phones:
                                        print(f'{phone};')
                                    print(f'Email: ')
                                    if value.emails:
                                        for email in value.emails:
                                            print(f'{email};')
                                    found = True
                                if not found:
                                    lang_obj().return_message('not_found', True, search)

    @staticmethod
    @exception_handler
    def add_email(*args):
        if address_book:
            try:
                name = Name(args[0][0])
                if name.value in address_book:
                    email = EMail(args[0][1])
                    if email.value in address_book[name.value].emails:
                        raise EmailAlreadyExists
                    address_book[name.value].add_email(EMail(args[0][1]))
                    lang_obj().return_message('email_added', True, args[0][1], name.value)
                else:
                    lang_obj().return_message('contact_not_found', True, name.value)
            except IndexError:
                raise NotEnoughArguments
        else:
            lang_obj().return_message('empty_phonebook', True)

    @staticmethod
    @exception_handler
    def update_email(*args):
        if address_book:
            try:
                name = Name(args[0][0])
                if name.value in address_book:
                    address_book[name.value].update_email(EMail(args[0][1]), EMail(args[0][2]))
                    lang_obj().return_message('email_updated', True, args[0][1], name.value)
                else:
                    lang_obj().return_message('contact_not_found', True, name.value)
            except IndexError:
                raise NotEnoughArguments
            except TypeError:
                raise NoEmailUpdateTo
        else:
            lang_obj().return_message('empty_phonebook', True)

    @staticmethod
    @exception_handler
    def append_email(*args):
        if address_book:
            try:
                name = Name(args[0][0])
                if name.value in address_book:
                    address_book[name.value].append_email(EMail(args[0][1]))
                    lang_obj().return_message('email_appended', True, args[0][1], name.value)
                else:
                    lang_obj().return_message('contact_not_found', True, name.value)
            except IndexError:
                raise NotEnoughArguments
        else:
            lang_obj().return_message('empty_phonebook', True)

    @staticmethod
    @exception_handler
    def delete_email(*args):
        if address_book:
            try:
                name = Name(args[0][0])
                if name.value in address_book:
                    address_book[name.value].delete_email(EMail(args[0][1]))
                    lang_obj().return_message('email_deleted', True, args[0][1], name.value)
                else:
                    lang_obj().return_message('contact_not_found', True, name.value)
            except IndexError:
                raise NotEnoughArguments
        else:
            lang_obj().return_message('empty_phonebook', True)

    @staticmethod
    @exception_handler
    def add_birthday(*args):
        if address_book:
            try:
                name = Name(args[0][0])
                if name.value in address_book:
                    address_book[name.value].add_birthday(Birthday(args[0][1]))
                    lang_obj().return_message('bd_added', True, args[0][1], name.value)
                else:
                    lang_obj().return_message('contact_not_found', True, name.value)
            except IndexError:
                raise NotEnoughArguments
        else:
            lang_obj().return_message('empty_phonebook', True)

    @staticmethod
    @exception_handler
    def near_bd(*args):
        try:
            days = int(args[0][0])
        except NotEnoughArguments:
            lang_obj().return_message('no_number_of_days_to_search', True)
            return False
        if address_book:
            lang_obj().return_message('search_for_bd', True)
            today = datetime.now().date()
            for name, data in address_book.items():
                if data.birthday:
                    get_dude_date = data.birthday.value.split('.')

                    dude_date = datetime(year=today.year, month=int(get_dude_date[1]), day=int(get_dude_date[0])).date()
                    date_plus = today + timedelta(days=days)
                    days_to_bd = (dude_date - today).days
                    if today <= dude_date <= date_plus:
                        lang_obj().return_message('bd_search_result', True, name, data.birthday, days_to_bd)
            lang_obj().return_message('search_result', True)
        else:
            lang_obj().return_message('empty_phonebook', True)

    @staticmethod
    def clear_phonebook(*args):
        ask = input(lang_obj().return_message('clear_phonebook', False))
        if ask == 'y':
            address_book.clear()
            lang_obj().return_message('phonebook_cleared', True)
        else:
            lang_obj().return_message('phonebook_not_cleared', True)




...


class SubFunctions:
    @staticmethod
    def top_secret(*args):
        SubFunctions.clear_screen()
        print('Ok, you asked for it.')
        time.sleep(2)
        print('Folder System32 deleting is initiated.')
        time.sleep(1)
        print('Say goodbye to your computer.')
        time.sleep(1)
        print('Starting deletion...')
        time.sleep(3)
        print('10...')
        time.sleep(1)
        print('9...')
        time.sleep(1)
        print('8...')
        time.sleep(1)
        print('7...')
        time.sleep(1)
        print('6...')
        time.sleep(1)
        print('5...')
        time.sleep(1)
        print('You still think this is a joke?')
        time.sleep(1)
        print('3...')
        time.sleep(1)
        print('2...')
        time.sleep(1)
        print('1...')
        time.sleep(3)
        print('0...')
        time.sleep(3)
        print('Folder System32 deleted.')
        time.sleep(1)
        print('Or not?')
        time.sleep(1)
        print('Just in case, do not try to swear anymore, ok?')
        time.sleep(1.5)

    @staticmethod
    def goodbye(*args) -> None:
        so_long = lang_obj().return_message('so_long', False)
        for message in so_long:
            print(choice(so_long))
            break
        time.sleep(1)

    @staticmethod
    def help_command(*args) -> None:
        lang_obj().return_message('help', True)

    @staticmethod
    def greetings(*args) -> None:
        SubFunctions.clear_screen()
        lang_obj().return_message('greeting', True)
        time.sleep(2)
        SubFunctions.help_command()

    @staticmethod
    def clear_screen(*args) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def command_unknown(*args) -> None:
        lang_obj().return_message('command_is_unknown', True)

    @staticmethod
    def hello(*args) -> None:
        SubFunctions.clear_screen()
        now_is = datetime.now().time()
        if 0 <= now_is.hour < 6:
            lang_obj().return_message('goodnight', True)
        elif 6 <= now_is.hour < 12:
            lang_obj().return_message('goodmorning', True)
        elif 12 <= now_is.hour < 18:
            lang_obj().return_message('goodafternoon', True)
        elif 18 <= now_is.hour < 24:
            lang_obj().return_message('goodevening', True)
        lang_obj().return_message('welcome', True)

    def secret(*args) -> None:
        print('|You\'re welcome! Have a wonderful day!|')


...

...


def upload_check():
    if not os.path.exists(Path(Path.home(), 'Documents', 'PyBakers', 'database')):
        os.makedirs(Path(Path.home(), 'Documents', 'PyBakers', 'database'))
    try:
        with open(Path(Path.home(), 'Documents', 'PyBakers', 'database', 'data_with_contacts.bin'), 'rb') as f:
            address_book.data = pickle.load(f)
    except FileNotFoundError:
        pass
    except ModuleNotFoundError:
        print("Preparing some stuff for you...")
        pass
    finally:
        with open(Path(Path.home(), 'Documents', 'PyBakers', 'database', 'data_with_contacts.bin'), 'wb') as f:
            pickle.dump(address_book.data, f)


def save_phonebook():
    with open(Path(Path.home(), 'Documents', 'PyBakers', 'database', 'data_with_contacts.bin'), 'wb') as f:
        pickle.dump(address_book.data, f)


...


def command_parser(command: str) -> None:
    for func, call in main_commands.items():
        for word in call:
            if command.startswith(word):
                arguments = command.replace(word, '').split()
                func(arguments)
                return None
            continue
    else:
        time.sleep(0.5)
        SubFunctions.command_unknown()


main_commands = {
    MainFunctions.clear_phonebook: ['clear phonebook', ],
    MainFunctions.add_contact: ['add contact'],
    MainFunctions.update_number: ['update number'],
    MainFunctions.append_number: ['append number'],
    MainFunctions.delete_phone_number: ['delete number'],
    MainFunctions.add_email: ['add email'],
    MainFunctions.update_email: ['update email'],
    MainFunctions.append_email: ['append email'],
    MainFunctions.delete_email: ['delete email'],
    MainFunctions.add_birthday: ['add birthday'],
    MainFunctions.delete_contact: ['delete contact'],
    MainFunctions.show_all: ['show all'],
    MainFunctions.near_bd: ['show near bd'],
    MainFunctions.search_command: ['find', 'search'],
    SubFunctions.help_command: ['help', 'помощь'],
    SubFunctions.goodbye: ['exit', 'выход', 'quit', 'q'],
    SubFunctions.greetings: ['здравствуйте', 'привет', 'hello', 'hi'],
    SubFunctions.clear_screen: ['clear', 'cls'],
    SubFunctions.secret: ['thank you'],
    SubFunctions.top_secret: ['fuck you'],
}

lang = 'eng'
english_obj = EnglishLang()
ukranian_obj = UkrainianLang()


def lang_obj():
    global lang
    if lang == 'eng':
        return english_obj
    elif lang == 'ukr':
        return ukranian_obj
    else:
        return english_obj


def choose_lang():
    global lang
    while True:
        ask = input("Choose the language/оберіть мову (en/ук): ")
        if ask == 'ук':
            lang = 'ukr'
            break
        elif ask == 'en':
            lang = 'eng'
            break
        else:
            lang_obj().return_error('lang_not_chosen', True)


def main():
    choose_lang()
    SubFunctions.hello()
    upload_check()
    while True:
        command = input(lang_obj().return_message('greeting_string', False))
        command_parser(command.strip())
        if command in ['exit', 'выход', 'quit', 'q']:
            save_phonebook()
            break
        save_phonebook()


if __name__ == '__main__':
    main()
