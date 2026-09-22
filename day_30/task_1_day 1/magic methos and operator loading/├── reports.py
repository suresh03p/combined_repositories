from collections import Counter
from storage import Storage
from issue import IssueManager


class Reports:

    @staticmethod
    def available_books():

        books = Storage.load_data(
            "data/books.json"
        )

        print("\nAvailable Books")

        for book in books:

            if book["quantity"] > 0:
                print(book)

    @staticmethod
    def borrowed_books():

        issues = Storage.load_data(
            "data/issues.json"
        )

        print("\nBorrowed Books")

        for issue in issues:
            print(issue)

    @staticmethod
    def top_borrowers():

        issues = Storage.load_data(
            "data/issues.json"
        )

        counter = Counter(
            issue["member_id"]
            for issue in issues
        )

        print(
            counter.most_common(5)
        )

    @staticmethod
    def fine_report():

        issues = Storage.load_data(
            "data/issues.json"
        )

        print("\nFine Report")

        for issue in issues:

            fine = (
                IssueManager.calculate_fine(
                    issue["issue_date"]
                )
            )

            print(
                f"Member: "
                f"{issue['member_id']}"
                f" Fine:{fine}"
            )