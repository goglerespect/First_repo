def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the argument for the command"
    return inner


def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:              # перевірка на пустий рядок
        return "", []          
    cmd, *args = parts
    return cmd.lower(), args



@input_error
def add_contact(args, contacts):
    name, phone = args  # якщо немає 2 аргументи → ValueError
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    name, phone = args  # якщо не 2 аргументи → ValueError
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        raise KeyError  # кидаємо помилку, якщо нема контакту


@input_error
def show_phone(args, contacts):
    name = args[0]  # якщо немає аргументів → IndexError
    return contacts[name]  # якщо нема в словнику → KeyError


@input_error
def show_all(contacts):
    if not contacts:
        return "No contacts saved."
    result = []
    for name, phone in contacts.items():
        result.append(f"{name}: {phone}")
    return "\n".join(result)


def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        if not command:       # пропускаємо пустий рядок
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()