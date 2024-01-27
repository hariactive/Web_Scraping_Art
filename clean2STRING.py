import pandas as pd

def remove_medplus_rows(input_file, output_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Remove rows where the 'name' column contains the string "medplus" (case-insensitive)
    df_no_medplus = df[~df['name'].str.lower().str.contains('medplus')]

    # Write the cleaned DataFrame to a new CSV file
    df_no_medplus.to_csv(output_file, index=False)

# Replace 'input_file.csv' and 'output_file.csv' with your actual file names
input_file = 'indore_final.csv'
output_file = 'indorrrr.csv'

remove_medplus_rows(input_file, output_file)
