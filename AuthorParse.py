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
    "Abbeville": (31.5718, -85.2505),
    "Adamsville": (33.5901, -86.9589),
    "Addison": (34.2001, -87.1778),
    "Akron": (32.8768, -87.7406),
    "Alabaster": (33.2443, -86.8164),
    "Albertville": (34.2676, -86.2089),
    "Alexander City": (32.9440, -85.9539),
    "Aliceville": (33.1279, -88.1517),
    "Allgood": (33.9054, -86.5122),
    "Altoona": (34.0234, -86.3195),
    "Andalusia": (31.3088, -86.4836),
    "Anderson": (34.9223, -87.2611),
    "Anniston": (33.6598, -85.8316),
    "Arab": (34.3281, -86.4954),
    "Ardmore": (34.9920, -86.8428),
    "Argo": (33.7012, -86.5180),
    "Ariton": (31.5985, -85.7194),
    "Arley": (34.0812, -87.2147),
    "Ashford": (31.1835, -85.2355),
    "Ashland": (33.2737, -85.8363),
    "Ashville": (33.8401, -86.2647),
    "Athens": (34.8029, -86.9717),
    "Atmore": (31.0243, -87.4941),
    "Attalla": (34.0209, -86.0991),
    "Auburn": (32.6099, -85.4808),
    "Autauga": (32.4340, -86.6547),
    "Autaugaville": (32.4340, -86.6547),
    "Avon": (31.1902, -85.3194),
    "Babbie": (31.2738, -86.3167),
    "Baileyton": (34.2568, -86.6861),
    "Banks": (31.8157, -85.8427),
    "Bay Minette": (30.8829, -87.7731),
    "Bayou La Batre": (30.4058, -88.2477),
    "Bear Creek": (34.2748, -87.7006),
    "Beatrice": (31.7335, -87.2111),
    "Beaverton": (33.9318, -88.0203),
    "Belk": (33.6487, -87.9303),
    "Benton": (32.3065, -86.8186),
    "Berry": (33.6601, -87.6006),
    "Bessemer": (33.4018, -86.9544),
    "Billingsley": (32.6601, -86.7147),
    "Birmingham": (33.5186, -86.8104),
    "Black": (31.0138, -86.0011),
    "Blountsville": (34.0818, -86.5911),
    "Blue Mountain": (33.6776, -85.8577),
    "Blue Ridge": (32.4915, -86.2219),
    "Blue Springs": (31.6635, -85.5016),
    "Boaz": (34.2001, -86.1522),
    "Boligee": (32.7640, -88.0264),
    "Bon Air": (33.2790, -86.3336),
    "Branchville": (33.9298, -86.4222),
    "Brantley": (31.5857, -86.2544),
    "Brent": (32.9379, -87.1644),
    "Brewton": (31.1054, -87.0722),
    "Bridgeport": (34.9484, -85.7144),
    "Brighton": (33.4343, -86.9472),
    "Brilliant": (34.0237, -87.7581),
    "Brookside": (33.6373, -86.9164),
    "Brookwood": (33.2415, -87.3186),
    "Brundidge": (31.7207, -85.8166),
    "Butler": (32.0891, -88.2219),
    "Bynum": (33.6143, -85.9619),
    "Cahaba Heights": (33.4662, -86.7347),
    "Calera": (33.1098, -86.7547),
    "Camden": (31.9910, -87.2908),
    "Camp Hill": (32.8001, -85.6533),
    "Carbon Hill": (33.8918, -87.5261),
    "Cardiff": (33.6446, -86.9314),
    "Carlton": (32.8929, -87.6489),
    "Carolina": (33.1454, -87.7222),
    "Carrollton": (33.2615, -88.0950),
    "Cedar Bluff": (34.2201, -85.6077),
    "Center Point": (33.6415, -86.6814),
    "Centre": (34.1520, -85.6789),
    "Centreville": (32.9445, -87.1386),
    "Chandler Springs": (33.4790, -86.0836),
    "Chelsea": (33.3401, -86.6305),
    "Cherokee": (34.7565, -87.9701),
    "Chickasaw": (30.7635, -88.0747),
    "Childersburg": (33.2779, -86.3705),
    "Citronelle": (31.0902, -88.2486),
    "Clanton": (32.8387, -86.6294),
    "Clay": (33.7026, -86.5997),
    "Clayhatchee": (31.2396, -85.7102),
    "Clayton": (31.8774, -85.4497),
    "Cleveland": (33.9923, -86.5789),
    "Clio": (31.7096, -85.6102),
    "Coaling": (33.1554, -87.3547),
    "Coffee Springs": (31.1602, -86.0066),
    "Coffeeville": (31.7624, -88.0836),
    "Coker": (33.2501, -87.6867),
    "Collinsville": (34.2648, -85.8605),
    "Colony": (33.9487, -86.8853),
    "Columbia": (31.2927, -85.1124),
    "Columbiana": (33.1832, -86.6078),
    "Coosada": (32.5007, -86.3305),
    "Cordova": (33.7598, -87.1836),
    "Cottonwood": (31.0485, -85.3047),
    "County Line": (33.8351, -86.7289),
    "Courtland": (34.6687, -87.3100),
    "Cowarts": (31.1996, -85.3041),
    "Creola": (30.8910, -88.0397),
    "Crossville": (34.2873, -85.9944),
    "Cuba": (32.4318, -88.3728),
    "Cullman": (34.1748, -86.8436),
    "Dadeville": (32.8312, -85.7636),
    "Daleville": (31.3024, -85.7144),
    "Daphne": (30.6035, -87.9019),
    "Dauphin Island": (30.2558, -88.1275),
    "Daviston": (33.0540, -85.6372),
    "Dayton": (32.3493, -87.6422),
    "Deatsville": (32.6024, -86.4019),
    "Decatur": (34.6059, -86.9833),
    "Demopolis": (32.5174, -87.8369),
    "Detroit": (34.0262, -88.1708),
    "Dodge City": (34.0551, -86.8850),
    "Dora": (33.7279, -87.0855),
    "Dothan": (31.2232, -85.3905),
    "Double Springs": (34.1465, -87.4019),
    "Douglas": (34.1715, -86.3208),
    "Dozier": (31.4957, -86.3664),
    "Dutton": (34.6059, -85.9172),
    "East Brewton": (31.0957, -87.0533),
    "Eclectic": (32.6351, -86.0341),
    "Edgewater": (33.5254, -86.9975),
    "Edwardsville": (33.7787, -85.5122),
    "Elba": (31.4182, -86.0744),
    "Elberta": (30.4143, -87.5978),
    "Eldridge": (33.9212, -87.6225),
    "Elkmont": (34.9312, -86.9783),
    "Elmore": (32.5429, -86.3122),
    "Emelle": (32.7285, -88.3139),
    "Enterprise": (31.3152, -85.8552),
    "Epes": (32.6874, -88.1203),
    "Ethelsville": (33.4204, -88.2200),
    "Eufaula": (31.8918, -85.1455),
    "Eutaw": (32.8404, -87.8875),
    "Eva": (34.3248, -86.7558),
    "Evergreen": (31.4335, -86.9569),
    "Excel": (31.4263, -87.3403),
    "Fairfield": (33.4859, -86.9119),
    "Fairhope": (30.5229, -87.9033),
    "Fairview": (34.2462, -86.6911),
    "Falkville": (34.3679, -86.9089),
    "Faunsdale": (32.4574, -87.5936),
    "Fayette": (33.6846, -87.8308),
    "Five Points": (32.8512, -85.3522),
    "Flomaton": (31.0074, -87.2597),
    "Florala": (31.0052, -86.3247),
    "Florence": (34.7998, -87.6773),
    "Foley": (30.4069, -87.6836),
    "Forestdale": (33.5793, -86.9039),
    "Fort Deposit": (31.9846, -86.5780),
    "Fort Payne": (34.4443, -85.7194),
    "Fort Rucker": (31.3435, -85.7080),
    "Franklin": (32.4557, -85.8028),
    "Frisco City": (31.4335, -87.4022),
    "Fulton": (31.7857, -87.7203),
    "Fultondale": (33.6165, -86.8017),
    "Fyffe": (34.4467, -85.9047),
    "Gadsden": (34.0143, -86.0066),
    "Gainesville": (32.8185, -88.1589),
    "Gantt": (31.4074, -86.4836),
    "Garden City": (34.0084, -86.7483),
    "Gardendale": (33.6601, -86.8128),
    "Gaylesville": (34.2687, -85.5572),
    "Geiger": (32.8671, -88.3078),
    "Geneva": (31.0327, -85.8644),
    "Georgiana": (31.6374, -86.7419),
    "Geraldine": (34.3526, -85.9447),
    "Gilbertown": (31.8813, -88.3189),
    "Glen Allen": (33.8959, -87.7314),
    "Glencoe": (33.9570, -85.9322),
    "Glenwood": (31.6624, -86.1733),
    "Goldville": (33.0893, -85.7836),
    "Good Hope": (34.1151, -86.8644),
    "Goodwater": (33.0657, -86.0533),
    "Gordo": (33.3207, -87.9028),
    "Gordon": (31.1327, -85.0958),
    "Gordonville": (32.1457, -86.7278),
    "Goshen": (31.7188, -86.1225),
    "Grant": (34.5009, -86.2544),
    "Graysville": (33.6165, -86.9717),
    "Greensboro": (32.7040, -87.5958),
    "Greenville": (31.8296, -86.6194),
    "Grove Hill": (31.7074, -87.7775),
    "Guin": (33.9654, -87.9153),
    "Gulf Shores": (30.2460, -87.7008),
    "Guntersville": (34.3581, -86.2947),
    "Gurley": (34.7012, -86.3744),
    "Hackleburg": (34.2773, -87.8328),
    "Haleburg": (31.4182, -85.1397),
    "Hamilton": (34.1423, -87.9889),
    "Hammondville": (34.5668, -85.6361),
    "Hanceville": (34.0629, -86.7672),
    "Harpersville": (33.3265, -86.4344),
    "Hartford": (31.1024, -85.6969),
    "Hartselle": (34.4434, -86.9403),
    "Hayden": (33.8937, -86.7533),
    "Hayneville": (32.1840, -86.5803),
    "Headland": (31.3513, -85.3422),
    "Heath": (32.3401, -86.4633),
    "Heflin": (33.6457, -85.5844),
    "Helena": (33.2962, -86.8439),
    "Henagar": (34.6351, -85.7444),
    "Highland Lake": (33.8923, -86.4236),
    "Hillsboro": (34.6401, -87.1919),
    "Hobson City": (33.6326, -85.8316),
    "Hodges": (34.3276, -87.9236),
    "Hokes Bluff": (33.9985, -85.8655),
    "Holly Pond": (34.1762, -86.6200),
    "Hollywood": (34.7176, -85.9711),
    "Homewood": (33.4719, -86.8086),
    "Hoover": (33.4054, -86.8114),
    "Horn Hill": (31.2371, -86.3039),
    "Hueytown": (33.4287, -86.9989),
    "Huntsville": (34.7304, -86.5861),
    "Hurtsboro": (32.2407, -85.4161),
    "Hytop": (34.9037, -86.0833),
    "Ider": (34.7062, -85.6775),
    "Indian Springs Village": (33.3679, -86.7525),
    "Irondale": (33.5382, -86.7072),
    "Jackson": (31.5087, -87.8944),
    "Jackson's Gap": (32.8851, -85.8144),
    "Jacksonville": (33.8137, -85.7611),
    "Jasper": (33.8318, -87.2775),
    "Jemison": (32.9576, -86.7444),
    "Kansas": (33.9048, -87.5578),
    "Kennedy": (33.5845, -87.9903),
    "Killen": (34.8623, -87.5378),
    "Kimberly": (33.7707, -86.8011),
    "Kinsey": (31.2932, -85.3436),
    "Kinston": (31.2188, -86.1708),
    "Lafayette": (32.8998, -85.4011),
    "Lake Purdy": (33.4345, -86.6419),
    "Lake View": (33.2790, -87.1355),
    "Lanett": (32.8687, -85.1894),
    "Langston": (34.5359, -86.0911),
    "Leeds": (33.5482, -86.5444),
    "Leesburg": (34.1798, -85.7705),
    "Leighton": (34.7001, -87.5314),
    "Lester": (34.9843, -87.1483),
    "Level Plains": (31.2971, -85.7611),
    "Lexington": (34.9654, -87.3750),
    "Liberty": (32.1332, -85.7922),
    "Lincoln": (33.6154, -86.1419),
    "Linden": (32.3065, -87.7986),
    "Lineville": (33.3112, -85.7533),
    "Lipscomb": (33.4301, -86.9289),
    "Lisman": (32.1724, -88.2889),
    "Littleville": (34.5901, -87.6750),
    "Livingston": (32.5848, -88.1872),
    "Loachapoka": (32.6132, -85.5955),
    "Lockhart": (31.0113, -86.3500),
    "Locust Fork": (33.8901, -86.6311),
    "Louisville": (31.7799, -85.5558),
    "Lowndesboro": (32.2754, -86.6161),
    "Loxley": (30.6324, -87.7547),
    "Luverne": (31.7168, -86.2644),
    "Lynn": (34.0473, -87.5497),
    "Madison": (34.6993, -86.7483),
    "Madrid": (31.0363, -85.3825),
    "Magnolia Springs": (30.3963, -87.7761),
    "Malvern": (31.1399, -85.5197),
    "Maplesville": (32.7832, -86.8747),
    "Margaret": (33.6790, -86.4811),
    "Marion": (32.6323, -87.3192),
    "Marion Junction": (32.4718, -87.2522),
    "Maytown": (33.5537, -86.9928),
    "McCalla": (33.3512, -87.0047),
    "McKenzie": (31.5396, -86.7197),
    "McMullen": (33.1501, -87.6561),
    "Memphis": (34.7462, -87.4647),
    "Mentone": (34.5712, -85.5797),
    "Midfield": (33.4565, -86.9236),
    "Midland City": (31.3052, -85.4911),
    "Midway": (32.0774, -85.5144),
    "Millbrook": (32.4790, -86.3619),
    "Millport": (33.5651, -88.0831),
    "Millry": (31.6296, -88.3289),
    "Mobile": (30.6954, -88.0399),
    "Monroeville": (31.5274, -87.3247),
    "Montevallo": (33.1040, -86.8644),
    "Montgomery": (32.3792, -86.3077),
    "Moody": (33.5912, -86.4911),
    "Mooresville": (34.6265, -86.8803),
    "Morris": (33.7482, -86.8089),
    "Mosses": (32.1793, -86.6747),
    "Moulton": (34.4815, -87.2939),
    "Moundville": (32.9979, -87.6278),
    "Mount Vernon": (31.0885, -88.0147),
    "Mountain Brook": (33.4857, -86.7361),
    "Mulga": (33.5537, -86.9797),
    "Muscle Shoals": (34.7448, -87.6675),
    "Myrtlewood": (32.2304, -87.9453),
    "Napier Field": (31.3213, -85.4483),
    "Natural Bridge": (34.0915, -87.6039),
    "Nauvoo": (33.9898, -87.4861),
    "Nectar": (33.9732, -86.6311),
    "Needham": (31.9835, -88.0147),
    "New Brockton": (31.3824, -85.9244),
    "New Hope": (34.5373, -86.3944),
    "New Market": (34.9115, -86.4261),
    "New Site": (32.9415, -85.7858),
    "Newton": (31.3368, -85.6022),
    "Newville": (31.4174, -85.3369),
    "North Courtland": (34.6693, -87.3194),
    "North Johns": (33.4537, -87.1050),
    "Northport": (33.2290, -87.5772),
    "Notasulga": (32.5632, -85.6675),
    "Oak Grove": (33.1854, -87.2997),
    "Oak Hill": (31.9018, -86.3422),
    "Oakman": (33.7129, -87.3867),
    "Odenville": (33.6768, -86.3980),
    "Ohatchee": (33.7818, -86.0388),
    "Oneonta": (33.9487, -86.4722),
    "Onycha": (31.3188, -86.3169),
    "Opelika": (32.6454, -85.3783),
    "Opp": (31.2835, -86.2547),
    "Orange Beach": (30.2697, -87.5867),
    "Orrville": (32.3068, -87.2469),
    "Owens Cross Roads": (34.5854, -86.4583),
    "Oxford": (33.6143, -85.8355),
    "Ozark": (31.4590, -85.6400),
    "Paint Rock": (34.6598, -86.3269),
    "Parrish": (33.7315, -87.2861),
    "Pelham": (33.2859, -86.8097),
    "Pell City": (33.5857, -86.2861),
    "Pennington": (32.1957, -88.0506),
    "Petrey": (31.8496, -86.2044),
    "Phenix City": (32.4700, -85.0007),
    "Phil Campbell": (34.3515, -87.7072),
    "Pickensville": (33.2315, -88.2728),
    "Piedmont": (33.9243, -85.6133),
    "Pike Road": (32.2790, -86.1394),
    "Pinckard": (31.3135, -85.5477),
    "Pine Apple": (31.8685, -86.9900),
    "Pine Hill": (31.9857, -87.5933),
    "Pine Ridge": (34.3790, -85.9311),
    "Pinson": (33.6885, -86.6836),
    "Pisgah": (34.6859, -85.8494),
    "Pleasant Grove": (33.4901, -86.9889),
    "Pleasant Groves": (34.4176, -86.9517),
    "Pollard": (31.0271, -87.1736),
    "Powell": (34.5334, -85.8919),
    "Prattville": (32.4640, -86.4597),
    "Priceville": (34.5229, -86.8961),
    "Prichard": (30.7388, -88.0797),
    "Providence": (31.3621, -87.7775),
    "Ragland": (33.7445, -86.1433),
    "Rainbow City": (33.9529, -86.0419),
    "Rainsville": (34.4948, -85.8477),
    "Ranburne": (33.5271, -85.3397),
    "Red Bay": (34.4398, -88.1403),
    "Red Level": (31.4035, -86.6086),
    "Redstone Arsenal": (34.6682, -86.6647),
    "Reece City": (34.0776, -86.0322),
    "Reform": (33.3829, -88.0150),
    "Rehobeth": (31.1288, -85.4436),
    "Repton": (31.4074, -87.2361),
    "River Falls": (31.3549, -86.5344),
    "Riverside": (33.6062, -86.2047),
    "Riverview": (32.4857, -86.5522),
    "Roanoke": (33.1529, -85.3722),
    "Robertsdale": (30.5543, -87.7105),
    "Rochester": (34.2787, -86.2586),
    "Rock Creek": (33.4843, -87.0647),
    "Rockford": (32.8890, -86.2194),
    "Rogers": (34.9843, -87.5786),
    "Rosa": (34.0326, -86.2089),
    "Russellville": (34.5088, -87.7283),
    "Rutledge": (31.7346, -86.3108),
    "Samson": (31.1179, -86.0455),
    "Sand Rock": (34.2362, -85.7669),
    "Sanford": (31.2935, -86.3922),
    "Saraland": (30.8207, -88.0703),
    "Sardis City": (34.1787, -86.1178),
    "Satsuma": (30.8532, -88.0547),
    "Scottsboro": (34.6723, -86.0341),
    "Section": (34.5784, -85.9897),
    "Selma": (32.4074, -87.0211),
    "Sheffield": (34.7565, -87.7017),
    "Shiloh": (34.3679, -85.8877),
    "Shorter": (32.4018, -85.9372),
    "Silverhill": (30.5457, -87.7500),
    "Sipsey": (33.8237, -87.0847),
    "Skyline": (34.8029, -86.1322),
    "Slocomb": (31.1013, -85.5958),
    "Smiths Station": (32.5379, -85.1033),
    "Snead": (34.1087, -86.3944),
    "Somerville": (34.4715, -86.7989),
    "South Vinemont": (34.2351, -86.8625),
    "Southside": (33.9223, -86.0258),
    "Spanish Fort": (30.7219, -87.9125),
    "Spring Garden": (33.8851, -85.5511),
    "Spring Hill": (30.6757, -88.1264),
    "Springville": (33.7737, -86.4722),
    "St. Florian": (34.8729, -87.6253),
    "Steele": (33.9412, -86.2033),
    "Stevenson": (34.8698, -85.8361),
    "Sulligent": (33.9029, -88.1314),
    "Sumiton": (33.7479, -87.0453),
    "Summerdale": (30.4877, -87.7003),
    "Susan Moore": (34.0815, -86.4122),
    "Sweet Water": (32.0974, -87.8586),
    "Sylacauga": (33.1732, -86.2503),
    "Sylvan Springs": (33.5254, -87.0047),
    "Sylvania": (34.5590, -85.8122),
    "Talladega": (33.4359, -86.1000),
    "Talladega Springs": (33.1737, -86.3647),
    "Tallassee": (32.5340, -85.8988),
    "Tarrant": (33.5901, -86.7747),
    "Taylor": (31.1685, -85.4661),
    "Theodore": (30.5438, -88.1742),
    "Thomaston": (32.2668, -87.6256),
    "Thomasville": (31.9135, -87.7375),
    "Thorsby": (32.9165, -86.7122),
    "Town Creek": (34.6726, -87.4083),
    "Toxey": (31.9157, -88.3089),
    "Trafford": (33.8201, -86.7450),
    "Triana": (34.5865, -86.7458),
    "Trinity": (34.6065, -87.0875),
    "Troy": (31.8088, -85.9699),
    "Trussville": (33.6198, -86.6089),
    "Tuscaloosa": (33.2098, -87.5692),
    "Tuscumbia": (34.7312, -87.7017),
    "Tuskegee": (32.4307, -85.7077),
    "Twin": (34.0734, -87.6336),
    "Union": (32.9501, -87.1336),
    "Union Grove": (34.4037, -86.4522),
    "Union Springs": (32.1443, -85.7144),
    "Uniontown": (32.4501, -87.5139),
    "Valley": (32.8187, -85.1791),
    "Valley Grande": (32.4901, -87.0389),
    "Valley Head": (34.5687, -85.6119),
    "Vance": (33.1762, -87.2286),
    "Vernon": (33.7579, -88.1075),
    "Vestavia Hills": (33.4487, -86.7878),
    "Vina": (34.3748, -88.0531),
    "Vincent": (33.3873, -86.4167),
    "Vredenburgh": (31.8043, -87.3097),
    "Wadley": (33.1232, -85.5669),
    "Waldo": (33.6876, -86.0341),
    "Walnut Grove": (34.0712, -86.2811),
    "Warrior": (33.8173, -86.8133),
    "Waterloo": (34.9176, -88.0642),
    "Waverly": (32.7351, -85.5727),
    "Weaver": (33.7490, -85.8105),
    "Webb": (31.2610, -85.2855),
    "Wedowee": (33.3065, -85.4847),
    "West Blocton": (33.1154, -87.1247),
    "West Jefferson": (33.6451, -87.0872),
    "West Point": (34.1437, -86.9486),
    "Westover": (33.3429, -86.5472),
    "Wetumpka": (32.5448, -86.2122),
    "White Hall": (32.3154, -86.7094),
    "Wilsonville": (33.2337, -86.4836),
    "Wilton": (33.0818, -86.8847),
    "Winfield": (33.9290, -87.8169),
    "Woodland": (33.3743, -85.3972),
    "Woodstock": (33.2176, -87.1503),
    "Woodville": (34.6248, -86.2744),
    "Yellow Bluff": (31.9596, -87.4814),
    "York": (32.4868, -88.2961)
    # TODO Add all cities/ locations
    # You can continue to add more cities as necessary
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
    info_keywords = ["childhood home", "home", "lived in", "resided", "resides", "moved to", "practiced", "career", "business", "taught"]
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
missing_lat_long_df = parsed_df[parsed_df['latitude'].isna() | parsed_df['location'].isna()]
missing_lat_long_df = missing_lat_long_df.drop_duplicates(subset=['Last_First', 'First_Last'])
# Save the rows missing lat/long to a second CSV file
# TODO CHANGE PATH TO WHERE YOUR OUTPUT WILL GO
output_csv_path_missing = "/Users/goodman/Desktop/LiteraryMap/missing.csv"
missing_lat_long_df.to_csv(output_csv_path_missing, index=False)

# Display CSV file path
(output_csv_path, output_csv_path_missing)