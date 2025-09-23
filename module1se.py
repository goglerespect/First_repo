import pickle
from collections import UserDict, defaultdict
from datetime import datetime, date, timedelta
from abc import ABC, abstractmethod


# ================== ФУНКЦІЇ ЗБЕРЕЖЕННЯ ==================

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # нова адресна книга, якщо файлу немає


# ================== БАЗОВІ КЛАСИ ==================

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str):
        if not self.validate(value):
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)

    @staticmethod
    def validate(value: str) -> bool:
        return value.isdigit() and len(value) == 10


class Birthday(Field):
    def __init__(self, value: str):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

    def __str__(self):
        return self.value


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str):
        phone_obj = self.find_phone(old_phone)
        if phone_obj:
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
        else:
            raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "no phones"
        bday_str = str(self.birthday) if self.birthday else "no birthday"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {bday_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days: int = 7):
        today = date.today()
        result = []

        for record in self.data.values():
            if not record.birthday:
                continue

            orig = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            congratulate = orig.replace(year=today.year)

            if congratulate < today:
                congratulate = congratulate.replace(year=today.year + 1)

            if congratulate.weekday() >= 5:
                congratulate += timedelta(days=(7 - congratulate.weekday()))

            diff = (congratulate - today).days
            if 0 <= diff <= days:
                result.append({
                    "name": record.name.value,
                    "birthday": congratulate.strftime("%d.%m.%Y")
                })

        return result

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())


# ================== VIEW (УЯВЛЕННЯ) ==================

class View(ABC):
    @abstractmethod
    def show_message(self, text: str):
        pass

    @abstractmethod
    def show_contacts(self, book: AddressBook):
        pass

    @abstractmethod
    def show_help(self):
        pass


class ConsoleView(View):
    def show_message(self, text: str):
        print(text)

    def show_contacts(self, book: AddressBook):
        if not book.data:
            print("No contacts saved.")
        else:
            for record in book.values():
                print(record)

    def show_help(self):
        print("""
Available commands:
  add <name> <phone>
  change <name> <old_phone> <new_phone>
  phone <name>
  all
  add-birthday <name> <DD.MM.YYYY>
  show-birthday <name>
  birthdays
  hello
  help
  exit / close
""")


# ================== ДЕКОРАТОР ==================

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Enter the argument for the command."
        except AttributeError:
            return "Contact not found."
        except KeyError:
            return "Contact not found."
    return inner


# ================== ОБРОБНИКИ КОМАНД ==================

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Phone updated."


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    return "; ".join(p.value for p in record.phones) or "No phones"


@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts saved."
    return "\n".join(str(rec) for rec in book.values())


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    return str(record.birthday) if record.birthday else "No birthday set."


@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    grouped = defaultdict(list)
    for item in upcoming:
        grouped[item["birthday"]].append(item["name"])
    lines = []
    for day in sorted(grouped, key=lambda d: datetime.strptime(d, "%d.%m.%Y").date()):
        lines.append(f"{day}: {', '.join(grouped[day])}")
    return "\n".join(lines)


# ================== КОНСОЛЬНИЙ БОТ ==================

def parse_input(user_input: str):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd, *args = parts
    return cmd.lower(), args


def main():
    book = load_data()  # завантажуємо з файлу або створюємо новий
    view = ConsoleView()

    view.show_message("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)  # зберігаємо перед виходом
            view.show_message("Good bye!")
            break

        elif command == "hello":
            view.show_message("How can I help you?")

        elif command == "add":
            view.show_message(add_contact(args, book))

        elif command == "change":
            view.show_message(change_contact(args, book))

        elif command == "phone":
            view.show_message(show_phone(args, book))

        elif command == "all":
            view.show_contacts(book)

        elif command == "add-birthday":
            view.show_message(add_birthday(args, book))

        elif command == "show-birthday":
            view.show_message(show_birthday(args, book))

        elif command == "birthdays":
            view.show_message(birthdays(args, book))

        elif command == "help":
            view.show_help()

        else:
            view.show_message("Invalid command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()
