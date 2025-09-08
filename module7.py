from collections import UserDict, defaultdict
from datetime import datetime, date, timedelta


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
            bday = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(bday)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


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

            orig = record.birthday.value
            congratulate = orig.replace(year=today.year)

            if congratulate < today:
                congratulate = congratulate.replace(year=today.year + 1)

            # якщо вихідний — переносимо на понеділок
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
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()