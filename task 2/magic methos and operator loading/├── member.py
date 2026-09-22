from storage import Storage


class Person:

    def __init__(self, id, name):
        self.id = id
        self.name = name


class Member(Person):

    def __init__(
        self,
        member_id,
        name,
        membership_type
    ):
        super().__init__(member_id, name)

        self.membership_type = membership_type


class MemberManager:

    FILE = "data/members.json"

    @classmethod
    def register_member(cls, member):

        members = Storage.load_data(cls.FILE)

        members.append(member.__dict__)

        Storage.save_data(cls.FILE, members)

        print("Member Registered")

    @classmethod
    def delete_member(cls, member_id):

        members = Storage.load_data(cls.FILE)

        members = [
            m for m in members
            if m["id"] != member_id
        ]

        Storage.save_data(cls.FILE, members)

    @classmethod
    def validate_member(cls, member_id):

        members = Storage.load_data(cls.FILE)

        return any(
            m["id"] == member_id
            for m in members
        )

    @classmethod
    def update_member(cls, member_id, new_name):

        members = Storage.load_data(cls.FILE)

        for member in members:
            if member["id"] == member_id:
                member["name"] = new_name

        Storage.save_data(cls.FILE, members)