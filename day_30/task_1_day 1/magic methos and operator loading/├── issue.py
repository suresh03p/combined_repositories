from datetime import datetime
from storage import Storage
from member import MemberManager
from book import BookManager
from exceptions import *


class Issue:

    def __init__(
        self,
        book_id,
        member_id
    ):
        self.book_id = book_id
        self.member_id = member_id
        self.issue_date = datetime.now().strftime(
            "%Y-%m-%d"
        )


class IssueManager:

    FILE = "data/issues.json"

    @classmethod
    def issue_book(
        cls,
        book_id,
        member_id
    ):

        if not MemberManager.validate_member(
                member_id):
            raise MemberNotFoundError()

        if not BookManager.is_available(
                book_id):
            raise BookUnavailableError()

        issue = Issue(
            book_id,
            member_id
        )

        issues = Storage.load_data(cls.FILE)

        issues.append(issue.__dict__)

        Storage.save_data(
            cls.FILE,
            issues
        )

        print("Book Issued")

    @classmethod
    def return_book(
        cls,
        book_id,
        member_id
    ):

        issues = Storage.load_data(
            cls.FILE
        )

        issues = [
            i for i in issues
            if not (
                i["book_id"] == book_id and
                i["member_id"] == member_id
            )
        ]

        Storage.save_data(
            cls.FILE,
            issues
        )

        print("Book Returned")

    @staticmethod
    def late_days(issue_date):

        today = datetime.now()

        issued = datetime.strptime(
            issue_date,
            "%Y-%m-%d"
        )

        days = (
            today - issued
        ).days

        return max(0, days - 14)

    @staticmethod
    def calculate_fine(
        issue_date,
        fine_per_day=5
    ):

        return (
            IssueManager.late_days(
                issue_date
            ) * fine_per_day
        )