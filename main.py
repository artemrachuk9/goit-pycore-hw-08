import pickle
from collections import UserDict


class Record:
    def __init__(self, name, phone=None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone):
        self.phones.append(phone)

    def change_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p == old_phone:
                self.phones[i] = new_phone
                return True
        return False

    def __str__(self):
        return f"{self.name}: {', '.join(self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name] = record

    def find(self, name):
        return self.data.get(name)

    def show_all(self):
        if not self.data:
            return "No contacts found."
        return "\n".join(str(record) for record in self.data.values())


# -------- Серіалізація --------
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  



def main():
    book = load_data() 

    while True:
        user_input = input("Enter command: ").strip().lower()
        parts = user_input.split()
        if not parts:
            continue

        command = parts[0]
        args = parts[1:]

        if command == "add":
            if len(args) < 2:
                print("Usage: add <name> <phone>")
                continue
            name, phone = args
            record = book.find(name)
            if record:
                record.add_phone(phone)
            else:
                record = Record(name, phone)
                book.add_record(record)
            print("Contact added.")

        elif command == "change":
            if len(args) < 3:
                print("Usage: change <name> <old_phone> <new_phone>")
                continue
            name, old_phone, new_phone = args
            record = book.find(name)
            if record and record.change_phone(old_phone, new_phone):
                print("Phone changed.")
            else:
                print("Contact or phone not found.")

        elif command == "phone":
            if len(args) < 1:
                print("Usage: phone <name>")
                continue
            name = args[0]
            record = book.find(name)
            if record:
                print(record)
            else:
                print("Contact not found.")

        elif command == "all":
            print(book.show_all())

        elif command in ("exit", "close"):
            save_data(book)  
            print("Address book saved. Goodbye!")
            break

        elif command == "hello":
            print("How can I help you?")

        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
