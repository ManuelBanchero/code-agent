from functions.run_python_file import run_python_file


def test():
    base_path = '/Users/manuelbanchero/dev/courses/boot_dev/code-agent'

    result = run_python_file(f'{base_path}/calculator', 'main.py')
    print("Result for 'main.py' file")
    print(result)
    print('')

    result = run_python_file(f'{base_path}/calculator', 'main.py', ['3 + 5'])
    print("Result for 'main.py' file")
    print(result)
    print('')

    result = run_python_file(f'{base_path}/calculator', '../main.py')
    print("Result for '../main.py' file")
    print(result)
    print('')

    result = run_python_file(f'{base_path}/calculator', 'nonexistent.py')
    print("Result for 'nonexistent.py' file")
    print(result)
    print('')

    result = run_python_file(f'{base_path}/calculator', 'lorem.txt')
    print("Result for 'lorem.txt' file")
    print(result)


if __name__ == "__main__":
    test()
