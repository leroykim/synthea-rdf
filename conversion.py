from synthea_rdf.graph import GraphBuilder
from alive_progress import alive_bar
from argparse import ArgumentParser
from pathlib import PurePath, Path


def main():
    args = parse_argument()
    model_path = Path(args.model_path).resolve()
    csv_path = Path(args.csv_path).resolve()
    dest_path = Path(args.dest_path).resolve()
    recursive = args.recursive
    include_dua = args.include_dua

    builder = GraphBuilder(
        csv_dir=csv_path, model_path=model_path, include_dua=include_dua
    )

    if recursive:
        for path in Path(csv_path).iterdir():
            if path.is_dir():
                convert(path, dest_path, builder)
    else:
        convert(csv_path, dest_path, builder)


def convert(csv_path, dest_path, builder):
    print(f"CSV file directory: {csv_path}")
    print(f"Destination directory: {dest_path}")
    print(f"Converting {PurePath(csv_path).name} ...")

    file_name = PurePath(csv_path).name
    graph = builder.build()
    with alive_bar(
        title="Graph Serialization",
        unknown="waves2",
    ) as bar:
        graph.serialize(destination=f"{dest_path}/{file_name}.ttl")
        bar()


def parse_argument():
    parser = ArgumentParser()
    parser.add_argument(
        "-o",
        "--ontology",
        dest="model_path",
        type=str,
        required=True,
        help="Provide model ontology path.",
    )
    parser.add_argument(
        "-csv",
        "--csv-dir",
        dest="csv_path",
        type=str,
        required=True,
        help="Provide Synthea csv directory path.",
    )
    # parser.add_argument("-n", "--filename", dest="file_name", type=str, required=False,
    #                     default=None, help="Provide conversion result file name.")
    parser.add_argument(
        "-dest",
        "--destination",
        dest="dest_path",
        type=str,
        required=False,
        default="result",
        help="Provide destination path of result file.",
    )
    parser.add_argument("-r", dest="recursive", action="store_true", required=False)
    parser.add_argument(
        "-dua",
        "--include-dua",
        dest="include_dua",
        action="store_true",
        default=False,
        required=False,
        help="Include Data Usage Agreement in the conversion.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()

# python3 conversion.py --ontology ./ontology/synthea_ontology --dir ./csv -r
# python3 conversion.py --ontology synthea-rdf/synthea_ontology/synthea_ontology.ttl --csv-dir /home/k163/synthea-rdf/csv/500
# python3 conversion.py --include-dua --ontology synthea_ontology/synthea_ontology.ttl --csv-dir csv/500
