import math

FACTORIES = {
    "Lot's O' Nuts": {"lat": 32.881893, "lon": -111.768036, "city": "Casa Grande", "state": "Arizona", "division": "Chocolate"},
    "Wicked Choccy's": {"lat": 32.076176, "lon": -81.088371, "city": "Savannah", "state": "Georgia", "division": "Chocolate"},
    "Sugar Shack": {"lat": 48.11914, "lon": -96.18115, "city": "Thief River Falls", "state": "Minnesota", "division": "Sugar"},
    "Secret Factory": {"lat": 41.446333, "lon": -90.565487, "city": "Rock Island", "state": "Illinois", "division": "Sugar/Other"},
    "The Other Factory": {"lat": 35.1175, "lon": -89.971107, "city": "Memphis", "state": "Tennessee", "division": "Other"}
}

PRODUCT_FACTORY_MAP = {
    'Wonka Bar - Nutty Crunch Surprise': "Lot's O' Nuts",
    'Wonka Bar - Fudge Mallows': "Lot's O' Nuts",
    'Wonka Bar -Scrumdiddlyumptious': "Lot's O' Nuts",
    'Wonka Bar - Milk Chocolate': "Wicked Choccy's",
    'Wonka Bar - Triple Dazzle Caramel': "Wicked Choccy's",
    'Laffy Taffy': "Sugar Shack",
    'SweeTARTS': "Sugar Shack",
    'Nerds': "Sugar Shack",
    'Fun Dip': "Sugar Shack",
    'Fizzy Lifting Drinks': "Sugar Shack",
    'Everlasting Gobstopper': "Secret Factory",
    'Hair Toffee': "The Other Factory",
    'Lickable Wallpaper': "Secret Factory",
    'Wonka Gum': "Secret Factory",
    'Kazookles': "The Other Factory"
}

PRODUCT_DIVISION_MAP = {
    'Wonka Bar - Nutty Crunch Surprise': 'Chocolate',
    'Wonka Bar - Fudge Mallows': 'Chocolate',
    'Wonka Bar -Scrumdiddlyumptious': 'Chocolate',
    'Wonka Bar - Milk Chocolate': 'Chocolate',
    'Wonka Bar - Triple Dazzle Caramel': 'Chocolate',
    'Laffy Taffy': 'Sugar',
    'SweeTARTS': 'Sugar',
    'Nerds': 'Sugar',
    'Fun Dip': 'Sugar',
    'Fizzy Lifting Drinks': 'Other',
    'Everlasting Gobstopper': 'Sugar',
    'Hair Toffee': 'Sugar',
    'Lickable Wallpaper': 'Other',
    'Wonka Gum': 'Other',
    'Kazookles': 'Other'
}

