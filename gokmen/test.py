import pandas as pd
from openpyxl.styles import NamedStyle
from openpyxl import load_workbook
from datetime import datetime

# Set the input and output file paths
input_path = r"/Users/levent/Desktop/input.xlsx"  # Ensure the file exists here
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f"/Users/levent/Desktop/output_{current_time}.xlsx"


def process_table(input_path, output_path):
    try:
        # Read the input Excel file
        input_df = pd.read_excel(input_path)
    except FileNotFoundError:
        print(f"Error: The file {input_path} was not found.")
        return

    # Process the data
    output_df = input_df.copy()

    # Ensure 'Date' is in datetime format and formatted as "1 January 2024 Monday"
    if "Date" in output_df.columns:
        output_df["Date"] = pd.to_datetime(output_df["Date"]).dt.strftime(
            "%-d %B %Y %A"
        )

    # Transform 'Vol.' column: remove 'K' and multiply by 1000
    if "Vol." in output_df.columns:
        output_df["Vol."] = (
            output_df["Vol."]
            .replace(
                r"[^\d.]", "", regex=True
            )  # Remove non-numeric characters except '.'
            .astype(float)
            * 1000
        )

    # Ensure 'Change %' is in decimal format
    if "Change %" in output_df.columns:
        output_df["Change %"] = output_df["Change %"].round(4)

    # Reset cumulative calculation for each month
    output_df["Month"] = pd.to_datetime(output_df["Date"]).dt.to_period("M")
    cumulative_values = []
    for _, group in output_df.groupby("Month"):
        cumulative = 0
        for val in group["Change %"]:
            cumulative += val
            cumulative_values.append(cumulative)
    output_df["Change % Cumulative"] = cumulative_values

    # Add formulas for "Up/Down" column for each month
    output_df["Up/Down"] = None
    for _, group in output_df.groupby("Month"):
        for i in range(len(group)):
            if i == 0:
                continue  # Skip the first row of each month
            idx = group.index[i]
            prev_idx = group.index[i - 1]
            output_df.loc[idx, "Up/Down"] = (
                f'=IF(H{idx + 2}-H{prev_idx + 2}<0,"Down","Up")'
            )

    # Generate "Up Down" sheet data with specific ranges
    up_down_data = []
    for month, group in output_df.groupby("Month"):
        month_str = month.strftime("%b.%y")  # Format as "Jan.24"
        start_row = group.index[0] + 2  # Excel is 1-based, +2 for the header
        end_row = group.index[-1] + 2
        up_formula = f'=COUNTIF(Output!I{start_row}:I{end_row}, "Up")'
        down_formula = f'=COUNTIF(Output!I{start_row}:I{end_row}, "Down")'
        up_down_data.append([month_str, up_formula, down_formula])

    up_down_df = pd.DataFrame(up_down_data, columns=["Month", "Up", "Down"])

    # Drop the temporary 'Month' column
    output_df.drop(columns=["Month"], inplace=True, errors="ignore")

    # Save the processed DataFrame to Excel
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        # Write the main output data
        output_df.to_excel(writer, index=False, sheet_name="Output")
        # Write the "Up Down" data
        up_down_df.to_excel(writer, index=False, sheet_name="Up Down")

        # Style the sheets
        workbook = writer.book
        worksheet_output = writer.sheets["Output"]
        worksheet_up_down = writer.sheets["Up Down"]

        # Apply percentage style formatting to "Change %" and "Change % Cumulative"
        percentage_style = NamedStyle(name="percentage", number_format="0.00%")
        if "percentage" not in workbook.named_styles:
            workbook.add_named_style(percentage_style)

        for row in range(
            2, len(output_df) + 2
        ):  # Start from row 2 (Excel rows are 1-based)
            if (
                worksheet_output[f"G{row}"].value is not None
            ):  # Ensure 'Change %' is not empty
                worksheet_output[f"G{row}"].style = percentage_style
            if (
                worksheet_output[f"H{row}"].value is not None
            ):  # Ensure 'Change % Cumulative' is not empty
                worksheet_output[f"H{row}"].style = percentage_style

    print(f"Processed file saved to: {output_path}")


# Run the processing function
process_table(input_path, output_path)
