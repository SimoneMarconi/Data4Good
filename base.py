#initial file to train the model
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

import random
random.seed(42)

d = pd.read_csv("./accidents_Berlin_2021.csv")
d.drop(columns=["ObjectID","State", "AccidentYear", "InvolvingBike","InvolvingCar","InvolvingPedestrian","InvolvingMotorcycle","InvolvingHGV", "InvolvingOther","LOR_ab_2021", "GraphicCoord1","GraphicCoord2",  "LongitudeWGS84",  "LatitudeWGS84"], inplace=True)
dt = d.groupby(["District", "AccidentHour", "DayOfWeek", "LightingCondition", "RoadCondition"]).size().reset_index(name="Count")
X,y = dt.drop(columns=["Count"]), dt["Count"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestRegressor(max_depth= 15, max_features= 'sqrt', min_samples_leaf=2, min_samples_split= 2, n_estimators= 500)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print("Mean Squared Error:", mse)
print("Average Error:", mse**0.5)

print("Predict the number of accidents in Berlin")
District = int(input("Enter district: ")) # 0-12
AccidentHour = int(input("Enter hour: ")) # 0-23
DayOfWeek = int(input("Enter day: ")) # 1-7
LightingCondition = int(input("Enter lighting condition: ")) # 0-2
RoadCondition = int(input("Enter road condition: ")) # 0-2

columns = ["District", "AccidentHour", "DayOfWeek", "LightingCondition", "RoadCondition"]
# Make prediction using the model
userdata = pd.DataFrame([[District, AccidentHour, DayOfWeek, LightingCondition, RoadCondition]], columns=columns)
prediction = model.predict(userdata)
print("Predicted number of accidents:", prediction[0])
print("Probability of the happening of the accident:", prediction[0]/54)