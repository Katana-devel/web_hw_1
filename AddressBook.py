from collections import UserDict
from datetime import datetime, date, timedelta
import pickle
from abc import ABC, abstractmethod
from typing import List, Dict, Any

from Record import Record

class AbstractAddressBook(ABC):

    @abstractmethod
    def add_record(self, record: Record) -> None:
        pass

    @abstractmethod
    def find(self, name) -> Record:
        pass

    @abstractmethod
    def delete(self, name) -> None:
        pass

    @abstractmethod
    def get_upcoming_birthdays(self, days=7) -> List[Dict[str, Any]]:
        pass

class AddressBook(UserDict, AbstractAddressBook):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)

    def get_upcoming_birthdays(self, days=7)-> List[Dict[str, Any]]:
        upcoming_birthdays = []
        today = date.today()
        for user in self.data.values():
            if user.birthday is None:
                continue

            birthday_this_year = user.birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if 0 <= (birthday_this_year - today).days <= days:
                congratulation_date = adjust_for_weekend(birthday_this_year)
                upcoming_birthdays.append(
                    {"name": user.name.value, "congratulation_date": date_to_string(congratulation_date)}
                )

        return upcoming_birthdays

    def __str__(self):
        contacts = "\n".join(str(record) for record in self.data.values())
        return f"Information about contacts:\n{contacts}"




def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def string_to_date(date_string):
    return datetime.strptime(date_string, "%Y.%m.%d").date()

def date_to_string(date):
    return date.strftime("%Y.%m.%d")

def prepare_user_list(user_data):
    prepared_list = []
    for user in user_data:
        prepared_list.append({"name": user["name"], "birthday": string_to_date(user["birthday"])})
    return prepared_list

def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)

def adjust_for_weekend(birthday):
    if birthday.weekday() >= 5:
        return find_next_weekday(birthday, 0)
    return birthday
