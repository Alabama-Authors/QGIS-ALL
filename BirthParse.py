import json
import pandas as pd
import re

# Load the uploaded files
master_filePath = '/Users/thomaslander/Desktop/AL_Authors_QGIS/data/Full AL Collection Master File (Updated Aug 13 2024).xlsm'

# Read the master file
master_file = pd.read_excel(master_filePath, sheet_name='master_new')

# Hardcoded dictionary of Alabama towns and cities with their respective latitude and longitude
# The list is far too long for readability's sake, so it is stored in a separate json file
with open("alabama_city_coordinates.json", "r") as f:
    alabama_city_coordinates = json.load(f)

# Hardcoded dictionary of Alabama counties with their respective latitude and longitude
alabama_county_coordinates = {
    "Autauga County": (32.5789, -86.6424),
    "Baldwin County": (30.7278, -87.7221),
    "Barbour County": (31.8705, -85.4050),
    "Bibb County": (32.9960, -87.1272),
    "Blount Coutny": (33.9965, -86.5679),
    "Bullock County": (32.0877, -85.7161),
    "Butler County": (31.7514, -86.6852),
    "Calhoun County": (33.7702, -85.8263),
    "Chambers County": (32.9024, -85.3549),
    "Cherokee County": (34.1782, -85.6067),
    "Chilton County": (32.9944, -86.7175),
    "Choctaw County": (32.0179, -88.2547),
    "Clarke County": (31.6804, -87.8357),
    "Clay County": (33.2777, -85.8603),
    "Cleburne County": (33.6775, -85.5200),
    "Coffee County": (31.4055, -85.9891),
    "Colbert County": (34.7118, -87.8368),
    "Conecuh County": (31.4231, -87.1236),
    "Coosa County": (32.9464, -86.2294),
    "Covington County": (31.2406, -86.4402),
    "Crenshaw County": (31.6680, -86.3151),
    "Cullman County": (34.1526, -86.8436),
    "Dale County": (31.4245, -85.6073),
    "Dallas County": (32.3545, -87.1183),
    "DeKalb County": (34.4599, -85.8074),
    "Elmore County": (32.6020, -86.2148),
    "Escambia County": (31.1256, -87.1598),
    "Etowah County": (34.0459, -86.0402),
    "Fayette County": (33.7272, -87.7488),
    "Franklin County": (34.4418, -87.8420),
    "Geneva County": (31.0840, -85.8478),
    "Greene County": (32.8403, -87.9414),
    "Hale County": (32.7628, -87.6272),
    "Henry County": (31.5704, -85.1894),
    "Houston County": (31.1561, -85.3559),
    "Jackson County": (34.7621, -85.9668),
    "Jefferson County": (33.5446, -86.9292),
    "Lamar County": (33.7806, -88.0934),
    "Lauderdale County": (34.8849, -87.6581),
    "Lawrence County": (34.5264, -87.3108),
    "Lee County": (32.6019, -85.3548),
    "Limestone County": (34.7981, -86.9478),
    "Lowndes County": (32.2492, -86.6501),
    "Macon County": (32.3938, -85.6986),
    "Madison County": (34.7562, -86.5611),
    "Marengo County": (32.2621, -87.6879),
    "Marion County": (34.1449, -87.9075),
    "Marshall County": (34.3223, -86.4997),
    "Mobile County": (30.6592, -88.0965),
    "Monroe County": (31.5924, -87.3657),
    "Montgomery County": (32.2332, -86.2086),
    "Morgan County": (34.4667, -86.8569),
    "Perry County": (32.6364, -87.2972),
    "Pickens County": (33.2615, -88.0881),
    "Pike County": (31.8003, -86.0239),
    "Randolph County": (33.3016, -85.4513),
    "Russell County": (32.3029, -85.1894),
    "St. Clair County": (33.7285, -86.3109),
    "Shelby County": (33.2395, -86.6611),
    "Sumter County": (32.6656, -88.0819),
    "Talladega County": (33.3774, -86.1511),
    "Tallapoosa County": (32.8131, -85.7851),
    "Tuscaloosa County": (33.2096, -87.5241),
    "Walker County": (33.8088, -87.2802),
    "Washington County": (31.3939, -88.2098),
    "Wilcox County": (31.9875, -87.3061),
    "Winston County": (34.1455, -87.3667)
}


