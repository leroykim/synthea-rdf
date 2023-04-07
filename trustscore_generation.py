from trustscore.generator import TrustScoreGenerator
from argparse import ArgumentParser
from pathlib import Path


def main():
    args = parse_argument()
    num_org = args.num_org
    user_per_org = args.user_per_org
    save_path = args.save_path
    trust_score_generator = TrustScoreGenerator(num_org, user_per_org)
    trust_score_generator.generate_trustscore(save_path=save_path)


def parse_argument():
    # python3 dev_generation.py -o 10 -u 10 -s csv/500
    parser = ArgumentParser()
    parser.add_argument(
        "-o",
        "--num-org",
        dest="num_org",
        type=int,
        required=True,
        help="Provide the number of organizations.",
    )
    parser.add_argument(
        "-u",
        "--user-per-org",
        dest="user_per_org",
        type=int,
        required=True,
        help="Provide the number of users per organization.",
    )
    parser.add_argument(
        "-s",
        "--save-path",
        dest="save_path",
        type=str,
        required=True,
        help="Provide the path to save the generated trust score.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
