import osmnx as ox
from math import radians, sin, cos, sqrt, asin
import time


# ==========================================
# OSMNX SETTINGS
# ==========================================

ox.settings.requests_timeout = 300
ox.settings.overpass_rate_limit = True
ox.settings.use_cache = True


# ==========================================
# OVERPASS SERVERS
# ==========================================

OVERPASS_SERVERS = [
    "https://overpass-api.de/api",
    "https://overpass.private.coffee/api"
]


# ==========================================
# HAVERSINE DISTANCE
# ==========================================

def haversine_meters(lat1, lon1, lat2, lon2):

    R = 6371000.0

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2.0) ** 2
        +
        cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2.0) ** 2
    )

    c = 2 * asin(sqrt(a))

    return R * c


# ==========================================
# LOAD ROAD GRAPH
# ==========================================

def load_graph_dynamic(start, end):

    lat1, lon1 = start
    lat2, lon2 = end

    # --------------------------------------
    # Distance between start and end
    # --------------------------------------

    dist = haversine_meters(
        lat1,
        lon1,
        lat2,
        lon2
    )

    # --------------------------------------
    # Dynamic radius
    # --------------------------------------

    radius = max(
        800,
        min(
            int(dist * 1.5),
            3000
        )
    )

    # --------------------------------------
    # Midpoint
    # --------------------------------------

    mid_lat = (lat1 + lat2) / 2
    mid_lon = (lon1 + lon2) / 2

    print("=" * 60)
    print("LOADING ROAD GRAPH")
    print("=" * 60)

    print("Start:", start)
    print("End:", end)
    print("Distance:", dist, "meters")
    print("Center:", mid_lat, mid_lon)
    print("Radius:", radius, "meters")

    # --------------------------------------
    # Try Overpass servers
    # --------------------------------------

    last_error = None

    for server in OVERPASS_SERVERS:

        try:

            print()
            print("Trying Overpass server:")
            print(server)

            # Set current Overpass server
            ox.settings.overpass_url = server

            # Download road network
            G = ox.graph_from_point(
                (
                    mid_lat,
                    mid_lon
                ),
                dist=radius,
                network_type="drive"
            )

            print()
            print("SUCCESS!")
            print("Road network downloaded.")
            print("Server used:", server)
            print("Nodes:", len(G.nodes))
            print("Edges:", len(G.edges))

            return G

        except Exception as error:

            last_error = error

            print()
            print("Overpass server failed:")
            print(server)

            print("Error:")
            print(error)

            print("Trying next server...")

            # Small delay before next server
            time.sleep(3)

    # --------------------------------------
    # All servers failed
    # --------------------------------------

    print()
    print("=" * 60)
    print("ALL OVERPASS SERVERS FAILED")
    print("=" * 60)

    # IMPORTANT:
    # last_error, NOT last_errors
    raise RuntimeError(
        f"Unable to download road network. "
        f"Last Overpass error: {last_error}"
    )