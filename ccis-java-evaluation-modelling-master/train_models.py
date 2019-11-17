import pandas
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.externals import joblib
import matplotlib.pyplot as plt

# Set modeling specifications
metrics = ["NG","NPA","TNIN","TLLOC","TNLA","TNLS"]
code_property = 'size'
level = 'package'

# Read data
data = pandas.read_csv('data/' + code_property + '_' + level + '.csv')

# Normalize score 
maximum = max(data[["scores_ANN"]].values)[0]
minimim = min(data[["scores_ANN"]].values)[0]
data[["scores_ANN"]] = ((data[["scores_ANN"]] - minimim) / (maximum - minimim))

# Create model (Solver: lbgfs, sgd, adam Activation: identity, logistic, tanh, relu)
model = MLPRegressor(activation='logistic', solver='lbgfs')
model.fit(data[metrics], data["scores_ANN"])

# Predict based on model
pred = model.predict(data[metrics])

print('---')
print(min(pred))
print(max(pred))
print('---')
pred_normed = ((pred - min(pred)) / (max(pred) - min(pred)))
plt.hist(data[["scores_ANN"]].values, np.arange(0, 1, 0.01))
plt.hist(pred, np.arange(0, 1, 0.01), alpha=0.6)
plt.hist(pred_normed, np.arange(0, 1, 0.01), alpha=0.8)
plt.show()

# save the model to disk
filename = 'trained_models/model_' + code_property + '_' + level + '.model'
joblib.dump(model, filename)
  
print(mean_squared_error(data["scores_ANN"], pred))
print(mean_absolute_error(data["scores_ANN"], pred))