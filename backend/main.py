from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import osmnx as ox

from load_map import load_graph_dynamic

from algorithms import (
    bfs,
    dfs,
    dijkstra,
    astar,
    haversine_meters_coords
)


# ==========================================
# CREATE FASTAPI APP
# ==========================================

app = FastAPI()


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Map Pathfinding Visualizer"
    }


# ==========================================
# SOLVE
# ==========================================

@app.post("/solve")
def solve(data: dict):

    try:

        print("\n==============================")
        print("SOLVE REQUEST RECEIVED")
        print("==============================")

        # ----------------------------------
        # 1. GET DATA FROM FRONTEND
        # ----------------------------------

        start = data.get("start")
        end = data.get("end")
        algo = data.get("algo", "dijkstra").lower()

        print("Start:", start)
        print("End:", end)
        print("Algorithm:", algo)


        if not start or not end:

            raise HTTPException(
                status_code=400,
                detail="Start and end points are required"
            )


        # ----------------------------------
        # 2. LOAD ROAD GRAPH
        # ----------------------------------

        print("STEP 1: Loading road graph...")

        G = load_graph_dynamic(
            start,
            end
        )

        print("STEP 2: Road graph loaded!")

        print(
            "Number of nodes:",
            len(G.nodes)
        )

        print(
            "Number of edges:",
            len(G.edges)
        )


        # ----------------------------------
        # 3. STORE NODE COORDINATES
        # ----------------------------------

        print("STEP 3: Creating node coordinates...")

        nodes = {
            n: (d["y"], d["x"])
            for n, d in G.nodes(data=True)
        }


        # ----------------------------------
        # 4. CREATE ADJACENCY LIST
        # ----------------------------------

        print("STEP 4: Creating adjacency list...")

        adj = {}


        for u, v, key, data_edge in G.edges(
            keys=True,
            data=True
        ):

            length = data_edge.get("length")


            # If edge doesn't have length
            if length is None:

                length = haversine_meters_coords(
                    nodes[u],
                    nodes[v]
                )


            # u -> v
            adj.setdefault(
                u,
                []
            ).append(
                (v, length)
            )


            # v -> u
            adj.setdefault(
                v,
                []
            ).append(
                (u, length)
            )


        print("STEP 5: Adjacency list created!")


        # ----------------------------------
        # 5. FIND NEAREST START NODE
        # ----------------------------------

        print("STEP 6: Finding nearest start node...")

        start_node = ox.distance.nearest_nodes(
            G,
            start[1],
            start[0]
        )


        print(
            "Start node:",
            start_node
        )


        # ----------------------------------
        # 6. FIND NEAREST END NODE
        # ----------------------------------

        print("STEP 7: Finding nearest end node...")

        end_node = ox.distance.nearest_nodes(
            G,
            end[1],
            end[0]
        )


        print(
            "End node:",
            end_node
        )


        # ----------------------------------
        # 7. RUN ALGORITHM
        # ----------------------------------

        print(
            "STEP 8: Running",
            algo.upper()
        )


        # ==================================
        # BFS
        # ==================================

        if algo == "bfs":

            path_nodes, visited_nodes = bfs(
                adj,
                start_node,
                end_node
            )


            dist = 0.0


            for i in range(
                len(path_nodes) - 1
            ):

                u = path_nodes[i]
                v = path_nodes[i + 1]


                weight = next(
                    (
                        w
                        for neighbor, w
                        in adj.get(u, [])
                        if neighbor == v
                    ),
                    None
                )


                if weight is None:

                    weight = haversine_meters_coords(
                        nodes[u],
                        nodes[v]
                    )


                dist += weight


        # ==================================
        # DFS
        # ==================================

        elif algo == "dfs":

            path_nodes, visited_nodes = dfs(
                adj,
                start_node,
                end_node
            )


            dist = 0.0


            for i in range(
                len(path_nodes) - 1
            ):

                u = path_nodes[i]
                v = path_nodes[i + 1]


                weight = next(
                    (
                        w
                        for neighbor, w
                        in adj.get(u, [])
                        if neighbor == v
                    ),
                    None
                )


                if weight is None:

                    weight = haversine_meters_coords(
                        nodes[u],
                        nodes[v]
                    )


                dist += weight


        # ==================================
        # DIJKSTRA
        # ==================================

        elif algo == "dijkstra":

            (
                path_nodes,
                visited_nodes,
                dist
            ) = dijkstra(
                adj,
                start_node,
                end_node
            )


        # ==================================
        # A*
        # ==================================

        elif algo == "astar":

            (
                path_nodes,
                visited_nodes,
                dist
            ) = astar(
                adj,
                nodes,
                start_node,
                end_node
            )


        # ==================================
        # INVALID ALGORITHM
        # ==================================

        else:

            raise HTTPException(
                status_code=400,
                detail="Invalid algorithm"
            )


        print(
            "STEP 9: Algorithm completed!"
        )

        print(
            "Path nodes:",
            len(path_nodes)
        )

        print(
            "Visited nodes:",
            len(visited_nodes)
        )

        print(
            "Distance:",
            dist,
            "meters"
        )


        # ----------------------------------
        # 8. CONVERT NODES TO COORDINATES
        # ----------------------------------

        print(
            "STEP 10: Converting nodes to coordinates..."
        )


        visited_coords = [
            nodes[n]
            for n in visited_nodes
            if n in nodes
        ]


        path_coords = [
            nodes[n]
            for n in path_nodes
            if n in nodes
        ]


        print(
            "Visited coordinates:",
            len(visited_coords)
        )

        print(
            "Path coordinates:",
            len(path_coords)
        )


        # ----------------------------------
        # 9. RETURN DATA TO FRONTEND
        # ----------------------------------

        result = {

            "visited": visited_coords,

            "path": path_coords,

            "distance_km": round(
                dist / 1000.0,
                3
            ),

            "visited_count": len(
                visited_coords
            )
        }


        print(
            "STEP 11: Sending result to frontend"
        )

        print(
            "=============================="
        )


        return result


    # ======================================
    # ERROR HANDLING
    # ======================================

    except HTTPException:

        raise


    except Exception as e:

        print(
            "\n!!!!!!!!!!!! ERROR !!!!!!!!!!!!"
        )

        print(
            repr(e)
        )

        print(
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        )


        raise HTTPException(
            status_code=500,
            detail=str(e)
        )