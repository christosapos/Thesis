import pandas
import numpy as np
from sklearn.externals import joblib
import time


class Evaluator():
    
    def __init__(self):
        
        self.complexity_class_model = joblib.load('trained_models/model_complexity_class.model')
        self.complexity_package_model = joblib.load('trained_models/model_complexity_package.model')
        
        self.coupling_class_model = joblib.load('trained_models/model_coupling_class.model')
        self.coupling_package_model = joblib.load('trained_models/model_coupling_package.model')
        
        self.documentation_class_model = joblib.load('trained_models/model_documentation_class.model')
        self.documentation_package_model = joblib.load('trained_models/model_documentation_package.model')
        
        self.inheritance_class_model = joblib.load('trained_models/model_inheritance_class.model')
        self.inheritance_package_model = joblib.load('trained_models/model_inheritance_package.model')
        
        self.size_class_model = joblib.load('trained_models/model_size_class.model')
        self.size_package_model = joblib.load('trained_models/model_size_package.model')
        
        self.metrics_per_model = {}
        self.metrics_per_model["Complexity_Class"] = ["McCC", "WMC", "NL"]
        self.metrics_per_model["Complexity_Package"] = ["NL", "WMC"]
        self.metrics_per_model["Coupling_Class"] = ["NII", "RFC", "CBO"]
        self.metrics_per_model["Coupling_Package"] = ["NII", "CBOI", "RFC"]
        self.metrics_per_model["Documentation_Class"] = ["TCD", "DLOC", "TCLOC"]
        self.metrics_per_model["Documentation_Package"] = ["TCD", "DLOC", "TCLOC"]
        self.metrics_per_model["Inheritance_Class"] = ["DIT", "NOC"]
        self.metrics_per_model["Inheritance_Package"] = ["NOC","DIT"]
        self.metrics_per_model["Size_Class"] = ["NUMPAR", "TNG", "TNA", "NPA", "TLLOC", "TNLS"]
        self.metrics_per_model["Size_Package"] = ["NG", "NPA", "TNIN", "TLLOC", "TNLA", "TNLS"]

        self.weights = {}
        self.weights["Complexity_Class"] = 0.207
        self.weights["Complexity_Package"] = 0.192
        self.weights["Coupling_Class"] = 0.210
        self.weights["Coupling_Package"] = 0.148
        self.weights["Documentation_Class"] = 0.197
        self.weights["Documentation_Package"] = 0.322
        self.weights["Inheritance_Class"] = 0.177
        self.weights["Inheritance_Package"] = 0.043
        self.weights["Size_Class"] = 0.208
        self.weights["Size_Package"] = 0.298
        
    def create_data_schema(self, metrics):
    
        data_schema = {}
        for metric in metrics:
            data_schema[metric] = []
        
        return data_schema

    def get_normalization_Specs(self, property, level):
        
        df = pandas.read_csv('trained_models/models_specs.txt')
        specs = {}
        specs["min"] = df[(df["Property"] == property) & (df["Level"] == level)]["Minimum"].iloc[0]
        specs["max"] = df[(df["Property"] == property) & (df["Level"] == level)]["Maximum"].iloc[0]
        
        return specs
        

    def evaluate_complexity(self, data, level):
        
        metrics = self.metrics_per_model["Complexity_" + level]
        if(level == 'Class'):
            model = self.complexity_class_model
        else:
            model = self.complexity_package_model
            
        info = self.create_data_schema(metrics)
        for obj in data:
            for metric in metrics:
                info[metric].append(obj[metric])
        
        df = pandas.DataFrame(info)
        
        # Re-arrange columns in order for the model to work
        df = df[metrics]
        
        pred = model.predict(df)
        specs = self.get_normalization_Specs('Complexity', level)
        pred_normed = ((pred - specs["min"]) / (specs["max"] - specs["min"]))
        
        df["complexity_score"] = pred_normed
        
        return df, pred_normed

    def evaluate_coupling(self, data, level):
        
        metrics = self.metrics_per_model["Coupling_" + level]
        if(level == 'Class'):
            model = self.coupling_class_model
        else:
            model = self.coupling_package_model
            
        info = self.create_data_schema(metrics)
        for obj in data:
            for metric in metrics:
                info[metric].append(obj[metric])
        
        df = pandas.DataFrame(info)
        # Re-arrange columns in order for the model to work
        df = df[metrics]
        
        pred = model.predict(df)
        specs = self.get_normalization_Specs('Coupling', level)
        
        pred_normed = ((pred - specs["min"]) / (specs["max"] - specs["min"]))
        
        df["coupling_score"] = pred_normed
        
        return df, pred_normed
    
    def evaluate_documentation(self, data, level):
        
        metrics = self.metrics_per_model["Documentation_" + level]
        if(level == 'Class'):
            model = self.documentation_class_model
        else:
            model = self.documentation_package_model
            
        info = self.create_data_schema(metrics)
        for obj in data:
            for metric in metrics:
                info[metric].append(obj[metric])
        
        df = pandas.DataFrame(info)
        # Re-arrange columns in order for the model to work
        df = df[metrics]
        
        pred = model.predict(df)
        specs = self.get_normalization_Specs('Documentation', level)
        pred_normed = ((pred - specs["min"]) / (specs["max"] - specs["min"]))
        
        df["documentation_score"] = pred_normed
        
        return df, pred_normed
    
    def evaluate_inheritance(self, data, level):
        
        metrics = self.metrics_per_model["Inheritance_" + level]
        if(level == 'Class'):
            model = self.inheritance_class_model
        else:
            model = self.inheritance_package_model
            
        info = self.create_data_schema(metrics)
        for obj in data:
            for metric in metrics:
                info[metric].append(obj[metric])
        
        df = pandas.DataFrame(info)
        # Re-arrange columns in order for the model to work
        df = df[metrics]
        
        pred = model.predict(df)
        specs = self.get_normalization_Specs('Inheritance', level)
        pred_normed = ((pred - specs["min"]) / (specs["max"] - specs["min"]))
        df["inheritance_score"] = pred_normed
        
        return df, pred_normed

    def evaluate_size(self, data, level):
        
        metrics = self.metrics_per_model["Size_" + level]
        if(level == 'Class'):
            model = self.size_class_model
        else:
            model = self.size_package_model
            
        info = self.create_data_schema(metrics)
        for obj in data:
            for metric in metrics:
                info[metric].append(obj[metric])
        
        df = pandas.DataFrame(info)
        # Re-arrange columns in order for the model to work
        df = df[metrics]
        
        pred = model.predict(df)
        specs = self.get_normalization_Specs('Size', level)
        pred_normed = ((pred - specs["min"]) / (specs["max"] - specs["min"]))
        df["size_score"] = pred_normed
        
        return df, pred_normed
    
    def evaluate_all_properies(self, data, level):
        
        df1 = self.evaluate_complexity(data, level)[0]
        df2 = self.evaluate_coupling(data, level)[0]
        df3 = self.evaluate_documentation(data, level)[0]
        df4 = self.evaluate_inheritance(data, level)[0]
        df5 = self.evaluate_size(data, level)[0]
        
        df = pandas.concat([df1, df2, df3, df4, df5], axis=1)
        df["final_score"] = df["complexity_score"] * self.weights["Complexity_" + level] + \
                            df["coupling_score"] * self.weights["Coupling_" + level] + \
                            df["documentation_score"] * self.weights["Documentation_" + level] + \
                            df["inheritance_score"] * self.weights["Inheritance_" + level] + \
                            df["size_score"] * self.weights["Size_" + level]
        
        return df
        
       
