def get_int(prompt: str) -> int:
    while True:
        number = input(prompt)
        if number.isdigit():
            return int(number)