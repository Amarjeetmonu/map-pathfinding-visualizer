// ===============================
// 1. CREATE MAP
// ===============================

let map = L.map("map").setView(
    [28.61, 77.20],
    13
);


L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
).addTo(map);


// ===============================
// 2. VARIABLES
// ===============================

let startMarker = null;
let endMarker = null;
let routeLine = null;

let visitedLayer =
    L.layerGroup().addTo(map);

let startLatLng = null;
let endLatLng = null;


// ===============================
// 3. SELECT START AND END
// ===============================

map.on("click", function (e) {

    // First click = START
    if (!startLatLng) {

        startLatLng = [
            e.latlng.lat,
            e.latlng.lng
        ];

        startMarker =
            L.marker(e.latlng)
                .addTo(map)
                .bindPopup("Start")
                .openPopup();

        return;
    }


    // Second click = END
    if (!endLatLng) {

        endLatLng = [
            e.latlng.lat,
            e.latlng.lng
        ];

        endMarker =
            L.marker(e.latlng)
                .addTo(map)
                .bindPopup("End")
                .openPopup();

        return;
    }

});


// ===============================
// 4. SOLVE BUTTON
// ===============================

const solveButton =
    document.getElementById("solveBtn");

solveButton.addEventListener(
    "click",
    solve
);


// ===============================
// 5. SOLVE
// ===============================

async function solve() {

    // Check start and end
    if (!startLatLng || !endLatLng) {

        alert(
            "Select start and end points"
        );

        return;
    }


    // Selected algorithm
    const algo =
        document.getElementById(
            "algo"
        ).value;


    const stats =
        document.getElementById(
            "stats"
        );


    // Clear previous visited nodes
    visitedLayer.clearLayers();


    // Remove previous route
    if (routeLine) {

        map.removeLayer(
            routeLine
        );

        routeLine = null;
    }


    stats.innerText =
        `Running ${algo.toUpperCase()}...`;


    try {

        // ===============================
        // SEND REQUEST
        // ===============================

        console.log(
            "Sending request..."
        );

        console.log(
            "Start:",
            startLatLng
        );

        console.log(
            "End:",
            endLatLng
        );

        console.log(
            "Algorithm:",
            algo
        );


        const response =
            await fetch(
                "http://127.0.0.1:8000/solve",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        start:
                            startLatLng,

                        end:
                            endLatLng,

                        algo:
                            algo

                    })
                }
            );


        // ===============================
        // HTTP STATUS
        // ===============================

        console.log(
            "HTTP status:",
            response.status
        );


        // ===============================
        // RECEIVE RESPONSE
        // ===============================

        const data =
            await response.json();


        console.log(
            "BACKEND DATA:",
            data
        );


        // ===============================
        // CHECK ERROR
        // ===============================

        if (!response.ok) {

            console.error(
                "BACKEND ERROR:",
                data
            );


            stats.innerText =
                "Backend error. Check Console.";

            return;
        }


        // ===============================
        // GET DATA
        // ===============================

        const visited =
            data.visited || [];


        const path =
            data.path || [];


        console.log(
            "Visited count:",
            visited.length
        );


        console.log(
            "Path count:",
            path.length
        );


        // ===============================
        // DRAW VISITED NODES
        // ===============================

        for (
            let i = 0;
            i < visited.length;
            i++
        ) {

            L.circleMarker(
                visited[i],
                {
                    radius: 4,

                    color: "orange",

                    fillColor: "orange",

                    fillOpacity: 0.8,

                    weight: 1
                }
            ).addTo(
                visitedLayer
            );
        }


        // ===============================
        // DRAW FINAL PATH
        // ===============================

        if (
            path.length > 0
        ) {

            routeLine =
                L.polyline(
                    path,
                    {
                        color:
                            "deepskyblue",

                        weight: 6,

                        opacity: 1
                    }
                ).addTo(map);


            // Automatically fit route
            // inside the map

            map.fitBounds(
                routeLine.getBounds(),
                {
                    padding: [
                        30,
                        30
                    ]
                }
            );
        }


        // ===============================
        // SHOW STATISTICS
        // ===============================

        stats.innerText =
            `Algorithm: ${algo.toUpperCase()} | ` +
            `Visited: ${data.visited_count} | ` +
            `Distance: ${data.distance_km} km`;


        console.log(
            "Visualization completed."
        );

    }


    catch (error) {

        console.error(
            "Solve error:",
            error
        );


        stats.innerText =
            "Something went wrong. Check Console.";

    }

}


// ===============================
// 6. RESET
// ===============================

function resetMap() {

    // Remove start marker
    if (startMarker) {

        map.removeLayer(
            startMarker
        );
    }


    // Remove end marker
    if (endMarker) {

        map.removeLayer(
            endMarker
        );
    }


    // Remove route
    if (routeLine) {

        map.removeLayer(
            routeLine
        );
    }


    // Remove visited nodes
    visitedLayer.clearLayers();


    // Reset variables
    startMarker = null;

    endMarker = null;

    routeLine = null;

    startLatLng = null;

    endLatLng = null;


    // Reset statistics
    document.getElementById(
        "stats"
    ).innerText =
        "Select start and end points";

}