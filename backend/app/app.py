from flask import Flask, send_from_directory, request

app = Flask(__name__, static_folder='../../frontend/dist', static_url_path='')


@app.route('/api/<path:subpath>')
def api(subpath):
    # Your API handling logic here
    return {"message": "This is an API endpoint"}


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if request.path.startswith('/api/'):
        # Allow the routing for API to naturally return Not Found if no endpoint matches.
        pass
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    app.run(debug=True)
