import datetime
from abc import ABC, abstractmethod

class AbstractRecord(ABC):
    @abstractmethod
    def add_phone(self, phone_number):
        pass

    @abstractmethod
    def remove_phone(self, phone_number):
        pass

    @abstractmethod
    def edit_phone(self, old_number, new_number):
        pass

    @abstractmethod
    def find_phone(self, phone_number):
        pass

    @abstractmethod
    def add_birthday(self, birthday):
        pass

class Record(AbstractRecord):
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self,phone_number):
        new_phone = Phone(phone_number)
        self.phones.append(new_phone)


    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break

    def edit_phone(self, old_number, new_number):
        Phone(new_number)
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                break
        else:
            raise ValueError(f"Can`t find {old_number}.")

    def find_phone(self, phone_number):
        try:
            for phone in self.phones:
                if phone.value == phone_number:
                    return phone
            return None
        except ValueError:
            return None

    def add_birthday(self, birthday):
        new_birthday = Birthday(birthday)
        self.birthday = new_birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        super().__init__(name)

class Phone(Field):
    def __init__(self, phone):
        if len(phone) == 10 and phone.isdigit():
            super().__init__(phone)
        else:
            raise ValueError("Phone number must contain exactly 10 digits.")

class Birthday(Field):
    def __init__(self, value):
        datetime.strptime(value, '%d.%m.%Y').date()
        super().__init__(value)
