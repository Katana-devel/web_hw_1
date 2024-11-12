import datetime
from Modul_1.Py_bot.AddressBook import AddressBook, load_data, save_data
from Modul_1.Py_bot.Record import Record
from Modul_1.Py_bot.main import ConsoleView

view = ConsoleView()

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            view.show_message("Give me name and phone please.")
        except KeyError:
            view.show_message("Wrong key")
        except IndexError:
            view.show_message("Wrong index")
        except Exception as e:
            view.show_message(f"An unexpected error occurred: {e}")

    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

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
    view.show_message(message)

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is not None:
        record.edit_phone(old_phone, new_phone)
        view.show_message("Contact changed.")
    else:
        view.show_message("Contact not found")

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        view.show_message('; '.join(phone.value for phone in record.phones))
    else:
        view.show_message('Contact not found')

@input_error
def show_all(book: AddressBook):
    result = []
    for name, record in book.data.items():
        phone_numbers = '; '.join(phone.value for phone in record.phones)
        birthday_str = f", Birthday: {record.birthday.value}" if record.birthday else ""
        result.append(f"{name}: {phone_numbers}{birthday_str}")
    view.show_contacts('\n'.join(result))

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    message = "Birthday updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact and Birthday added."

    try:
        birthday_date = datetime.strptime(birthday, '%d.%m.%Y').date()
    except ValueError:
        view.show_message("Error: Invalid date format. Please use DD.MM.YYYY")
        return

    record.birthday = birthday_date
    view.show_message(message)

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday is not None:
            view.show_message(record.birthday.value)
        else:
            view.show_message("Birthday not found")
    else:
        view.show_message("Contact not found")

@input_error
def birthdays(book: AddressBook):
    days = 7
    upcoming_birthdays = book.get_upcoming_birthdays(days)

    if not upcoming_birthdays:
        view.show_message("Немає днів народження на найближчі 7 днів.")
        return

    result = "Дні народження на найближчі 7 днів:\n"
    for birthday_info in upcoming_birthdays:
        name = birthday_info["name"]
        congratulation_date = birthday_info["congratulation_date"]
        result += f"{name}: {congratulation_date}\n"
    view.show_message(result)

def main():
    book = load_data()
    view.show_message("Welcome to the assistant bot!")
    while True:
        user_input = view.get_user_input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            view.show_message("Good bye!")
            save_data(book)
            break

        elif command == "hello":
            view.show_message("How can I help you?")

        elif command == "add":
            add_contact(args, book)
            save_data(book)

        elif command == "change":
            change_contact(args, book)
            save_data(book)

        elif command == "phone":
            show_phone(args, book)

        elif command == "all":
            show_all(book)

        elif command == "add-birthday":
            add_birthday(args, book)
            save_data(book)

        elif command == "show-birthday":
            show_birthday(args, book)

        elif command == "birthdays":
            birthdays(book)

        else:
            view.show_message("Invalid command.")

if __name__ == "__main__":
    main()