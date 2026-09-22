"""Simple explanations of machine learning types."""


def show_supervised_learning():
    print("Supervised Learning")
    print("Input -> Known Answer")
    print("Examples:")
    print("- House features -> House price")
    print("- Student data -> Pass/Fail")
    print("- Customer data -> Churn/No Churn")
    print()


def show_unsupervised_learning():
    print("Unsupervised Learning")
    print("No predefined answer")
    print("Example:")
    print("Customer data -> Find groups (clusters)")
    print()


def show_regression():
    print("Regression")
    print("Predicts a continuous number.")
    examples = [
        "House price prediction",
        "Temperature forecast",
        "Stock price prediction",
        "Sales forecasting",
        "Salary prediction",
    ]
    for item in examples:
        print("-", item)
    print()


def show_classification():
    print("Classification")
    print("Predicts a class or label.")
    examples = [
        "Spam or not spam",
        "Dog or cat image",
        "Pass or fail",
        "Customer churn or not",
        "Fraud or genuine transaction",
    ]
    for item in examples:
        print("-", item)
    print()


def show_clustering():
    print("Clustering")
    print("Groups similar data together without labels.")
    examples = [
        "Customer segmentation",
        "Market grouping",
        "Image grouping",
        "Product categories",
        "Social media audience groups",
    ]
    for item in examples:
        print("-", item)
    print()


if __name__ == "__main__":
    show_supervised_learning()
    show_unsupervised_learning()
    show_regression()
    show_classification()
    show_clustering()
