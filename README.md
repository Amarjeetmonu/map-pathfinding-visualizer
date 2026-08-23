🗺️ Map Pathfinding Visualizer

A real-world map-based pathfinding visualizer that demonstrates classical graph traversal and shortest-path algorithms on actual road networks using OpenStreetMap data.

This project visually compares how different algorithms explore nodes and find routes between two points on a map.

✨ Features 🧠 Algorithms implemented:

Dijkstra A* BFS DFS 🗺️ Uses real road networks (OpenStreetMap via OSMnx)

🎞️ Animated traversal of visited nodes

📏 Displays total path distance (km)

🖱️ Click-based start & end point selection

⚡ Optimized animation speed (not snap, not slow)

🏗️ Tech Stack Backend

Python FastAPI OSMnx NetworkX (via OSMnx) Frontend

HTML JavaScript Leaflet.js OpenStreetMap tiles 📁 Project Structure map-pathfinding-visualizer/ │ ├── backend/ │ ├── main.py │ ├── algorithms.py │ ├── load_map.py │ ├── requirements.txt │ ├── frontend/ │ └── index.html │ ├── assets/ │ └── demo.mp4 │ ├── README.md └── .gitignore

🧪 How to Use

Click on the map → Start point
Click again → End point
Choose algorithm from dropdown
Click Solve
Watch traversal animation + final path
Distance shown at top
🧠 Learning Outcomes

Real-world graph modeling

Algorithm behavior comparison

Spatial data handling

Backend–frontend integration

Visualization + animation logic

👨‍💻 Author

AMARJEET KUMAR Computer Science & Engineering

📌 Focus: DSA, Algorithms, System Thinking
