from flask import Flask, request, abort, send_file, Response
import Model.model as model
import Model.map as map
import Model.graph as graph
app = Flask(__name__)

@app.route("/probability", methods=["POST"])
def probability():
    query = request.args.to_dict(flat=False)
    print(query)
    data = request.json
    if validate_probability(data) == "ok":
        prediction = model.get(data)
        if query["mode"][0] == "percentage":
            return str(float(prediction)/52)
        elif query["mode"][0] == "number":
            return prediction
    else:
        return Response("Wrong request format", status=422)

@app.route("/image", methods=["POST"])
def image():
    data = request.json
    if validate_image(data):
        map.create_map(data)
        return send_file("./Images/Map.jpg", mimetype="image/gif")
    else:
        return Response("Wrong request format", status=422)

@app.route("/day", methods=["POST"])
def day():
    data = request.json
    if validate_day(data):
        day = model.get_day(data)
        graph.draw(day)
        return send_file("./Images/Graph.jpg", mimetype="image/gif")
    else:
        return Response("Wrong request format", status=422)

def validate_probability(data):
    if data["district"] and data["hour"] and data["light"] and data["condition"] == False:
        return Response("Missing parameters", status=400)
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

def validate_day(data):
    if data["district"] < 1 or data["district"] > 12:
        return None
    if data["day"] < 1 or data["day"] > 7:
        return None
    if data["light"] < 0 or data["light"] > 2:
        return None
    if data["condition"] < 0 or data["condition"] > 2:
        return None
    return "ok"