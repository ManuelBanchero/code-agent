from functions.get_files_info import get_files_info


def test():
    base_path = '/Users/manuelbanchero/dev/courses/boot_dev/code-agent'

    result = get_files_info(f"{base_path}/calculator", ".")
    print("Result for current directory:")
    print(result)
    print("")

    result = get_files_info(f"{base_path}/calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(result)
    print("")

    result = get_files_info(f"{base_path}/calculator", "/bin")
    print("Result for '/bin' directory:")
    print(result)
    print("")

    result = get_files_info(f"{base_path}/calculator", "../")
    print("Result for '../' directory:")
    print(result)
    print("")


if __name__ == "__main__":
    test()
