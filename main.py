from abc import ABC, abstractmethod

class AbstractView(ABC): #I`m not sure is it correctly, but that how I  understood the task.
    @abstractmethod
    def show_message(self, message: str):
        pass

    @abstractmethod
    def show_contacts(self, contacts: str):
        pass

    @abstractmethod
    def get_user_input(self, prompt: str) -> str:
        pass

class ConsoleView(AbstractView):
    def show_message(self, message: str):
        print(message)

    def show_contacts(self, contacts: str):
        print("Contacts:")
        print(contacts)

    def get_user_input(self, prompt: str) -> str:
        return input(prompt)