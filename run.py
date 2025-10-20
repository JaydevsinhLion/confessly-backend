from app import create_app

# Initialize Flask app
app = create_app()

# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
