import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("data/bookmarks.json")


def load_bookmarks() -> list:
    if not DATA_FILE.exists():
        return []
    raw = DATA_FILE.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("Warning: bookmarks file is invalid JSON; starting fresh.", file=sys.stderr)
        return []
    if not isinstance(data, list):
        print("Warning: bookmarks JSON must be a list; starting fresh.", file=sys.stderr)
        return []
    return data


def save_bookmarks(bookmarks: list) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(bookmarks, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def show_bookmarks():
    bookmarks = load_bookmarks()

    if not bookmarks:
        print("No bookmarks")
    else:
        for i, bookmark in enumerate(bookmarks, start=1):
            title = bookmark.get("title", "")
            url = bookmark.get("url", "")
            date = bookmark.get("date", "")
            print(f"{i}. {title} ({url}): {date}")


def main() -> None:
    while True:
        bookmarks = load_bookmarks()
        user_input = (
            input("What do you want to do? (add, list, delete, clear, edit) ").strip().lower()
        )
        if user_input == "list":
            show_bookmarks()
        elif user_input == "add":
            url = input("Enter the URL: ").strip()
            title = input("Enter the title: ").strip()
            datetime_now = datetime.now(timezone.utc).strftime("%d-%m-%Y %H:%M")
            bookmarks.append({"url": url, "title": title, "date": datetime_now})
            save_bookmarks(bookmarks)
            print("Bookmark", title, "added!")
        elif user_input == "delete":
            show_bookmarks()
            index = int(
                input("Enter the index number of the bookmark you want to delete: ").strip()
            )
            if index > len(bookmarks) or index < 1:
                print("Invalid index")
            else:
                removed = bookmarks.pop(index - 1)
                save_bookmarks(bookmarks)
                print("Bookmark", removed["title"], "deleted!")
        elif user_input == "clear":
            confirm = input("Are you sure you want to clear all bookmarks? (y/n) ").strip().lower()
            if confirm == "y":
                save_bookmarks([])
                print("All bookmarks cleared!")
            else:
                print("Clear cancelled.")
        elif user_input == "edit":
            show_bookmarks()
            index = int(input("Enter the index number of the bookmark you want to edit: ").strip())
            if index > len(bookmarks) or index < 1:
                print("Invalid index")
            else:
                bookmark = bookmarks[index - 1]
                new_url = input(
                    f"Enter the new URL (leave blank to keep '{bookmark['url']}'): "
                ).strip()
                new_title = input(
                    f"Enter the new title (leave blank to keep '{bookmark['title']}'): "
                ).strip()
                if new_url:
                    bookmark["url"] = new_url
                if new_title:
                    bookmark["title"] = new_title
                save_bookmarks(bookmarks)
                print("Bookmark", bookmark["title"], "updated!")
        else:
            print("This command does not exist yet")

        again = input("Is there something else you would like to do? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for using the bookmark manager!")
            break


if __name__ == "__main__":
    main()
