from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # Обов'язкове поле, успадковує Field
    pass


class Phone(Field):
    def __init__(self, value: str):
        if not self.validate(value):
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)

    @staticmethod
    def validate(value: str) -> bool:
        return value.isdigit() and len(value) == 10


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str):
        phone_obj = self.find_phone(old_phone)
        if phone_obj:
            if not Phone.validate(new_phone):
                raise ValueError("New phone number must contain exactly 10 digits")
            phone_obj.value = new_phone
        else:
            raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "no phones"
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
