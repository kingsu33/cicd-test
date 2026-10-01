from flask import Flask, request, jsonify, send_file
from io import BytesIO

app = Flask(__name__)

latest_frame = None


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CI/CD Test</title>
    </head>
    <body>
        <h1 id="message">Hello! Flask running on Docker.</h1>

        <button onclick="changeMessage()">Click me!</button>

        <script>
            function changeMessage() {
                document.getElementById("message").innerText =
                    "Button clicked! CI/CD is working!";
            }
        </script>
    </body>
    </html>
    """

@app.route("/iot/sub", methods=["POST"])
def sub():

    data = request.get_json()

    print("IoT telemetry recieved:")
    print(data)

    return jsonify({
        "status": "received",
        "data": data
    })


@app.route("/test")
def test():
    return "Hello! Flask running on Docker."


@app.route("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/frame")
def receive_frame():
    global latest_frame

    if request.content_type != "image/jpeg":
        return jsonify({
            "error": "Content-Type must be image/jpeg"
        }), 415

    jpeg_bytes = request.get_data()

    if not jpeg_bytes:
        return jsonify({
            "error": "Empty frame"
        }), 400

    latest_frame = jpeg_bytes

    print(
        f"Received JPEG frame: {len(jpeg_bytes)} bytes",
        flush=True
    )

    return jsonify({
        "status": "ok",
        "received_bytes": len(jpeg_bytes)
    })


@app.get("/frame")
def show_frame():

    if latest_frame is None:
        return jsonify({
            "error": "No frame received yet"
        }), 404

    return send_file(
        BytesIO(latest_frame),
        mimetype="image/jpeg"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)