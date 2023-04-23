import panel as pn
from dua.generator import DUAGenerator
from trustscore.generator import TrustScoreGenerator


def main():
    pn.extension(sizing_mode="stretch_width")

    # Define a function to generate the dashboard
    def generate_dashboard(
        num_orgs,
        num_orgs_dua,
        num_user_per_org,
        num_requested_data,
        random_seed,
        save_path,
    ):
        # Print the input values to the console
        input_text = (
            f"Number of organizations: {num_orgs}\n"
            f"Number of organizations with DUA: {num_orgs_dua}\n"
            f"User per organization: {num_user_per_org}\n"
            f"Number of requested data: {num_requested_data}\n"
            f"Random seed: {random_seed}\n"
            f"Save path: {save_path}\n"
        )
        print(input_text)

        dua_generator = DUAGenerator()
        dua_generator.generate_dua(
            num_organization=num_orgs,
            num_dua_org=num_orgs_dua,
            num_requested_data=num_requested_data,
            seed=random_seed,
            save_path=save_path,
        )
        trustscore_generator = TrustScoreGenerator(
            num_org=num_orgs, user_per_org=num_user_per_org
        )
        trustscore_generator.generate_trustscore(save_path=save_path)

        output_text = f"Output saved to {save_path}\n"

        print(output_text)

        # Return the input and output text
        return input_text, output_text

    # Create the input widgets
    num_orgs_input = pn.widgets.IntInput(name="Number of organizations:", value=10)
    num_orgs_dua_input = pn.widgets.IntInput(
        name="Number of organizations with DUA:", value=5
    )
    num_user_per_org_input = pn.widgets.IntInput(
        name="User per organization:", value=10
    )
    num_requested_data_input = pn.widgets.IntInput(
        name="Number of requested data:", value=3
    )
    random_seed_input = pn.widgets.IntInput(name="Random seed:", value=7)
    save_path_input = pn.widgets.TextInput(name="Save path:", value="../csv")

    # Create the button widget and callback function
    button = pn.widgets.Button(name="Generate Dashboard")
    output_text = pn.pane.Str()

    def button_callback(event):
        input_text, output_text_value = generate_dashboard(
            num_orgs_input.value,
            num_orgs_dua_input.value,
            num_user_per_org_input.value,
            num_requested_data_input.value,
            random_seed_input.value,
            save_path_input.value,
        )
        # Set the output text value and update the widget
        output_text.object = input_text + output_text_value
        output_text.param.trigger("object")

    button.on_click(button_callback)

    # Create the dashboard layout
    dashboard = pn.Column(
        "# DUA and Trust Score Generator",
        num_orgs_input,
        num_orgs_dua_input,
        num_user_per_org_input,
        num_requested_data_input,
        random_seed_input,
        save_path_input,
        button,
        output_text,
    )

    # Launch the dashboard
    pn.serve(dashboard)


if __name__ == "__main__":
    main()
