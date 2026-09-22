class Validator:

    @staticmethod
    def validate_name(name):

        if len(name) < 3:
            raise ValueError(
                "Name too short"
            )

    @staticmethod
    def validate_quantity(quantity):

        if quantity < 0:
            raise ValueError(
                "Invalid Quantity"
            )