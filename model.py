import pickle
import pandas as pd

model_file = "./model.pkl"
with open(model_file, 'rb') as file:
    model = pickle.load(file)

def convert(d):
    conv = {
        1 : "Mitte",
        2 : "Friedrichshain-Kreuzberg",
        3 : "Pankow",
        4 : "Charlottenburg-Wilm.",
        5 : "Spandau",
        6 : "Steglitz - Zehlendorf",
        7 : "Tempelhof - Schöneberg",
        8 : "Neukölln",
        9 : "Treptow - Köpenick",
        10 : "Marzahn - Hellersdorf",
        11 : "Lichtenberg",
        12 : "Reinickendorf"
    }
    return conv[d]
    
def get(data):
    district = data["district"]
    hour = data["hour"]
    day = data["day"]
    light = data["light"]
    condition = data["condition"]
    columns = ["District", "AccidentHour", "DayOfWeek", "LightingCondition", "RoadCondition"]
    userdata = pd.DataFrame([[district, hour, day, light, condition]], columns=columns)
    predictions = model.predict(userdata)[0]
    return str(predictions)

def get_percentage(data):
    dict = {}
    hour = data["hour"]
    day = data["day"]
    light = data["light"]
    condition = data["condition"]
    columns = ["District", "AccidentHour", "DayOfWeek", "LightingCondition", "RoadCondition"]
    for district in range(1, 13):
        userdata = pd.DataFrame([[district, hour, day, light, condition]], columns=columns)
        prediction = model.predict(userdata)[0]
        dict[convert(district)] = prediction/52
    print(dict)
    return dict

def get_day(data):
    list = []
    district = data["district"]
    day = data["day"]
    light = data["light"]
    condition = data["condition"]
    columns = ["District", "AccidentHour", "DayOfWeek", "LightingCondition", "RoadCondition"]
    for hour in range(24):
        userdata = pd.DataFrame([[district, hour, day, light, condition]], columns=columns)
        prediction = model.predict(userdata)[0]/52
        list.append(prediction)
    return list
        
# mock = {
#     "district": 6,
#     "day" : 3,
#     "light" : 1,
#     "condition" : 1
# }

# print(get_day(mock))