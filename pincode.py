import requests
import csv

def get_location_details(pincode):
    api_url = "https://api.postalpincode.in/pincode/"
    response = requests.get(api_url + pincode)
    
    if response.status_code == 200:
        data = response.json()
        
        if data[0]['Status'] == 'Success':
            post_office = data[0]['PostOffice'][0]
            name = post_office['Name']
            region = post_office['Region']
            block = post_office['Block']
            state = post_office['State']
            city_name = post_office['District']
            
            return name, region, block, state, city_name
        else:
            return "City not found", "", "", "", ""
    else:
        return "API request failed", "", "", "", ""

# Read PIN codes from a file and process each one
with open("pincode.txt", "r") as file, open("locations.csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["PIN Code", "Name", "Region", "Block", "State", "City Name"])  # Write header row

    for line in file:
        input_pincode = line.strip()  # Remove leading/trailing whitespace
        name, region, block, state, city_name = get_location_details(input_pincode)
        
        # Print and write to CSV
        print(f"PIN code {input_pincode} corresponds to {city_name}")
        csv_writer.writerow([input_pincode, name, region, block, state, city_name])

print("Results saved to locations.csv")
