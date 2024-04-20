from flask import Flask, request, abort, send_file
import model
import map
app = Flask(__name__)

@app.route("/probability", methods=["POST"])
def probability():
    query = request.args.to_dict(flat=False)
    print(query)
    data = request.json
    if validate_probability(data):
        prediction = model.get(data)
        if query["mode"][0] == "percentage":
            return str(float(prediction)/52)
        elif query["mode"][0] == "number":
            return prediction
        else:
            abort(400)
    else:
        abort(422)

@app.route("/image", methods=["POST"])
def image():
    data = request.json
    if validate_image(data):
        map.create_map(data)
        filename = "./Map.jpg"
        return send_file(filename, mimetype="image/gif")
    else:
        abort(422)

def validate_probability(data):
    if data["district"] < 1 or data["district"] > 12:
        return None
    if data["hour"] < 0 or data["hour"] > 23:
        return None
    if data["day"] < 1 or data["day"] > 7:
        return None
    if data["light"] < 0 or data["light"] > 2:
        return None
    if data["condition"] < 0 or data["condition"] > 2:
        return None
    return "ok"


def validate_image(data):
    if data["hour"] < 0 or data["hour"] > 23:
        return None
    if data["day"] < 1 or data["day"] > 7:
        return None
    if data["light"] < 0 or data["light"] > 2:
        return None
    if data["condition"] < 0 or data["condition"] > 2:
        return None
    return "ok"