STATE_COORDINATES = {
    'Alabama': (32.806671, -86.791130),
    'Alberta': (53.933271, -116.576504),
    'Arizona': (34.048928, -111.093731),
    'Arkansas': (34.969704, -92.373123),
    'British Columbia': (53.726668, -127.647621),
    'California': (36.116203, -119.681564),
    'Colorado': (39.059811, -105.311104),
    'Connecticut': (41.597782, -72.755371),
    'Delaware': (39.318523, -75.507141),
    'District of Columbia': (38.897438, -77.026817),
    'Florida': (27.766279, -81.686783),
    'Georgia': (33.040619, -83.643074),
    'Idaho': (44.240459, -114.478828),
    'Illinois': (40.349457, -88.986137),
    'Indiana': (39.849426, -86.258278),
    'Iowa': (42.011539, -93.210526),
    'Kansas': (38.526600, -96.726486),
    'Kentucky': (37.668140, -84.670067),
    'Louisiana': (31.169546, -91.867805),
    'Maine': (44.693947, -69.381927),
    'Manitoba': (53.760861, -98.813876),
    'Maryland': (39.063946, -76.802101),
    'Massachusetts': (42.230171, -71.530106),
    'Michigan': (43.326618, -84.536095),
    'Minnesota': (45.694454, -93.900192),
    'Mississippi': (32.741646, -89.678696),
    'Missouri': (38.456085, -92.288368),
    'Montana': (46.921925, -110.454353),
    'Nebraska': (41.125370, -98.268082),
    'Nevada': (38.313515, -117.055374),
    'New Brunswick': (46.565316, -66.461916),
    'New Hampshire': (43.452492, -71.563896),
    'New Jersey': (40.298904, -74.521011),
    'New Mexico': (34.840515, -106.248482),
    'New York': (42.165726, -74.948051),
    'Newfoundland and Labrador': (53.135509, -57.660436),
    'North Carolina': (35.630066, -79.806419),
    'North Dakota': (47.528912, -99.784012),
    'Nova Scotia': (44.681986, -63.744311),
    'Ohio': (40.388783, -82.764915),
    'Oklahoma': (35.565342, -96.928917),
    'Ontario': (51.253775, -85.323214),
    'Oregon': (44.572021, -122.070938),
    'Pennsylvania': (40.590752, -77.209755),
    'Prince Edward Island': (46.510712, -63.416814),
    'Quebec': (52.939916, -73.549136),
    'Rhode Island': (41.680893, -71.511780),
    'Saskatchewan': (52.939916, -106.450864),
    'South Carolina': (33.856892, -80.945007),
    'South Dakota': (44.299782, -99.438828),
    'Tennessee': (35.747845, -86.692345),
    'Texas': (31.054487, -97.563461),
    'Utah': (40.150032, -111.862434),
    'Vermont': (44.045876, -72.710686),
    'Virginia': (37.769337, -78.169968),
    'Washington': (47.400902, -121.490494),
    'West Virginia': (38.491226, -80.954453),
    'Wisconsin': (44.268543, -89.616508),
    'Wyoming': (42.755966, -107.302490)
}

CITY_COORDINATES = {
    'New York City': (40.7128, -74.0060),
    'Los Angeles': (34.0522, -118.2437),
    'Philadelphia': (39.9526, -75.1652),
    'San Francisco': (37.7749, -122.4194),
    'Seattle': (47.6062, -122.3321),
    'Houston': (29.7604, -95.3698),
    'Chicago': (41.8781, -87.6298),
    'Columbus': (39.9612, -82.9988),
    'San Diego': (32.7157, -117.1611),
    'Springfield': (37.2089, -93.2923),
    'Dallas': (32.7767, -96.7970),
    'Jacksonville': (30.3322, -81.6557),
    'Detroit': (42.3314, -83.0458),
    'Newark': (40.7357, -74.1724),
    'Richmond': (37.5407, -77.4360),
    'Denver': (39.7392, -104.9903),
    'Austin': (30.2672, -97.7431),
    'San Antonio': (29.4241, -98.4936),
    'Miami': (25.7617, -80.1918),
    'Atlanta': (33.7490, -84.3880),
    'Phoenix': (33.4484, -112.0740),
    'Las Vegas': (36.1699, -115.1398),
    'Memphis': (35.1495, -90.0490),
    'Nashville': (36.1627, -86.7816),
    'Toronto': (43.6532, -79.3832),
    'Montreal': (45.5017, -73.5673),
    'Vancouver': (49.2827, -123.1207),
    'Calgary': (51.0447, -114.0719),
    'Halifax': (44.6488, -63.5752)
}

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees) in kilometers.
    """
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_customer_coords(city, state):
    """Return (lat, lon) for customer city/state."""
    if city in CITY_COORDINATES:
        return CITY_COORDINATES[city]
    if state in STATE_COORDINATES:
        return STATE_COORDINATES[state]
    return (39.8283, -98.5795)  # Geographic center of contiguous US fallback

def get_factory_coords(factory_name):
    """Return (lat, lon) for factory."""
    if factory_name in FACTORIES:
        return (FACTORIES[factory_name]['lat'], FACTORIES[factory_name]['lon'])
    return (39.8283, -98.5795)
