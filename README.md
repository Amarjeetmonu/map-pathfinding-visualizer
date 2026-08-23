🗺️ Map Pathfinding Visualizer

A real-world map-based pathfinding visualizer that demonstrates classical graph traversal and shortest-path algorithms on actual road networks using OpenStreetMap data.

This project visually compares how different algorithms explore nodes and find routes between two points on a map.

🎥 Project Demo (Actual Working Video)

https://drive.google.com/file/d/1bsUPzlLIV6Sqxvzx9OBASlhFuln9-a7f/view?usp=drive_link


✨ Features
#🧠 Algorithms implemented:

1. Dijkstra
2. A*
3. BFS
4. DFS

1. 🗺️ Uses real road networks (OpenStreetMap via OSMnx)

2. 🎞️ Animated traversal of visited nodes

3. 📏 Displays total path distance (km)

4. 🖱️ Click-based start & end point selection

5. ⚡ Optimized animation speed (not snap, not slow)


🏗️ Tech Stack

Backend

1. Python
2. FastAPI
3. OSMnx
4. NetworkX (via OSMnx)

Frontend

1. HTML
2. JavaScript
3. Leaflet.js
4. OpenStreetMap tiles

📁 Project Structure

map-pathfinding-visualizer/
│
├── backend/
│   ├── main.py
│   ├── algorithms.py
│   ├── load_map.py
│   ├── requirements.txt
│
├── frontend/
│   └── index.html
│
├── assets/
│   └── demo.mp4
│
├── README.md
└── .gitignore



🚀 How to Run This Project Locally (Step-by-Step)

1️⃣ Clone the Repository

git clone https://github.com/Amarjeetmonu/map-pathfinding-visualizer.git
cd map-pathfinding-visualizer

2️⃣ Create Virtual Environment (Backend)

cd backend
python -m venv venv

Activate it:

Windows (PowerShell)

venv\Scripts\activate

Linux / macOS

source venv/bin/activate

3️⃣ Install Backend Dependencies

pip install -r requirements.txt

⚠️ First-time OSMnx install may take some time — this is normal.

4️⃣ Start the Backend Server

uvicorn main:app --reload

You should see:

Uvicorn running on http://127.0.0.1:8000
✅ Backend is now live.

5️⃣ Run the Frontend
Option A (Recommended – simplest)
step-1. Go to frontend/
step-2. Double-click index.html
step-3. It will open in your browser

Option B (Using Live Server / HTTP server)
  cd frontend
  python -m http.server 5500

Then open:

   http://localhost:5500

🧪 How to Use

1. Click on the map → Start point
2. Click again → End point
3. Choose algorithm from dropdown
4. Click Solve
5. Watch traversal animation + final path
6. Distance shown at top


🧠 Learning Outcomes

Real-world graph modeling

Algorithm behavior comparison

Spatial data handling

Backend–frontend integration

Visualization + animation logic


👨‍💻 Author

Amarjeet Kumar Computer Science & Engineering

📌 Focus: DSA, Algorithms, System Thinking

