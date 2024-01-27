file_path = 'jio11.txt'

# Read the file content
with open(file_path, 'r') as file:
    lines = file.readlines()

# Remove the suffix from each line
modified_lines = [line.strip().replace('-site:1mg.com', '') for line in lines]

# Save the modified content back to the file
with open(file_path, 'w') as file:
    file.write('\n'.join(modified_lines))

print(f'The suffix has been removed from the file: {file_path}')
