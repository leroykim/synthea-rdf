import panel as pn
from dua.generator import DUAGenerator
from trustscore.generator import TrustScoreGenerator

PERMITTED_USE_OR_DISCLOSURE = [
    "treatment",
    "payment",
    "health_care_operations",
    "notification",
    "public_health",
    "limited_data_set",
]


DATA_CLASSES = [
    "Allergy",
    "CarePlan",
    "Claim",
    "ClaimTransaction",
    "Condition",
    "Device",
    "Encounter",
    "ImagingStudy",
    "Immunization",
    "Medication",
    "Observation",
    "Organization",
    "Patient",
    "PayerTransition",
    "Payer",
    "Procedure",
    "Provider",
    "Supply",
]


def main():
    pn.extension(sizing_mode="stretch_width")

    # Define a function to generate the dashboard
    def generate_dashboard(
        num_orgs_value,
        num_orgs_dua_value,
        num_user_per_org_value,
        # num_requested_data,
        dataclass_select_value,
        dataclass_portion_slider_value,
        permitted_use_or_disclosure_select_value,
        usage_portion_slider_value,
        random_seed_value,
        save_path_value,
    ):
        # Print the input values to the console
        input_text = (
            f"Number of organizations: {num_orgs_value}\n"
            f"Number of organizations with DUA: {num_orgs_dua_value}\n"
            f"User per organization: {num_user_per_org_value}\n"
            # f"Number of requested data: {num_requested_data}\n"
            f"Random seed: {random_seed_value}\n"
            f"Save path: {save_path_value}\n"
        )
        print(input_text)

        dua_generator = DUAGenerator()
        dua_generator.num_organization = num_orgs_value
        dua_generator.num_dua_org = num_orgs_dua_value
        # dua_generator.num_requested_data = num_requested_data
        dua_generator.main_dataclass = dataclass_select_value
        dua_generator.main_dataclass_portion = dataclass_portion_slider_value
        dua_generator.main_permitted_use_or_disclosure = (
            permitted_use_or_disclosure_select_value
        )
        dua_generator.main_permitted_use_or_disclosure_portion = (
            usage_portion_slider_value
        )
        dua_generator.seed = random_seed_value
        dua_generator.save_path = save_path_value
        dua_generator.generate_dua()
        trustscore_generator = TrustScoreGenerator(
            num_org=num_orgs_value, user_per_org=num_user_per_org_value
        )
        trustscore_generator.generate_trustscore(save_path=save_path_value)

        output_text = f"Output saved to {save_path_value}\n"

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
    # num_requested_data_input = pn.widgets.IntInput(
    #     name="Number of requested data:", value=3
    # )
    random_seed_input = pn.widgets.IntInput(name="Random seed:", value=7)
    save_path_input = pn.widgets.TextInput(name="Save path:", value="../csv")

    # Main data class selection
    dataclass_select = pn.widgets.Select(
        name="Main Data class", options=DATA_CLASSES, value="Patient"
    )

    # Main data class portion
    dataclass_portion_slider = pn.widgets.IntSlider(
        name="Main Data class portion", start=0, end=100, value=70
    )

    # Main permitted use or disclosure
    permitted_use_or_disclosure_select = pn.widgets.Select(
        name="Main permitted use or disclosure",
        options=PERMITTED_USE_OR_DISCLOSURE,
    )
    # Main permitted use or disclosure portion
    usage_portion_slider = pn.widgets.IntSlider(
        name="Main permitted use or disclosure portion", start=0, end=100, value=70
    )

    # Create the button widget and callback function
    button = pn.widgets.Button(name="Generate Data", button_type="primary")
    output_text = pn.pane.Str()

    def button_callback(event):
        input_text, output_text_value = generate_dashboard(
            num_orgs_input.value,
            num_orgs_dua_input.value,
            num_user_per_org_input.value,
            # num_requested_data_input.value,
            dataclass_select.value,
            dataclass_portion_slider.value,
            permitted_use_or_disclosure_select.value,
            usage_portion_slider.value,
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
        # num_requested_data_input,
        random_seed_input,
        save_path_input,
        dataclass_select,
        dataclass_portion_slider,
        permitted_use_or_disclosure_select,
        usage_portion_slider,
        button,
        output_text,
    )

    # Launch the dashboard
    # dashboard.servable()
    pn.serve(dashboard)


if __name__ == "__main__":
    main()
