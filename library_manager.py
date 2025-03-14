import json
import datetime
from InquirerPy import inquirer
from rich.console import Console
from rich.table import Table

console = Console()
date = datetime.datetime
FILENAME = 'library.json'

print("📚 Welcome to the Personal Library Manager by Rafay Nadeem! 📚")

# Load books from file
try:
    with open(FILENAME, 'r') as f:
        library = json.load(f)
    print("✅ Library loaded successfully.")
except (FileNotFoundError, json.JSONDecodeError):
    library = []
    print("📂 Starting with an empty library.")


def save_library():
    with open(FILENAME, 'w') as f:
        json.dump(library, f, indent=4)
    print("💾 Library saved successfully!")


def add_book():
    title = input("Enter the title of the book: ").strip()
    while not title:
        print("Title cannot be empty!")
        title = input("Enter the title of the book: ").strip()

    author = input("Enter the author of the book: ").strip()
    while not author:
        print("Author cannot be empty!")
        author = input("Enter the author of the book: ").strip()

    while True:
        try:
            year = int(input("Enter the year the book was published: ").strip())
            if 0 < year <= date.now().year:
                break
            print("Please enter a valid year!")
        except ValueError:
            print("Invalid input. Enter a numerical year!")

    genre = input("Enter the genre of the book: ").strip()
    while not genre:
        print("Genre cannot be empty!")
        genre = input("Enter the genre of the book: ").strip()

    read_status = inquirer.confirm("Have you read this book?").execute()

    book = {"title": title, "author": author, "year": year,
            "genre": genre, "isRead": read_status}
    library.append(book)
    print("📖 Book added successfully!")
    save_library()


def remove_book():
    title = input("Enter the title of the book to remove: ").strip().lower()
    original_count = len(library)
    library[:] = [book for book in library if book['title'].lower() != title]

    if len(library) < original_count:
        print("🗑️ Book removed successfully!")
        save_library()
    else:
        print("❌ No book found with that title.")


def list_books():
    if not library:
        console.print("[yellow]No books found![/yellow]")
        return

    table = Table(title="[cyan]Library Books[/cyan]", show_lines=True)
    table.add_column("Title", style="bold magenta")
    table.add_column("Author", style="bold cyan")
    table.add_column("Year", style="bold yellow")
    table.add_column("Genre", style="bold green")
    table.add_column("Read", style="bold red")

    for book in library:
        table.add_row(book['title'], book['author'], str(
            book['year']), book['genre'], "Yes" if book['isRead'] else "No")

    console.print(table)


def search_book():
    criteria = inquirer.select(
        message="Search by:",
        choices=["Title", "Author", "Year", "Genre"]
    ).execute()

    query = input(f"Enter the {criteria.lower()} to search: ").strip().lower()

    if criteria == "Year":
        try:
            query = int(query)
        except ValueError:
            print("Invalid year format.")
            return

    results = [book for book in library if str(
        book[criteria.lower()]).lower() == str(query)]

    if results:
        for book in results:
            print(
                f"Title: {book['title']}, Author: {book['author']}, Year: {book['year']}, Genre: {book['genre']}, Read: {'Yes' if book['isRead'] else 'No'}")
    else:
        print("🔍 No matching books found.")


def display_statistics():
    if not library:
        print("No books found!")
        return

    total_books = len(library)
    read_books = sum(book['isRead'] for book in library)
    unread_books = total_books - read_books

    author_count = {}
    genre_count = {}
    total_years = 0

    for book in library:
        author_count[book['author']] = author_count.get(book['author'], 0) + 1
        genre_count[book['genre']] = genre_count.get(book['genre'], 0) + 1
        total_years += book['year']

    most_popular_author = max(
        author_count, key=author_count.get, default="N/A")
    most_popular_genre = max(genre_count, key=genre_count.get, default="N/A")
    average_year = total_years / total_books if total_books else 0

    print(f"Total number of books: {total_books}")
    print(f"Total number of unread books: {unread_books}")
    print(f"Total number of read books: {read_books}")
    print(f"Most popular author: {most_popular_author}")
    print(f"Most popular genre: {most_popular_genre}")
    print(f"Average year of publication: {average_year:.2f}")
    print(f"Percentage of read books: {read_books / total_books * 100:.2f}%")


# Extra Functions


def edit_book():
    title = input("Enter the title of the book to edit: ").strip().lower()
    for book in library:
        if book['title'].lower() == title:
            print("Editing book:", book['title'])
            book['title'] = input(
                f"Enter new title (current: {book['title']}): ").strip() or book['title']
            book['author'] = input(
                f"Enter new author (current: {book['author']}): ").strip() or book['author']
            book['year'] = int(
                input(f"Enter new year (current: {book['year']}): ").strip() or book['year'])
            book['genre'] = input(
                f"Enter new genre (current: {book['genre']}): ").strip() or book['genre']
            book['isRead'] = inquirer.confirm(
                f"Have you read this book? (current: {'Yes' if book['isRead'] else 'No'})").execute()
            print("📝 Book updated successfully!")
            save_library()
            return
    print("❌ No book found with that title.")


def export_library():
    export_filename = input("Enter the filename to export to: ").strip()
    with open(export_filename, 'w') as f:
        json.dump(library, f, indent=4)
    print(f"📤 Library exported successfully to {export_filename}!")


def import_library():
    import_filename = input("Enter the filename to import from: ").strip()
    try:
        with open(import_filename, 'r') as f:
            global library
            library = json.load(f)
        print(f"📥 Library imported successfully from {import_filename}!")
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ Failed to import library. File not found or invalid format.")


def main():
    while True:
        action = inquirer.select(
            message="Which action would you like to perform?",
            choices=[
                "Add a book",
                "Remove a book",
                "Edit a book",
                "List all books",
                "Search for a book",
                "Display statistics",
                "Export library",
                "Import library",
                "Exit the program"
            ]
        ).execute()

        if action == "Add a book":
            add_book()
        elif action == "Remove a book":
            remove_book()
        elif action == "Edit a book":
            edit_book()
        elif action == "List all books":
            list_books()
        elif action == "Search for a book":
            search_book()
        elif action == "Display statistics":
            display_statistics()
        elif action == "Export library":
            export_library()
        elif action == "Import library":
            import_library()
        elif action == "Exit the program":
            save_library()
            print("👋 Goodbye!")
            break
        else:
            print("Invalid action!")


if __name__ == "__main__":
    main()
