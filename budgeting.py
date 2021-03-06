''' Main module to run the Flask server. '''

from app import create_app

app = create_app()

# Run server
if __name__ == "__main__":
    app.run(port=8090)
