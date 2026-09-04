from flask import Flask

app = Flask(__name__)


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


@app.route("/test")
def test():
    return "Hello! Flask running on Docker."


@app.route("/health")
def health():
    return {
        "status": "ok"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)