# evaluator = Evaluator()
# 
# info = []
# metrics = {"WMC": 24, "McCC": 10, "NL": 5, 
#            "NII": 3, "RFC": 3, "CBO": 1, 
#            "TCD": 0.1, "DLOC": 50, "TCLOC": 55,
#            "DIT": 1, "NOC": 5,
#            "NUMPAR": 47, "TNG": 0, "TNA": 18, "NPA": 2, "TLLOC": 159, "TNLS": 0
#            }
# info.append(metrics)
# metrics = {"WMC": 15, "McCC": 10, "NL": 5, 
#            "NII": 3, "RFC": 3, "CBO": 1, 
#            "TCD": 0.1, "DLOC": 50, "TCLOC": 55,
#            "DIT": 1, "NOC": 5,
#            "NUMPAR": 47, "TNG": 0, "TNA": 18, "NPA": 2, "TLLOC": 159, "TNLS": 0
#            }
# info.append(metrics)
# metrics = {"WMC": 1, "McCC": 1.5, "NL": 2}
# info.append(metrics)
 
# r = evaluator.evaluate_complexity(info, 'Class')[0]
# print(r)
# r = evaluator.evaluate_coupling(info, 'Class')[0]
# print(r)
# r = evaluator.evaluate_documentation(info, 'Class')[0]
# print(r)
# r = evaluator.evaluate_inheritance(info, 'Class')[0]
# print(r)
# r = evaluator.evaluate_size(info, 'Class')[0]
# print(r)
# 
# all = evaluator.evaluate_all_properies(info, 'Class')
# print(all)
