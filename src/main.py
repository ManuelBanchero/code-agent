from build_agent import build_agent


def main():
    agent = build_agent()

    response, success = agent.query(
        'watch how this project works and make a sum of 6 + 20')
    if success:
        print(response)
    else:
        print(response)
        exit(1)


main()
