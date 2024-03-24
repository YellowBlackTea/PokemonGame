import csv

def save_data(filepath: str) -> list[dict]:
    """Save data from its file path

    Args:
        filepath (str): path of the data file

    Returns:
        list[dict]: data stored as a dict and each row represents an index in the list
    """
    saved_data = []
    with open(filepath, 'r') as file:
        data = csv.DictReader(file, delimiter="\t")
        for row in data:
            saved_data.append(row)
    return saved_data

def get_int(prompt: str) -> int:
    while True:
        number = input(prompt)
        if number.isdecimal():
            return int(number)