import pandas as pd
import re

# Load the uploaded files
# TODO CHANGE THIS TO YOUR PATH
master_file_path = '/Users/goodman/Desktop/LiteraryMap/Full AL Collection Master File (Updated Aug 13 2024).xlsm'

# Read the master file
master_file = pd.read_excel(master_file_path, sheet_name=None)

# Hardcoded dictionary of Alabama cities with their respective latitude and longitude
# TODO CHANGE ADD LOCATIONS YOU NEED
alabama_city_coordinates = {
    "Agricultural and Mechanical College of Alabama": (32.6010112, -85.4874569),
    "Alabama A&M University": (34.783368, -86.568755),
    "Alabama College": (33.100674, -86.864136),
    "Alabama Conference Female College": (32.3668052, -86.2999689),
    "Alabama Girls' Industrial School": (33.100674, -86.864136),
    "Alabama Normal College": (34.79981, -87.677251),
    "Alabama Polytechnic Institute": (32.6010112, -85.4874569),
    "Alabama Presbyterian College": (33.659722, -85.831667),
    "Alabama State College": (32.3668052, -86.2999689),
    "Alabama State Normal School": (32.3668052, -86.2999689),
    "Alabama State University": (32.3668052, -86.2999689),
    "Auburn Polytechnic Institute": (32.6010112, -85.4874569),
    "Auburn University": (32.6010112, -85.4874569),
    "Birmingham-Southern College": (33.515381, -86.851527),
    "Centenary Institute": (32.3668052, -86.2999689),
    "Florence State College": (34.79981, -87.677251),
    "Florence State Normal College": (34.79981, -87.677251),
    "Florence State Teachers College": (34.79981, -87.677251),
    "Florence State University": (34.79981, -87.677251),
    "Howard College": (33.4658, -86.7914),
    "Huntingdon College": (32.3503, -86.2843),
    "Jacksonville State College": (33.8288, -85.7635),
    "Jacksonville State Normal School": (33.8288, -85.7635),
    "Jacksonville State Teachers College": (33.8288, -85.7635),
    "Jacksonville State University": (33.8288, -85.7635),
    "Jefferson State Community College": (33.6330, -86.6951),
    "Marion Institute": (32.6326, -87.3194),
    "Marion Military Institute": (32.6326, -87.3194),
    "Samford University": (33.4658, -86.7914),
    "Southern University": (32.7043, -87.5957),
    "State Normal School": (34.79981, -87.677251),
    "Talladega College": (33.4351, -86.1056),
    "Tuscaloosa Female College": (33.2094, -87.5415),
    "Tuskegee Institute": (32.4307, -85.7075),
    "University of Alabama": (33.214023, -87.539024),
    "University of Alabama at Birmingham": (33.5000, -86.8075),
    "University of Montevallo": (33.100674, -86.864136),
    "University of North Alabama": (34.79981, -87.677251),
    "University of South Alabama": (30.696794, -88.178612),
    "West Alabama Agricultural School": (34.1453, -87.9981)
}

# Function to clean biography text
def clean_biography(text):
    if pd.isna(text):
        return ""
    clean_text = re.sub(r'<.*?>', '', text)
    clean_text = re.sub(r';|:</strong>|</p>|<br />|</em>|[^\x00-\x7F]+', '', clean_text)
    return clean_text

# Function to search for residence-related keywords in the cleaned biography text
def extract_info(text):
    # TODO EDIT KEYWORDS TO FIND WHAT YOU NEED
    info_keywords = ["studied", "education", "learned", "degree", "enrolled", "graduate", "attended", "Normal School", "studie", "bachelor"]
    text = clean_biography(text)
    
    for keyword in info_keywords:
        if keyword in text.lower():
            start_idx = max(text.lower().find(keyword) - 30, 0)
            end_idx = min(text.lower().find(keyword) + 100, len(text))
            return text[start_idx:end_idx]
    
    return "NOT FOUND"

# Extract the sheet from the master file
master_sheet = master_file['master_new']

# Creating a new dataframe based on the master sheet
parsed_data = {
    "Last_First": master_sheet["Author_Last_Name_First_Name"],
    "First_Last": master_sheet["Author_First_Name_Last_Name"],
    "info": master_sheet["Author_Biography"].apply(extract_info),
}

# Convert parsed data to DataFrame
parsed_df = pd.DataFrame(parsed_data)

# Alabama cities list (you can extend this list as needed)
alabama_cities = list(alabama_city_coordinates.keys())

# Function to find if an Alabama city is mentioned in the residence text
def find_city(text):
    for city in alabama_cities:
        # Look for city name in the residence text
        if city.lower() in text.lower():
            return city
    return None

# Function to get the hardcoded latitude and longitude for the city
def get_lat_long(city):
    if city in alabama_city_coordinates:
        return alabama_city_coordinates[city]
    return None, None

# Populate latitude and longitude columns based on the city mentioned in info
parsed_df['location'] = parsed_df['info'].apply(find_city)
parsed_df['latitude'], parsed_df['longitude'] = zip(*parsed_df['location'].apply(get_lat_long))

#filter incomplete rows
filtered_df = parsed_df.dropna(subset=['latitude', 'longitude'])
filtered_df = filtered_df.drop_duplicates(subset=['Last_First', 'First_Last'])
# Saving the parsed data with author names, info, and lat/long fields to a CSV file
# TODO CHANGE PATH TO WHERE YOUR OUTPUT WILL GO
output_csv_path = "/Users/goodman/Desktop/LiteraryMap/found.csv"
filtered_df.to_csv(output_csv_path, index=False)

# Create a second DataFrame for rows that are missing latitude and longitude
missing_lat_long_df = parsed_df[parsed_df['latitude'].isna() | parsed_df['longitude'].isna()]
missing_lat_long_df = missing_lat_long_df.drop_duplicates(subset=['Last_First', 'First_Last'])
# Save the rows missing lat/long to a second CSV file
# TODO CHANGE PATH TO WHERE YOUR OUTPUT WILL GO
output_csv_path_missing = "/Users/goodman/Desktop/LiteraryMap/missing.csv"
missing_lat_long_df.to_csv(output_csv_path_missing, index=False)

# Display CSV file path
(output_csv_path, output_csv_path_missing)