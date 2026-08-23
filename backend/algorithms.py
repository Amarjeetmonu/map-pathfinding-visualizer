import heapq
import math
from collections import deque


def haversine_meters_coords(a, b):

    lat1, lon1 = a
    lat2, lon2 = b

    R = 6371000.0

    from math import radians, sin, cos, sqrt, asin

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    aa = (
        sin(dlat / 2.0) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2.0) ** 2
    )

    c = 2 * asin(sqrt(aa))

    return R * c


def reconstruct_path(parent, start, end):

    if end == start:
        return [start]

    if end not in parent:
        return []

    path = []

    cur = end

    while cur is not None:

        path.append(cur)

        if cur == start:
            break

        cur = parent.get(cur)

    path.reverse()

    return path


# ---------------- BFS ----------------

def bfs(adj, start, end):

    q = deque([start])

    parent = {
        start: None
    }

    visited_set = {
        start
    }

    visited_order = []

    while q:

        u = q.popleft()

        visited_order.append(u)

        if u == end:
            break

        for v, _ in adj.get(u, []):

            if v not in visited_set:

                visited_set.add(v)

                parent[v] = u

                q.append(v)

    path = reconstruct_path(
        parent,
        start,
        end
    )

    return path, visited_order


# ---------------- DFS ----------------

def dfs(adj, start, end):

    stack = [start]

    parent = {
        start: None
    }

    visited_set = {
        start
    }

    visited_order = []

    while stack:

        u = stack.pop()

        visited_order.append(u)

        if u == end:
            break

        for v, _ in adj.get(u, []):

            if v not in visited_set:

                visited_set.add(v)

                parent[v] = u

                stack.append(v)

    path = reconstruct_path(
        parent,
        start,
        end
    )

    return path, visited_order


# ---------------- DIJKSTRA ----------------

def dijkstra(adj, start, end):

    pq = [(0, start)]

    distance = {
        start: 0
    }

    parent = {
        start: None
    }

    visited_set = set()

    visited_order = []

    while pq:

        dist_u, u = heapq.heappop(pq)

        if u in visited_set:
            continue

        visited_set.add(u)

        visited_order.append(u)

        if u == end:
            break

        for v, weight in adj.get(u, []):

            new_dist = dist_u + weight

            if new_dist < distance.get(v, float("inf")):

                distance[v] = new_dist

                parent[v] = u

                heapq.heappush(
                    pq,
                    (new_dist, v)
                )

    path = reconstruct_path(
        parent,
        start,
        end
    )

    total_distance = distance.get(
        end,
        float("inf")
    )

    return path, visited_order, total_distance


# ---------------- A* ----------------

def astar(adj, nodes, start, end):

    pq = [(0, 0, start)]

    g_score = {
        start: 0
    }

    parent = {
        start: None
    }

    visited_set = set()

    visited_order = []

    def heuristic(u, v):

        return haversine_meters_coords(
            nodes[u],
            nodes[v]
        )

    while pq:

        f_score, current_g, u = heapq.heappop(pq)

        if u in visited_set:
            continue

        visited_set.add(u)

        visited_order.append(u)

        if u == end:
            break

        for v, weight in adj.get(u, []):

            new_g = current_g + weight

            if new_g < g_score.get(
                v,
                float("inf")
            ):

                g_score[v] = new_g

                parent[v] = u

                h = heuristic(v, end)

                f = new_g + h

                heapq.heappush(
                    pq,
                    (f, new_g, v)
                )

    path = reconstruct_path(
        parent,
        start,
        end
    )

    total_distance = g_score.get(
        end,
        float("inf")
    )

    return path, visited_order, total_distance