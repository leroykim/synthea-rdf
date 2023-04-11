from dua.generator import DUAGenerator
from trustscore.generator import TrustScoreGenerator
from argparse import ArgumentParser
from pathlib import Path


def main():
    args = parse_argument()
    generate_dua = args.generate_dua
    generate_trustscore = args.generate_trustscore
    if not generate_dua and not generate_trustscore:
        print("Please provide at least one generation type.")
        return
    num_org = args.num_org
    user_per_org = args.user_per_org
    trustscore_save_path = args.trustscore_save_path
    dua_save_path = args.dua_save_path
    num_requested_data = args.num_requested_data

    if generate_trustscore:
        if not num_org or not user_per_org or not trustscore_save_path:
            print(
                "Please provide all required parameters: --num-org, --user-per-org, --trustscore-save-path"
            )
            return
    if generate_dua:
        if not num_org or not dua_save_path or not num_requested_data:
            print(
                "Please provide all required parameters: --num-org, --num-requested-data, --dua-save-path"
            )
            return

    trust_score_generator = TrustScoreGenerator(
        num_org=num_org, user_per_org=user_per_org
    )
    trust_score_generator.generate_trustscore(save_path=trustscore_save_path)
    dua_generator = DUAGenerator()
    dua_generator.generate_dua(
        num_organization=num_org,
        save_path=dua_save_path,
        num_requested_data=num_requested_data,
    )


def parse_argument():
    # python3 dua_and_trustscore_generation.py -trustscore -o 10 -u 10 -tsp csv/500 -dua -nrd 10 -dsp csv/500
    parser = ArgumentParser()
    parser.add_argument(
        "-trustscore",
        "--generate-trustscore",
        dest="generate_trustscore",
        action="store_true",
        default=False,
        required=False,
        help="Generate Trust Score.",
    )
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
        "-tsp",
        "--trustscore-save-path",
        dest="trustscore_save_path",
        type=str,
        required=False,
        help="Provide the path to save the generated trust score.",
    )
    parser.add_argument(
        "-dua",
        "--generate-dua",
        dest="generate_dua",
        action="store_true",
        default=False,
        required=False,
        help="Generate Data Usage Agreement.",
    )
    parser.add_argument(
        "-nrd",
        "--num-requested-data",
        dest="num_requested_data",
        type=int,
        required=False,
        help="Provide the number of requested data.",
    )
    parser.add_argument(
        "-dsp",
        "--dua-save-path",
        dest="dua_save_path",
        type=str,
        required=False,
        help="Provide the path to save the generated data usage agreement.",
    )
    parser.add_argument(
        "-s",
        "--seed",
        dest="seed",
        type=int,
        required=False,
        help="Provide the seed for the random number generator.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
