input_file_path = "jio11.txt"
output_file_path = "jio_modified.txt"  # You can change the output file name if needed

# Open the input file in read mode
with open(input_file_path, 'r') as input_file:
    # Read all lines from the input file
    lines = input_file.readlines()

# Open the output file in write mode
with open(output_file_path, 'w') as output_file:
    # Iterate through each line and add the desired string
    for line in lines:
        modified_line = line.strip() + " -site:1mg.com\n"  # Add the desired string
        output_file.write(modified_line)

print("Script execution completed. Check", output_file_path, "for the modified content.")
