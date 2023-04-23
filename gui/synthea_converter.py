import io
import sys
from contextlib import contextmanager
from pathlib import PurePath, Path
import panel as pn
from alive_progress import alive_bar
from synthea_rdf.graph import GraphBuilder


# Custom print function
class PrintToOutput(io.StringIO):
    def __init__(self, output):
        self.output = output
        self.current_line = ""
        super().__init__()

    def write(self, text):
        for char in text:
            if char == "\r":
                self.current_line = ""
            elif char == "\n":
                self.output.value += self.current_line + char
                self.current_line = ""
            else:
                self.current_line += char

        super().write(text)

    def flush(self):
        pass


def main():
    pn.extension(sizing_mode="stretch_width")

    @contextmanager
    def capture_print(output):
        old_stdout = sys.stdout
        sys.stdout = PrintToOutput(output)
        try:
            yield
        finally:
            sys.stdout = old_stdout

    # Method to be run on button click
    def generate_dataset(
        synthea_ontology_path_input,
        synthea_csv_directory_path_input,
        destination_directory_path_input,
        include_trustscore_input,
        include_dua_input,
    ):
        print(f"Synthea Ontology Path: {synthea_ontology_path_input}")
        print(f"Synthea CSV data Directory: {synthea_csv_directory_path_input}")
        print(f"Include TrustScore: {include_trustscore_input}")
        print(f"Include DUA: {include_dua_input}")
        print(f"Destination Path: {destination_directory_path_input}")

        model_path = Path(synthea_ontology_path_input).resolve()
        csv_path = Path(synthea_csv_directory_path_input).resolve()
        dest_path = Path(destination_directory_path_input).resolve()
        builder = GraphBuilder(
            csv_dir=csv_path,
            model_path=model_path,
            include_trustscore=include_trustscore_input,
            include_dua=include_dua_input,
        )
        file_name = PurePath(dest_path).name
        graph = builder.build()
        with alive_bar(
            title="Graph Serialization",
            unknown="waves2",
        ) as bar:
            graph.serialize(
                destination=f"{destination_directory_path_input}/{file_name}.ttl"
            )
            bar()

        print("Dataset generation complete!")

    # Input widgets
    str_input1 = pn.widgets.TextInput(
        name="Synthea Ontology Path", value="../synthea_ontology/synthea_ontology.ttl"
    )
    str_input2 = pn.widgets.TextInput(
        name="Synthea CSV data Directory Path", value="../csv/500-veracity"
    )
    str_input3 = pn.widgets.TextInput(
        name="Destination Directory Path", value="../result"
    )
    bool_input1 = pn.widgets.Checkbox(name="Include TrustScore", value=True)
    bool_input2 = pn.widgets.Checkbox(name="Include DUA", value=True)
    button = pn.widgets.Button(name="Generate Dataset")
    output = pn.widgets.TextAreaInput(name="Log", height=600)

    # Function to run on button click
    def on_click(event):
        with capture_print(output):
            generate_dataset(
                str_input1.value,
                str_input2.value,
                str_input3.value,
                bool_input1.value,
                bool_input2.value,
            )

    button.on_click(on_click)

    # Create dashboard layout
    dashboard = pn.Column(
        "# Synthea CSV to Graph Data Converter",
        pn.Row(str_input1, str_input2, str_input3),
        pn.Row(bool_input1, bool_input2),
        output,
        button,
    )

    pn.serve(dashboard)


if __name__ == "__main__":
    main()
