from flask import Flask, jsonify, request

app = Flask(__name__)

a = [34, 12, 90, 44]

# ---------- GET ----------
@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(a)


# ---------- POST (add value) ----------
@app.route("/data", methods=["POST"])
def post_data():
    data = request.json          # user input
    value = data["value"]
    a.append(value)
    return jsonify(a)


# ---------- DELETE (remove by index) ----------
@app.route("/data", methods=["DELETE"])
def delete_data():
    data = request.json
    index = data["index"]
    a.pop(index)
    return jsonify(a)


# ---------- PATCH (update single index) ----------
@app.route("/data", methods=["PATCH"])
def patch_data():
    data = request.json
    index = data["index"]
    value = data["value"]
    a[index] = value
    return jsonify(a)


# ---------- PUT (replace full array) ----------
@app.route("/data", methods=["PUT"])
def put_data():
    data = request.json
    new_array = data["array"]
    global a
    a = new_array
    return jsonify(a)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
