from fastapi import (
    FastAPI,
    HTTPException
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

import osmnx as ox


from load_map import (
    load_graph_dynamic
)


from algorithms import (
    bfs,
    dfs,
    dijkstra,
    astar,
    haversine_meters_coords
)


app = FastAPI()


# ========================================
# CORS
# ========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_methods=["*"],

    allow_headers=["*"],
)


# ========================================
# HOME
# ========================================

@app.get("/")
def home():

    return {
        "message":
        "Map Pathfinding Visualizer"
    }


# ========================================
# SOLVE
# ========================================

@app.post("/solve")
def solve(
    data: dict
):

    try:

        print(
            "\n========================"
        )

        print(
            "SOLVE REQUEST RECEIVED"
        )

        print(
            "========================"
        )


        start = data.get(
            "start"
        )

        end = data.get(
            "end"
        )

        algo = data.get(
            "algo",
            "dijkstra"
        ).lower()


        print(
            "Start:",
            start
        )

        print(
            "End:",
            end
        )

        print(
            "Algorithm:",
            algo
        )


        if not start or not end:

            raise HTTPException(
                status_code=400,
                detail=
                "start and end required"
            )


        # ==================================
        # STEP 1
        # LOAD GRAPH
        # ==================================

        print(
            "STEP 1: Loading road graph..."
        )


        G = load_graph_dynamic(
            start,
            end
        )


        print(
            "STEP 2: Road graph loaded!"
        )


        # ==================================
        # STEP 3
        # NODE COORDINATES
        # ==================================

        print(
            "STEP 3: Creating node coordinates..."
        )


        nodes = {

            n: (
                d["y"],
                d["x"]
            )

            for n, d
            in G.nodes(
                data=True
            )
        }


        # ==================================
        # STEP 4
        # ADJACENCY LIST
        # ==================================

        print(
            "STEP 4: Creating adjacency list..."
        )


        adj = {}


        for (
            u,
            v,
            key,
            data_edge
        ) in G.edges(
            keys=True,
            data=True
        ):


            length = data_edge.get(
                "length"
            )


            if length is None:

                a = nodes[u]

                b = nodes[v]


                length = (
                    haversine_meters_coords(
                        a,
                        b
                    )
                )


            adj.setdefault(
                u,
                []
            ).append(
                (
                    v,
                    length
                )
            )


            adj.setdefault(
                v,
                []
            ).append(
                (
                    u,
                    length
                )
            )


        print(
            "STEP 5: Adjacency list created!"
        )


        # ==================================
        # STEP 6
        # START NODE
        # ==================================

        print(
            "STEP 6: Finding nearest start node..."
        )


        start_node = (
            ox.distance.nearest_nodes(
                G,
                start[1],
                start[0]
            )
        )


        print(
            "Start node:",
            start_node
        )


        # ==================================
        # STEP 7
        # END NODE
        # ==================================

        print(
            "STEP 7: Finding nearest end node..."
        )


        end_node = (
            ox.distance.nearest_nodes(
                G,
                end[1],
                end[0]
            )
        )


        print(
            "End node:",
            end_node
        )


        # ==================================
        # STEP 8
        # RUN ALGORITHM
        # ==================================

        print(
            "STEP 8: Running",
            algo.upper()
        )


        if algo == "bfs":

            path_nodes, visited_nodes = bfs(
                adj,
                start_node,
                end_node
            )


            distance = 0.0


            for i in range(
                len(path_nodes) - 1
            ):

                u = path_nodes[i]

                v = path_nodes[i + 1]


                weight = next(
                    (
                        w
                        for nv, w
                        in adj.get(
                            u,
                            []
                        )
                        if nv == v
                    ),
                    None
                )


                if weight is None:

                    weight = (
                        haversine_meters_coords(
                            nodes[u],
                            nodes[v]
                        )
                    )


                distance += weight


        elif algo == "dfs":

            path_nodes, visited_nodes = dfs(
                adj,
                start_node,
                end_node
            )


            distance = 0.0


            for i in range(
                len(path_nodes) - 1
            ):

                u = path_nodes[i]

                v = path_nodes[i + 1]


                weight = next(
                    (
                        w
                        for nv, w
                        in adj.get(
                            u,
                            []
                        )
                        if nv == v
                    ),
                    None
                )


                if weight is None:

                    weight = (
                        haversine_meters_coords(
                            nodes[u],
                            nodes[v]
                        )
                    )


                distance += weight


        elif algo == "astar":

            (
                path_nodes,
                visited_nodes,
                distance
            ) = astar(
                adj,
                nodes,
                start_node,
                end_node
            )


        elif algo == "dijkstra":

            (
                path_nodes,
                visited_nodes,
                distance
            ) = dijkstra(
                adj,
                start_node,
                end_node
            )


        else:

            raise HTTPException(
                status_code=400,
                detail=
                "Invalid algorithm"
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
            distance,
            "meters"
        )


        # ==================================
        # STEP 10
        # CONVERT TO COORDINATES
        # ==================================

        print(
            "STEP 10: Converting result to coordinates..."
        )


        visited_coords = [

            nodes[n]

            for n
            in visited_nodes

            if n in nodes

        ]


        path_coords = [

            nodes[n]

            for n
            in path_nodes

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


        # ==================================
        # STEP 11
        # RESPONSE
        # ==================================

        print(
            "STEP 11: Sending result to frontend"
        )


        return {

            "visited":
                visited_coords,

            "path":
                path_coords,

            "distance_km":
                round(
                    distance / 1000.0,
                    3
                ),

            "visited_count":
                len(visited_coords)

        }


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
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        )


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )