import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

import random
random.seed(42)

model_file = "model.pkl"
d = pd.read_csv("./DataSet/accidents_Berlin_2021.csv")
d.drop(columns=["ObjectID","State", "AccidentYear", "InvolvingBike","InvolvingCar","InvolvingPedestrian","InvolvingMotorcycle","InvolvingHGV", "InvolvingOther","LOR_ab_2021", "GraphicCoord1","GraphicCoord2",  "LongitudeWGS84",  "LatitudeWGS84"], inplace=True)
dt = d.groupby(["District", "AccidentHour", "DayOfWeek", "LightingCondition", "RoadCondition"]).size().reset_index(name="Count")
X,y = dt.drop(columns=["Count"]), dt["Count"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestRegressor(max_depth= 15, max_features= 'sqrt', min_samples_leaf=2, min_samples_split= 2, n_estimators= 500)
model.fit(X_train, y_train)
with open(model_file, 'wb') as file:
    pickle.dump(model, file)