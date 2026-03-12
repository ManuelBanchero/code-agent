from functions.write_file import write_file


def test():
    base_path = '/Users/manuelbanchero/dev/courses/boot_dev/code-agent'

    result = write_file(f'{base_path}/calculator',
                        'lorem.txt', "wait, this isn't lorem ipsum")
    print("Result for 'lorem.txt' file")
    print(result)
    print('')

    result = write_file(f'{base_path}/calculator',
                        'pkg/morelorem.txt', "lorem ipsum dolor sit amet")
    print("Result for 'pkg/morelorem.txt' file")
    print(result)
    print('')

    result = write_file(f'{base_path}/calculator',
                        '/tmp/temp.txt', "this should not be allowed")
    print("Result for '/tmp/temp.txt' file")
    print(result)
    print('')


if __name__ == "__main__":
    test()
