from build_agent import build_agent
import argparse


def main():
    # Get user input
    parser = argparse.ArgumentParser(description='Code Agent')
    parser.add_argument('user_prompt', type=str, help='User prompt')
    args = parser.parse_args()
    user_prompt = args.user_prompt

    # Create Agent
    agent = build_agent()

    # Make a query w/user prompt
    response, success = agent.query(user_prompt=user_prompt)

    if success:
        print(response)
    else:
        print(response)
        exit(1)


main()
