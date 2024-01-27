import requests
import csv

def get_pincode(place):
    api_url = "https://api.postalpincode.in/pincode/"
    try:
        response = requests.get(api_url + place, timeout=10)  # Set a timeout of 10 seconds
        
        if response.status_code == 200:
            data = response.json()
            
            if data[0]['Status'] == 'Success':
                return data[0]['PostOffice'][0]['Pincode']
            else:
                return "PIN code not found"
        else:
            return f"API request failed with status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Read places from a file and process each one
with open("loc_titles_hubli.txt", "r") as file, open("pincode_results.csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Place", "PIN Code"])  # Write header row

    for line in file:
        input_place = line.strip()  # Remove leading/trailing whitespace
        pincode = get_pincode(input_place)
        
        # Print and write to CSV
        print(f"The PIN code for {input_place} is: {pincode}")
        csv_writer.writerow([input_place, pincode])

print("Results saved to pincode_results.csv")
