from functions.get_file_content import get_file_content
from config import MAX_CHARS


def test():
    base_path = '/Users/manuelbanchero/dev/courses/boot_dev/code-agent'

    result = get_file_content(f'{base_path}/calculator', 'main.py')
    print("Result for 'main.py' file")
    print(result if len(result) <= MAX_CHARS else result.split('\n')[-1])
    print('')

    result = get_file_content(f'{base_path}/calculator', 'pkg/calculator.py')
    print("Result for 'calculator.py' file")
    print(result if len(result) <= MAX_CHARS else result.split('\n')[-1])
    print('')

    result = get_file_content(f'{base_path}/calculator', '/bin/cat')
    print("Result for '/bin/cat' file")
    print(result if len(result) <= MAX_CHARS else result.split('\n')[-1])
    print('')

    result = get_file_content(
        f'{base_path}/calculator', 'pkg/does_not_exist.py')
    print("Result for 'does_not_exist.py' file")
    print(result if len(result) <= MAX_CHARS else result.split('\n')[-1])


if __name__ == "__main__":
    test()
