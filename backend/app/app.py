from flask import Flask, send_from_directory, request

app = Flask(__name__, static_folder='../../frontend2/build', static_url_path='')


@app.route('/api/test')
def test():
    name = request.args.get('name', None)  # Get 'name' from query string, default to None if not provided
    if name:
        return f"Hello, {name}!"
    else:
        return "Hello, World!"


@app.route('/api/<path:path>')
def api(path: str):
    return {"message": f"fetching for {path}..."}


@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    app.run(debug=True)
