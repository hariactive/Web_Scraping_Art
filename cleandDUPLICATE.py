import pandas as pd

def remove_duplicates(input_file, output_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Drop duplicates based on only phone number and name, keeping the first occurrence
    df_no_duplicates = df.drop_duplicates(subset=['mobile'], keep='first')

    # Write the cleaned DataFrame to a new CSV file
    df_no_duplicates.to_csv(output_file, index=False)

# Replace 'input_file.csv' and 'output_file.csv' with your actual file names
input_file = 'nagpur_final.csv'
output_file = 'naaga.csv'

remove_duplicates(input_file, output_file)
