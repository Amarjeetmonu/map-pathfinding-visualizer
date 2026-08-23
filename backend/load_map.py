import osmnx as ox
ox.settings.overpass_url = "https://overpass-api.de/api"
from math import radians, sin, cos, sqrt, asin


# ==========================================
# OVERPASS SETTINGS
# ==========================================

ox.settings.requests_timeout = 300

ox.settings.overpass_rate_limit = True

# ==========================================
# HAVERSINE DISTANCE
# ==========================================

def haversine_meters(
    lat1,
    lon1,
    lat2,
    lon2
):

    R = 6371000.0

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2.0) ** 2
        +
        cos(radians(lat1))
        *
        cos(radians(lat2))
        *
        sin(dlon / 2.0) ** 2
    )

    c = 2 * asin(sqrt(a))

    return R * c


# ==========================================
# LOAD ROAD GRAPH
# ==========================================

def load_graph_dynamic(start, end):

    lat1, lon1 = start
    lat2, lon2 = end


    # Distance between Start and End
    dist = haversine_meters(
        lat1,
        lon1,
        lat2,
        lon2
    )


    # Keep graph reasonably small
    radius = max(
        800,
        min(
            int(dist * 1.5),
            3000
        )
    )


    # Midpoint between Start and End
    mid_lat = (
        lat1 + lat2
    ) / 2

    mid_lon = (
        lon1 + lon2
    ) / 2


    print(
        "Downloading road network..."
    )

    print(
        "Center:",
        mid_lat,
        mid_lon
    )

    print(
        "Radius:",
        radius,
        "meters"
    )


    # Download driving road network
    G = ox.graph_from_point(
        (
            mid_lat,
            mid_lon
        ),
        dist=radius,
        network_type="drive"
    )


    print(
        "Road network downloaded!"
    )


    return G