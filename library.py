import json
import re

from typing import List, Dict, Union

Book = Dict[str, Union[int, str]]


class Library:
    def __init__(self, storage_file: str = "library.json"):
        self.storage_file = storage_file
        self.books: List[Book] = []
        self.next_id = 1  # Счетчик для ID
        self.load_books()

    def load_books(self) -> None:
        """Загрузка данных из файла."""
        try:
            with open(self.storage_file, "r") as file:
                data = json.load(file)
                self.books = data.get("books", [])
                self.next_id = data.get("next_id", 1)
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Ошибка чтения данных. Файл поврежден.")
            self.books = []

    def save_books(self) -> None:
        """Сохранение данных в файл."""
        data = {
            "books": self.books,
            "next_id": self.next_id
        }
        with open(self.storage_file, "w") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str) -> None:
        """Добавление книги в библиотеку с проверкой года."""
        while True:
            year = input("Введите год издания книги (только целое число): ")
            if year.isdigit():
                year = int(year)
                if 0 < year <= 9999:  # Проверка на допустимый диапазон лет
                    break
                else:
                    print("Год должен быть в диапазоне от 1 до 9999.")
            else:
                print("Год должен быть целым числом. Попробуйте снова.")

        new_book = {
            "id": self.next_id,
            "title": title,
            "author": author,
            "year": year,
            "status": "в наличии"
        }
        self.books.append(new_book)
        self.next_id += 1  # Увеличиваем счетчик ID
        self.save_books()
        print(f"Книга '{title}' добавлена в библиотеку.")

    def delete_book(self, book_id: int) -> None:
        """Удаление книги по ID."""
        for book in self.books:
            if book["id"] == book_id:
                self.books.remove(book)
                self.save_books()
                print(f"Книга с ID {book_id} удалена.")
                return
        print(f"Книга с ID {book_id} не найдена.")

    def search_books(self, key: str, value: str) -> List[Book]:
        """Поиск книг по ключу без учета регистра, пробелов и символов."""
        if key not in ["title", "author", "year"]:
            print("Недопустимый критерий поиска. Используйте title, author или year.")
            return []

        # Функция для нормализации строк (удаление пробелов, символов и приведение к нижнему регистру)
        def normalize_string(s: str) -> str:
            return re.sub(r'\W+', '', s.strip().lower())  # Удаление всех символов, кроме букв и цифр

        # Приведение значения для поиска к нормализованной форме
        normalized_value = normalize_string(value)

        # Поиск книг с нормализованными значениями
        results = [book for book in self.books if normalized_value in normalize_string(str(book[key]))]
        return results

    def display_books(self) -> None:
        """Отображение всех книг."""
        if not self.books:
            print("Библиотека пуста.")
            return
        for book in self.books:
            print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, "
                  f"Год: {book['year']}, Статус: {book['status']}")

    def update_status(self, book_id: int, new_status: str) -> None:
        """Обновление статуса книги."""
        if new_status not in ["в наличии", "выдана"]:
            print("Недопустимый статус. Используйте 'в наличии' или 'выдана'.")
            return
        for book in self.books:
            if book["id"] == book_id:
                book["status"] = new_status
                self.save_books()
                print(f"Статус книги с ID {book_id} обновлен на '{new_status}'.")
                return
        print(f"Книга с ID {book_id} не найдена.")

def main() -> None:
    library = Library()

    while True:
        print("\nДоступные команды:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ").strip()
            author = input("Введите автора книги: ")
            library.add_book(title, author)
        elif choice == "2":
            try:
                book_id = int(input("Введите ID книги для удаления: "))
                library.delete_book(book_id)
            except ValueError:
                print("ID должен быть числом.")
        elif choice == "3":
            key = input("Введите критерий поиска (title, author, year): ").strip()
            if key not in ["title", "author", "year"]:
                print("Недопустимый критерий поиска. Попробуйте снова.")
                continue
            value = input("Введите значение для поиска: ").strip()
            results = library.search_books(key, value)
            if results:
                for book in results:
                    print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, "
                          f"Год: {book['year']}, Статус: {book['status']}")
            else:
                print("Книги по заданному критерию не найдены.")
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            try:
                book_id = int(input("Введите ID книги: "))
                new_status = input("Введите новый статус (в наличии, выдана): ").strip()
                if new_status not in ["в наличии", "выдана"]:
                    print("Недопустимый статус. Попробуйте снова.")
                    continue
                library.update_status(book_id, new_status)
            except ValueError:
                print("ID должен быть числом.")
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Недопустимый выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
