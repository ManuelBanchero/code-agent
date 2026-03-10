import argparse
from call_model import call_model


def main():
    parser = argparse.ArgumentParser(description='Code Agent')
    parser.add_argument('user_prompt', type=str, help='User prompt')
    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose output')
    args = parser.parse_args()

    call_model(args.user_prompt, args.verbose)


if __name__ == "__main__":
    main()