# Function to clean biography text
def clean_biography(text):
    if pd.isna(text):
        return ""
    clean_text = re.sub(r'<.*?>', '', text)
    clean_text = re.sub(r';|:</strong>|</p>|<br />|</em>|[^\x00-\x7F]+', '', clean_text)
    return clean_text

# Function to search for birthplace in the cleaned biography text
def extract_info(text):
    info_keywords = ["Born", "born", "Born in", "born in"]
    text = clean_biography(text)
    
    for keyword in info_keywords:
        if keyword in text:
            start_idx = max(text.find(keyword) - 30, 0)
            end_idx = min(text.find(keyword) + 100, len(text))
            return text[start_idx:end_idx]
    
    return "NOT FOUND"

# Extract the sheet from the master file
master_sheet = master_file

# Creating a new dataframe based on the master sheet
parsed_data = {
    "Last_First": master_sheet["Author_Last_Name_First_Name"],
    "First_Last": master_sheet["Author_First_Name_Last_Name"],
    "info": master_sheet["Author_Biography"].apply(extract_info),
}

# Convert parsed data to DataFrame
parsed_df = pd.DataFrame(parsed_data)

# Lists of Alabama cities and counties
alabama_cities = list(alabama_city_coordinates.keys())
alabama_counties = list(alabama_county_coordinates.keys())

# Function to find if an Alabama city is mentioned in the biography text
def find_city_or_county(text):
    for city in alabama_cities:
        if city.lower() in text.lower():
            return city
    for county in alabama_counties:
        if county.lower() in text.lower():
            return county 
    return None

# Function to get latitude and longitude for the found city
def get_lat_long(place):
    if place in alabama_county_coordinates:
        return alabama_county_coordinates[place]
    if place in alabama_city_coordinates:
        return alabama_city_coordinates[place]
    return None, None

# Apply functions to find city and get coordinates
parsed_df['Birthplace'] = parsed_df['info'].apply(find_city_or_county)
parsed_df['Latitude'], parsed_df['Longitude'] = zip(*parsed_df['Birthplace'].apply(get_lat_long))

# Remove duplicates based on Last_First, First_Last, and Birthplace
parsed_df.drop_duplicates(subset=['Last_First', 'First_Last', 'Birthplace'], inplace=True)

# Filter for rows with complete information, will go back later by hand or by AI
filtered_df = parsed_df.dropna(subset=['Latitude', 'Longitude'])

# Separate entries within Alabama and those outside Alabama or missing coordinates
in_alabama_df = filtered_df.dropna(subset=['Latitude', 'Longitude'])
outside_alabama_df = parsed_df[parsed_df['Birthplace'].isna() | \
                               (parsed_df['Birthplace'].isin(alabama_cities or alabama_counties) == False)]

# Format the output for Alabama authors
in_alabama_df['Formatted_Output'] = in_alabama_df.apply(
    lambda row: f'"{row["Last_First"]}", "{row["First_Last"]}", {row["Birthplace"]}, {row["Latitude"]}, {row["Longitude"]},',
    axis=1
)

# Save Alabama authors to a CSV
output_csv_path_alabama = "/Users/thomaslander/Desktop/AL_Authors_QGIS/data/Formatted_AL_Authors.csv"
in_alabama_df[['Formatted_Output']].to_csv(output_csv_path_alabama, index=False, header=False)

# Format and save the output for authors outside of Alabama or missing coordinates
outside_alabama_df['Formatted_Output'] = outside_alabama_df.apply(
    lambda row: f'"{row["Last_First"]}","{row["First_Last"]}",{row["info"]},,,',
    axis=1
)

output_csv_path_outside = "/Users/thomaslander/Desktop/AL_Authors_QGIS/data/Authors_Outside_Alabama.csv"
outside_alabama_df[['Formatted_Output']].to_csv(output_csv_path_outside, index=False, header=False)

print(f"Formatted CSV saved for Alabama authors at: {output_csv_path_alabama}")
print(f"Formatted CSV saved for authors outside Alabama or with unknown cities at: {output_csv_path_outside}")