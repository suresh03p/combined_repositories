 from book import *
from member import *
from issue import *
from reports import *


while True:

    print("""
    ===== Library System =====

    1. Add Book
    2. Search Book
    3. Register Member
    4. Issue Book
    5. Return Book
    6. Available Books Report
    7. Borrowed Books Report
    8. Fine Report
    9. Exit
    """)

    choice = input(
        "Enter Choice: "
    )

    try:

        if choice == "1":

            book = Book(
                int(input("Book ID: ")),
                input("Title: "),
                input("Author: "),
                int(input("Quantity: "))
            )

            BookManager.add_book(
                book
            )

        elif choice == "2":

            book_id = int(
                input("Book ID: ")
            )

            print(
                BookManager.search_book(
                    book_id
                )
            )

        elif choice == "3":

            member = Member(
                int(
                    input(
                        "Member ID:"
                    )
                ),
                input("Name: "),
                input(
                    "Membership:"
                )
            )

            MemberManager.register_member(
                member
            )

        elif choice == "4":

            IssueManager.issue_book(
                int(
                    input(
                        "Book ID:"
                    )
                ),
                int(
                    input(
                        "Member ID:"
                    )
                )
            )

        elif choice == "5":

            IssueManager.return_book(
                int(
                    input(
                        "Book ID:"
                    )
                ),
                int(
                    input(
                        "Member ID:"
                    )
                )
            )

        elif choice == "6":

            Reports.available_books()

        elif choice == "7":

            Reports.borrowed_books()

        elif choice == "8":

            Reports.fine_report()

        elif choice == "9":

            break

        else:

            print(
                "Invalid Choice"
            )

    except Exception as e:
        print("Error:", e)