<!DOCTYPE html>
<html>
<head>
    <title>Genealogy Map</title>
    <style>
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;        /* Full viewport height */
            font-family: 'Segoe UI', Arial, sans-serif;
            background-color: #f4f6f8;
            color: #333;
            overflow: hidden;    /* No page scrolling */
        }
        body {
            display: flex;
            flex-direction: column; /* Stack vertically */
            height: 100vh;          /* Exact viewport height */
        }
        #title {
            text-align: center;
            margin: 10px 0;
            font-size: 24px;
            font-weight: 600;
            color: #2c3e50;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
            flex: 0 0 auto;         /* Fixed height */
        }
        #map {
            width: 100%;
            height: calc(100vh - 60px - 40px); /* 100vh minus title and buttons */
            border: 1px solid #ddd;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            flex: 0 0 auto;         /* Fixed height, no grow */
        }
        #button-container {
            text-align: center;
            padding: 10px 0;
            background-color: #ffffff;
            border-top: 1px solid #ddd;
            box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.05);
            flex: 0 0 auto;         /* Fixed height */
            width: 100%;
            z-index: 1000;
        }
        button {
            margin: 0 15px;
            padding: 8px 20px;
            font-size: 14px;
            font-weight: 500;
            color: #fff;
            background-color: #3498db;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.1s ease;
        }
        button:hover {
            background-color: #2980b9;
            transform: translateY(-1px);
        }
        button:active {
            background-color: #1f6a9a;
            transform: translateY(0);
        }
    </style>
    {{ map_html|safe }}
</head>
<body>
    <h3 id="title">Newton & Stevens Migrations (1500-Present)</h3>
    <div id="map"></div>
    <div id="button-container">
        <button onclick="window.location.href='/newton'">Newton Data</button>
        <button onclick="window.location.href='/stevens'">Stevens Data</button>
    </div>
</body>
</html>
