import os


if __name__ == '__main__':
    with open(
    os.path.join(os.path.dirname(__file__), 'inputs', 'test_input.txt'), 'r', encoding='UTF-8'
    ) as file:
        data = file.read()