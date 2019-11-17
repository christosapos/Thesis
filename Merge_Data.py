from System_non_maintainability.Folders import *
import json
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import seaborn as sns
from System_non_maintainability.Measures import *
from sklearn.svm import OneClassSVM
from sklearn.externals import joblib

import pandas as pd
import csv
from collections import OrderedDict
import seaborn as sns

import time
from System_non_maintainability.Thresholds import *



class MergeData:
    
    measures=[]
    
    def __init__(self,measures):
        MergeData.measures=measures
    '''
    method which plot the distribution of all classes of the percentage of the releases that 
    the classes has changes to the total releases that the classes has appeared
    '''
    def plot_distribution_changes(self,projects):
          
        data=[]
        
        for project in projects:
            change_folder('Results_Classes_'+project)
            
            with open("changes_dropped.json",'r')as handle:
                changes_dropped=json.load(handle)
            
            with open("changes_non_dropped.json",'r')as handle:
                changes_non_dropped=json.load(handle)
                
            for clas in changes_dropped:
                if changes_dropped[clas]['total']>0:
                    value=changes_dropped[clas]['changes']/changes_dropped[clas]['total']
                    data.append(value)
                
            for clas in changes_non_dropped:
                if changes_non_dropped[clas]['total']>0:
                    value=changes_non_dropped[clas]['changes']/changes_non_dropped[clas]['total']
                    data.append(value)
            
        move_initial_folder()
        change_folder("Results_Merge_Data")
        sns.distplot(data,kde=False,rug=False)
        plt.savefig("distribution of total changes")
        plt.clf()
    
    '''
    method which produces three jsons for the training data
    first json contains first values of measures of training data
    second json contains last values of measures of training data
    thrid json contains final coefs of measures of training data
    '''  
    def create_model_data(self): 
        
        projects=[]
        projects.append('apache_struts')
        projects.append("spring-projects_spring-framework")
        
        start_values_data={}
        end_values_data={}
        coefs_data={}
        
        measures=return_meas_per_prop()
        thres=set_thresholds_measures(self)
        
        count=0
        count1=0
        
        for project in projects:
            
            change_folder("Results_Classes_"+project)
            
            with open("recalc_dropped_data.json",'r')as handle:
                recalc_data=json.load(handle)
            
            with open("final_coefs_dropped.json",'r')as handle:
                final_coefs=json.load(handle)
            
            with open("dropped_classes_start_stop.json",'r')as handle:
                limits=json.load(handle)
            
            with open("anomalies.json",'r')as handle:
                anomalies=json.load(handle)
            
            with open("filter_classes.json",'r')as handle:
                filter=json.load(handle)
            
            with open("short_life_classes.json",'r')as handle:
                short_life=json.load(handle)
            
            
            for clas in recalc_data:
                
                if clas not in short_life and clas in filter and clas not in anomalies:
                
                    end_timeline=limits[clas][2]
                    start_timeline=limits[clas][0]
                    
                    for property in measures:
                        
                        meas_values={}
                        flag=False    
                        
                        if property not in start_values_data:
                            start_values_data[property]={}
                            end_values_data[property]={}
                            coefs_data[property]={}
                        
                        count_meas=0
                        for measure in measures[property]:
                            
                            if measure not in start_values_data[property]:
                                
                                start_values_data[property][measure]=[]
                                end_values_data[property][measure]=[]
                                coefs_data[property][measure]=[]
                                
                            first_value=recalc_data[clas][start_timeline]['Metrics '+measure][0]
                            last_value=recalc_data[clas][end_timeline]["Metrics "+measure][-1]
                            coef=round(final_coefs[clas][measure],4)
                            
                            if property=="cohesion":
                                start_values_data[property][measure].append(first_value)
                                end_values_data[property][measure].append(last_value)
                                coefs_data[property][measure].append(coef)
                               
                            if property !="cohesion":
                                meas_values[measure]=[first_value,last_value,coef]
                                
                                if property !="documentation":
                                    if last_value>thres[measure]:
            
                                        flag=True
                                else:
                                    if last_value>thres[measure]:
                                        
                                        count_meas+=1
                                        if count_meas==len(measures[property]):
                                            flag=True
                            
                        if property !="cohesion":
                            if flag==True:
                                
                                count+=1
                                
                                for measure in meas_values:
                                    
                                    
                                    start_values_data[property][measure].append(meas_values[measure][0])
                                    end_values_data[property][measure].append(meas_values[measure][1])
                                    coefs_data[property][measure].append(meas_values[measure][2])
                                        
                                    
        
        
        
        
        move_initial_folder()
        
        change_folder("Training")
        
        with open("start_data_first_values.json",'w')as outfile:
            json.dump(start_values_data,outfile)
        
        with open("start_data_end_values.json",'w')as outfile: 
            json.dump(end_values_data,outfile)
        
        with open("start_data_coefs.json",'w')as outfile:
            json.dump(coefs_data,outfile)
        
    '''
    method which produces a json with the last values for every measure 
    of training data
    '''    
    def find_last_appear(self): 
        
        move_initial_folder()
        projects=[]
        projects.append('apache_struts')
        projects.append('spring-projects_spring-framework')
        
        measures=return_measures()
        
        last_values={}
        for project in projects:
                
            change_folder("Results_Classes_"+project)
            
            with open("dropped_classes_start_stop.json",'r')as handle:
                dropped_limits=json.load(handle)
            
            with open("classes_data_measures_dropped.json",'r')as handle:
                dropped_data=json.load(handle)
            
            with open("short_life_classes.json",'r')as handle:
                short_classes=json.load(handle)
            
            with open("filter_classes.json",'r')as handle:
                filter=json.load(handle)
            
            with open("anomalies.json",'r')as handle:
                anomalies=json.load(handle)
                
            
            for clas in dropped_data:
                
                    for measure in measures:
                        if measure not in last_values:
                            last_values[measure]=[]
                        end_timeline=dropped_limits[clas][2]
                        
                        value=dropped_data[clas][end_timeline]['Metrics '+measure][-1]
                        last_values[measure].append(value)
        
        move_initial_folder()
        change_inside_folder("Results_Merge_Data")
        
        with open("last_values.json",'w')as outfile:
            json.dump(last_values,outfile)
       
    '''
    method which plot the distributions of last values of training data for all metrics
    ''' 
    def plot_distribution_last_appear(self):
        
        change_folder("Results_Merge_Data")
        
        with open("last_values.json",'r')as handle:
            last_values=json.load(handle)
        
        change_inside_folder("distribution_last_values")
        
        recal_last_values={}
        
        for measure in last_values:
            
            
                
                last_values[measure].sort()
                
                t=last_values[measure]
                recal_last_values[measure]=t[0:int(0.95*len(t))+1]
            
                sns.distplot(recal_last_values[measure],kde=False,rug=True)
                plt.title("distribution of last values "+measure)
                plt.savefig('dropped '+measure)
                plt.clf()
               
                  
    '''
    method which create for every property many models based on parameters nu, gama and kernel
    '''
    def create_multiple_candidate_models(self):
        
        measures=return_meas_per_prop()
        
        change_folder("Training")
        with open("start_data_coefs.json",'r')as handle:
            first_values=json.load(handle)
        
        with open("start_data_end_values.json",'r')as handle:
            last_values=json.load(handle)
        
        with open("start_data_coefs.json",'r')as handle:
            aver_coefs=json.load(handle)
        
    
        for property in measures:
            
            count=0
            
           
            for measure in measures[property]:
               
                count+=1
                I=np.array([[first_values[property][measure][j],last_values[property][measure][j],aver_coefs[property][measure][j]] for j in range(0,len(first_values[property][measure]))])
                if count==1:
                    I2=I
                else:
                    I2=np.concatenate((I2,I),axis=1)
            
            
        
        
            change_inside_folder(property) 
            change_inside_folder("poly") #we can change the kernel to rbf and linear
            nu_tes=0
            gama=0
            
            for a in range(1,21):
                nu_tes=(a*0.01)
                
                for b in range(1,21):
                    gama=(b*0.01)
                    
                    #kernel can change to linear and rbf
                    clf = OneClassSVM(kernel="poly",nu=nu_tes,gamma=gama)
                    clf.fit(I2)
        
                    joblib.dump(clf,'nu_'+str(nu_tes)+'gama_'+str(gama)+'_'+property+'_model.joblib')
                gama=0
            
            
            move_initial_folder()
            change_folder("Training")
            change_inside_folder('models')   
            
    #method which create a model for every property based on the best combination of nu,gama and kernel according to percentage of prediction
    def create_final_models(self):
        
        measures=return_meas_per_prop()
        
    
        change_folder("Training")
        with open("start_data_coefs.json",'r')as handle:
            first_values=json.load(handle)
        
        with open("start_data_end_values.json",'r')as handle:
            last_values=json.load(handle)
        
        with open("start_data_coefs.json",'r')as handle:
            aver_coefs=json.load(handle)
         
        propert_attr={}
        propert_attr['cohesion']=[0.01,0.01]
        propert_attr['complexity']=[0.01,0.01]
        propert_attr['documentation']=[0.01,0.01]
        propert_attr['size']=[0.01,0.01]
        propert_attr['coupling']=[0.01,0.01]
        propert_attr['inheritance']=[0.01,0.01]
        
        for property in measures:
            
            count=0
            
           
            for measure in measures[property]:
               
                count+=1
                I=np.array([[first_values[property][measure][j],last_values[property][measure][j],aver_coefs[property][measure][j]] for j in range(0,len(first_values[property][measure]))])
                if count==1:
                    I2=I
                else:
                    I2=np.concatenate((I2,I),axis=1)
            
            
            nu_tes=propert_attr[property][0]
            gama=propert_attr[property][1]
            clf = OneClassSVM(kernel="poly",nu=nu_tes,gamma=gama)
            clf.fit(I2)
        
            joblib.dump(clf,'nu_'+str(nu_tes)+'gama_'+str(gama)+'_'+property+'_model.joblib')
                
            
    '''
    method which creates three json for target dropped data
    first json contains for all measues the start values of target data
    second json contains for all measures last values of target data
    third json contains for all measures aver coefs of target data
    '''
    def create_dropped_target_data(self):
        
        measures=return_meas_per_prop()
        
        project='hibernate_hibernate-orm'
        
        change_folder("Results_Classes_"+project)
        
        with open("dropped_classes_start_stop.json",'r')as handle:
            limits=json.load(handle)
        
        with open("recalc_dropped_data.json",'r')as handle:
            recalc_data=json.load(handle)
        
        with open("final_coefs_dropped.json",'r')as handle:
            final_coefs=json.load(handle)
            
        start_values_data={}
        end_values_data={}
        coefs_data={}
        
        
        for clas in recalc_data:
            
            end_timeline=limits[clas][2]
            start_timeline=limits[clas][0]
            
            for property in measures:
                
                if property not in start_values_data:
                    start_values_data[property]={}
                    end_values_data[property]={}
                    coefs_data[property]={}
                
                for measure in measures[property]:
                    
                    if measure not in start_values_data[property]:
                                
                        start_values_data[property][measure]=[]
                        end_values_data[property][measure]=[]
                        coefs_data[property][measure]=[]
                    
                    
                    first_value=recalc_data[clas][start_timeline]["Metrics "+measure][0]
                    last_value=recalc_data[clas][end_timeline]["Metrics "+measure][-1]
                    coef=final_coefs[clas][measure]
                    
                    
                    start_values_data[property][measure].append(first_value)
                    end_values_data[property][measure].append(last_value)
                    coefs_data[property][measure].append(coef)
                    
        move_initial_folder()
        
        change_folder("Training")
    
        with open("end_dropped_data_first_values.json","w")as outfile:
            json.dump(start_values_data,outfile)
        
        with open("end_dropped_data_last_values.json","w")as outfile:
            json.dump(end_values_data,outfile)
        
        with open("end_dropped_data_coefs.json","w")as outfile:
            json.dump(coefs_data,outfile)
    
    '''
    method which creates three json for target non dropped data
    first json contains for all measues the start values of target data
    second json contains for all measures last values of target data
    third json contains for all measures aver coefs of target data
    '''    
    def create_non_dropped_target_data(self):
        
        measures=return_meas_per_prop()
        
        project='hibernate_hibernate-orm'
        
        change_folder("Results_Classes_"+project)
        
        with open("non_dropped_classes_start_stop.json",'r')as handle:
            limits=json.load(handle)
        
        with open("recalc_non_dropped_data.json",'r')as handle:
            recalc_data=json.load(handle)
        
        with open("final_coefs_non_dropped.json",'r')as handle:
            final_coefs=json.load(handle)
            
        start_values_data={}
        end_values_data={}
        coefs_data={}
        
       
        
        for clas in recalc_data:
            
            end_timeline=limits[clas][1]
            start_timeline=limits[clas][0]
            
            for property in measures:
                
                if property not in start_values_data:
                    start_values_data[property]={}
                    end_values_data[property]={}
                    coefs_data[property]={}
                
                for measure in measures[property]:
                    
                    if measure not in start_values_data[property]:
                                
                        start_values_data[property][measure]=[]
                        end_values_data[property][measure]=[]
                        coefs_data[property][measure]=[]
                    
                    first_value=recalc_data[clas][start_timeline]["Metrics "+measure][0]
                    last_value=recalc_data[clas][end_timeline]["Metrics "+measure][-1]
                    coef=final_coefs[clas][measure]
                    
                    start_values_data[property][measure].append(first_value)
                    end_values_data[property][measure].append(last_value)
                    coefs_data[property][measure].append(coef)
                    
        move_initial_folder()
        change_folder("Training")
        
        with open("end_non_dropped_data_first_values.json","w")as outfile:
            json.dump(start_values_data,outfile)
        
        with open("end_non_dropped_data_last_values.json","w")as outfile:
            json.dump(end_values_data,outfile)
        
        with open("end_non_dropped_data_coefs.json","w")as outfile:
            json.dump(coefs_data,outfile)
        
    
    '''
    method which use dropped target data to all models of properties based on gama,nu and kernel 
    prints the percentage of predict for these models and keeps the higher predictions 
    '''
    def print_prediction_multiple_models(self):
        
        change_folder("Results_Merge_Data")
        
        measures=return_meas_per_prop()
        
        with open("end_dropped_data_first_values.json",'r')as handle:
            first_values=json.load(handle)
        
        with open("end_dropped_data_last_values.json",'r')as handle:
            last_values=json.load(handle)
            
        with open("end_dropped_data_coefs.json",'r')as handle:
            aver_coefs=json.load(handle)
        
        move_initial_folder()
        change_folder("Training")
        change_inside_folder("models")
        
        for property in measures:
        
            change_inside_folder(property)
            change_inside_folder("poly")    #It can be change to  linear and rbf 
            count=0
            for measure in measures[property]:
               
                count+=1
                I=np.array([[first_values[property][measure][j],last_values[property][measure][j],aver_coefs[property][measure][j]] for j in range(0,len(first_values[property][measure]))])
                if count==1:
                    I2=I
                else:
                    I2=np.concatenate((I2,I),axis=1)
            
            
            
        
            max_per=0
            max_a=0
            max_b=0
            
            count=0
            
            vals=[[0 for c in range(20)]for t in range(20)]
            label_col=[69/255,139/255,116/255]
            colors=[[(245/255,245/255,220/255) for c in range(20)]for t in range(20)]
        
            labely=[]
            labelx=[]
            nu_1=0
            for k in range(1,21):
                nu_1=0.01*k
                labely.append(nu_1)
                labelx.append(nu_1)
            
            for a in range(1,21):
                nu_tes=(a*0.01)
                for b in range(1,21):
                    gama=(b*0.01)
                    
                    clf=joblib.load('nu_'+str(nu_tes)+'gama_'+str(gama)+'_'+property+'_model.joblib')
            
                    predictions=clf.predict(I2)
                    decision=clf.decision_function(I2)
                    
                    k=round(predictions.tolist().count(1)/len(predictions),3)
                    if k>max_per:
                        max_per=k
                        max_a=a
                        max_b=b
                    
                    vals[a-1][b-1]=k
            
            colors[max_a-1][max_b-1]=[0,0,238/255]
            
            tab=plt.table(cellText=vals,
                  rowLabels=labelx,
                  colLabels=labely,
                  rowColours=[label_col]*20,
                  colColours=[label_col]*20,
                  cellColours=colors,
                  cellLoc='center',
                  loc='upper left'
                  )
        
            plt.axis('off')
            
            move_initial_folder()
            change_folder("Training")
            change_inside_folder("Best_models")
            plt.savefig(property)
            plt.clf()
            
            move_initial_folder()
            change_folder("Training")
            change_inside_folder("models")
            
            print('Max percentage '+str(max_per)+' for nu '+str(max_a*0.01)+' and for gama '+str(max_b*0.01)+" property "+property)
            

      
    '''
    method which create for every property csv files with all dropped classes
    and first values,last values and final coefs of all measures inside property 
    '''
    def create_csv_data_dropped(self,projects):
        
        measures=return_meas_per_prop()
        
        classes=[]
        proj=[]
        
        start_values_data={}
        end_values_data={}
        coefs_data={}
        
        for project in projects:
            
            change_folder("Results_Classes_"+project)
            
            with open("recalc_dropped_data.json",'r')as handle:
                recalc_data=json.load(handle)
            
            with open("final_coefs_dropped.json",'r')as handle:
                final_coefs=json.load(handle)
            
            with open("dropped_classes_start_stop.json",'r')as handle:
                limits=json.load(handle)
                
            with open("anomalies.json",'r')as handle:
                anomalies=json.load(handle)
            
            with open("filter_classes.json",'r')as handle:
                filter=json.load(handle)
            
            with open("short_life_classes.json",'r')as handle:
                short_life=json.load(handle)
            
            
            for clas in recalc_data:
                
                    #if clas not in short_life and clas in filter and clas not in anomalies:
                
                    end_timeline=limits[clas][2]
                    start_timeline=limits[clas][0]
                    
                    classes.append(clas)
                    proj.append(project)
                        
                    for property in measures:
                        
                        if property not in start_values_data:
                                start_values_data[property]={}
                                end_values_data[property]={}
                                coefs_data[property]={}
                        
                        for measure in measures[property]:
                            
                            if measure not in start_values_data[property]:
                                    
                                    start_values_data[property][measure]=[]
                                    end_values_data[property][measure]=[]
                                    coefs_data[property][measure]=[]
                    
                            first_value=recalc_data[clas][start_timeline]['Metrics '+measure][0]
                            last_value=recalc_data[clas][end_timeline]["Metrics "+measure][-1]
                            coef=round(final_coefs[clas][measure],4)
                                
                
                            start_values_data[property][measure].append(first_value)
                            end_values_data[property][measure].append(last_value)
                            coefs_data[property][measure].append(coef)
            
        move_initial_folder()
        change_inside_folder("Csvs_files_dropped")
        for property in measures:
            data=OrderedDict()
            data['classes']=classes
            data['project']=proj
            
            for measure in measures[property]:
                
                
                data['Start values '+measure]=start_values_data[property][measure]
                data['Last values '+measure]=end_values_data[property][measure]
                data['Coefs '+measure]=coefs_data[property][measure]
                ind=[]
            
            for a in range(0,len(classes)):
                ind.append(a+1)
            df=pd.DataFrame(data,index=ind)
            df.to_csv(property+".csv",encoding='utf-8')
     
    '''
    method which creates for every property csv files with all non dropped classes
    first values,last values and final coefs of all measures inside property 
    '''       
    def create_csv_data_non_dropped(self,projects):
        
        measures=return_meas_per_prop()
        
        classes=[]
        proj=[]
        
        start_values_data={}
        end_values_data={}
        coefs_data={}
        
        for project in projects:
            
            change_folder("Results_Classes_"+project)
            
            with open("recalc_non_dropped_data.json",'r')as handle:
                recalc_data=json.load(handle)
            
            with open("final_coefs_non_dropped.json",'r')as handle:
                final_coefs=json.load(handle)
            
            with open("non_dropped_classes_start_stop.json",'r')as handle:
                limits=json.load(handle)
                
            with open("anomalies.json",'r')as handle:
                anomalies=json.load(handle)
            
            with open("filter_classes.json",'r')as handle:
                filter=json.load(handle)
            
            with open("short_life_classes.json",'r')as handle:
                short_life=json.load(handle)
            
            
            for clas in recalc_data:
                
                    #if clas not in short_life and clas in filter and clas not in anomalies:
                
                    end_timeline=limits[clas][1]
                    start_timeline=limits[clas][0]
                    
                    classes.append(clas)
                    proj.append(project)
                        
                    for property in measures:
                        
                        if property not in start_values_data:
                                start_values_data[property]={}
                                end_values_data[property]={}
                                coefs_data[property]={}
                        
                        for measure in measures[property]:
                            
                            if measure not in start_values_data[property]:
                                    
                                    start_values_data[property][measure]=[]
                                    end_values_data[property][measure]=[]
                                    coefs_data[property][measure]=[]
                    
                            first_value=recalc_data[clas][start_timeline]['Metrics '+measure][0]
                            last_value=recalc_data[clas][end_timeline]["Metrics "+measure][-1]
                            coef=round(final_coefs[clas][measure],4)
                                
                
                            start_values_data[property][measure].append(first_value)
                            end_values_data[property][measure].append(last_value)
                            coefs_data[property][measure].append(coef)
            
        move_initial_folder()
        change_inside_folder("Csvs_files_non_dropped")
        for property in measures:
            data=OrderedDict()
            data['classes']=classes
            data['project']=proj
            for measure in measures[property]:
                
                
                data['Start values '+measure]=start_values_data[property][measure]
                data['Last values '+measure]=end_values_data[property][measure]
                data['Coefs '+measure]=coefs_data[property][measure]
                
            ind=[]
            
            for a in range(0,len(classes)):
                ind.append(a+1)
            df=pd.DataFrame(data,index=ind)
            df.to_csv(property+".csv",encoding='utf-8')
            
    '''
    method which create for every property distributions of scores of target non dropped classes
    it also creates a csv files with all non dropped target classes, their first values ,last values
    ,final coefs of all measures, their scores for all properties and the final average scores of the
    prediction
    '''                                    
    def create_distribution_scores_non_dropped(self):
        
        measures=return_meas_per_prop()
        
        change_folder("Training")
        
        with open("end_non_dropped_data_first_values.json",'r')as handle:
            first_values=json.load(handle)
        
        with open("end_non_dropped_data_last_values.json",'r')as handle:
            last_values=json.load(handle)
        
        with open("end_non_dropped_data_coefs.json",'r')as handle:
            aver_coefs=json.load(handle)
        
        
    
        
        propert_attr={}
        propert_attr['cohesion']=[0.01,0.01]
        propert_attr['complexity']=[0.01,0.01]
        propert_attr['documentation']=[0.01,0.01]
        propert_attr['size']=[0.01,0.01]
        propert_attr['coupling']=[0.01,0.01]
        propert_attr['inheritance']=[0.01,0.01]
        
        non_dropped_scores=OrderedDict()
         
        for property in measures:
            
            
            
            
            count1=0
            start=time.time()
            for measure in measures[property]:
                
                non_dropped_scores['Start_values '+measure]=first_values[property][measure]
                non_dropped_scores['Last values '+measure]=last_values[property][measure]
                non_dropped_scores['Coefs '+measure]=aver_coefs[property][measure]
                
               
                count1+=1
                I=np.array([[first_values[property][measure][j],last_values[property][measure][j],aver_coefs[property][measure][j]] for j in range(0,len(first_values[property][measure]))])
                if count1==1:
                    I2=I
                else:
                    I2=np.concatenate((I2,I),axis=1)
            end=time.time()
            
            
            nu_tes=propert_attr[property][0]
            gama=propert_attr[property][1]
            

            clf=joblib.load('nu_'+str(nu_tes)+'gama_'+str(gama)+'_'+property+'_model.joblib')

            predictions=clf.predict(I2)
            
            
            
            decision=clf.decision_function(I2)
            
            decis=[]
            for val in decision:
                decis.append(val[0])
            
            sort_dec=[]
            for val in decis:
                sort_dec.append(val)
            sort_dec.sort()
    
            
            min_lim=sort_dec[int(0.05*len(sort_dec))+1]
            max_lim=sort_dec[int(0.95*len(sort_dec))+1]
            
            
            A=[]
            
            

            for val in decis:

                
                if val>0:
                    if val<max_lim:
                        b=0.5+(val/max_lim)*0.5
                        
                        if property=="cohesion":
                            b-=0.01
                    else:
                        b=1
                    
                    if b>1:
                        b=1
                    if property =='documentation': 
                        A.append(1-b)
                    else:
                        A.append(b)
                    
                elif val<0:
                    if val>min_lim:
                        b=0.5-(val/min_lim)*0.5
                    else:
                        b=0
                   
                    
                    if property =='documentation':
                        A.append(1-b)
                    else:
                        A.append(b)
                         
                else:
                    if property=="documentation":
                        A.append(0.5)
                    else:
                        A.append(0.5)
                
            

            non_dropped_scores['Score of '+property]=A
            
           
            plt.hist(A,weights=np.ones(len(A))/len(A),bins=30)#move_initial_folder()
            
            plt.ylim(0,1.0)
            plt.savefig(property+"_non_dropped.png")
            plt.clf()
            
        average_score=[]
        for count in range(0,len(A)):
            aver=0
            for property in measures:
                val=non_dropped_scores['Score of '+property][count]
                aver+=val
            average_score.append(aver/len(measures))
        non_dropped_scores['Average_score']=average_score
        
        pos_score=[]
        for count in range(0,len(A)):
            posit=0
            for property in measures:
                val=non_dropped_scores['Score of '+property][count]
                if val>0.5:
                    posit+=val
                    
            pos_score.append(posit)
        non_dropped_scores["Positive_score"]=pos_score
                
        
        
        df=pd.DataFrame(non_dropped_scores)
        
        df.to_csv("non_dropped_scores.csv",encoding='utf-8',index=False)
        
    '''
    method which create for every property distributions of scores of target dropped classes
    it also creates a csv files with all dropped target classes, their first values ,last values
    ,final coefs of all measures, their scores for all properties and the final average scores of the
    prediction
    '''    
    def create_distribution_scores_dropped(self):   
        
        measures=return_meas_per_prop()
        
        change_folder("Training")
         
        with open("end_dropped_data_first_values.json",'r')as handle:
            first_values=json.load(handle)
        
        with open("end_dropped_data_last_values.json",'r')as handle:
            last_values=json.load(handle)
        
        with open("end_dropped_data_coefs.json",'r')as handle:
            aver_coefs=json.load(handle)
            
        propert_attr={}
        propert_attr['cohesion']=[0.01,0.01]
        propert_attr['complexity']=[0.01,0.01]
        propert_attr['documentation']=[0.01,0.01]
        propert_attr['size']=[0.01,0.01]
        propert_attr['coupling']=[0.01,0.01]
        propert_attr['inheritance']=[0.01,0.01]
        dropped_scores=OrderedDict()
        
        for property in measures:
            
            count1=0
            for measure in measures[property]:
                
                dropped_scores['Start_values '+measure]=first_values[property][measure]
                dropped_scores['Last values '+measure]=last_values[property][measure]
                dropped_scores['Coefs '+measure]=aver_coefs[property][measure]
                
               
                count1+=1
                I=np.array([[first_values[property][measure][j],last_values[property][measure][j],aver_coefs[property][measure][j]] for j in range(0,len(first_values[property][measure]))])
                if count1==1:
                    I2=I
                else:
                    I2=np.concatenate((I2,I),axis=1)
         
            nu_tes=propert_attr[property][0]
            gama=propert_attr[property][1]
            
            clf=joblib.load('nu_'+str(nu_tes)+'gama_'+str(gama)+'_'+property+'_model.joblib')
            
            predictions=clf.predict(I2)
            decision=clf.decision_function(I2)
            
            
            decis=[]
            for val in decision:
                decis.append(val[0])
            
            sort_dec=[]
            for val in decis:
                sort_dec.append(val)
            sort_dec.sort()
            
            
            min_lim=sort_dec[int(0.05*len(sort_dec))+1]
            max_lim=sort_dec[int(0.95*len(sort_dec))+1]
            
           
                        
            A=[]
            for val in decis:
                
                if val>0:
                    if val<max_lim:
                        b=0.5+(val/max_lim)*0.5
                        if property=="cohesion":
                            b-=0.01
                    else:
                        b=1
                    
                    
                    if b>1:
                        b=1
                    

                    if property=="documentation":
                        A.append(1-b)
                    else:
                        A.append(b)
                elif val<0:
                    if val>min_lim:
                        b=0.5-(val/min_lim)*0.5
                    else:
                        b=0
                    
                    if property=="documentation":
                        A.append(1-b)
                    else:
                        A.append(b)
                else:
                    if property=="documentation":
                        A.append(0.5)
                    else:
                        A.append(0.5)
                    
            dropped_scores['Score of '+property]=A
            
            
            plt.hist(A,weights=np.ones(len(A))/len(A),bins=30)
            plt.ylim(0,1.0)
            plt.savefig(property+"_dropped.png")
            plt.clf()
        
        average_score=[]
        for count in range(0,len(A)):
            aver=0
            for property in measures:
                val=dropped_scores['Score of '+property][count]
                aver+=val
            average_score.append(aver/len(measures))
        dropped_scores['Average_score']=average_score
        
        pos_score=[]
        for count in range(0,len(A)):
            posit=0
            for property in measures:
                val=dropped_scores['Score of '+property][count]
                if val>0.5:
                    posit+=val
                    
            pos_score.append(posit)
        dropped_scores["Positive_score"]=pos_score
        
        df=pd.DataFrame(dropped_scores)
        df.to_csv("dropped_scores.csv",encoding='utf-8',index=False)
     
    '''
    method which creates histogram with the percentage of target dropped classes
    which have n number of faults
    '''   
    def create_histogram_percentage_faults(self):
        
        measures=return_meas_per_prop()
        
        cols=[]
        for property in measures:
            cols.append("Score of "+property)
            
        change_folder("Training")
        
        df=pd.read_csv("dropped_scores.csv",usecols=["Average_score"]+cols+["Positive_score"])
        df1=df.loc[:,"Average_score"]
        
        A=[]
        for count in range(0,len(df1)):
            A.append(0)
            for prop in cols:
                df_prop=df.loc[:,prop]
                if df_prop[count]>0.5:
                    A[count]+=1
        
        B=[]
        for count in range(0,7):
            B.append(0)
        
        for val in A:
            B[val]+=1
        
        for count in range(0,len(B)):
            B[count]=B[count]/len(A)
            print(B[count])
    
        objects=(0,1,2,3,4,5,6)
        y_pos=np.arange(len(objects))
        
        performance=[B[0],B[1],B[2],B[3],B[4],B[5],B[6]]
        
        labels=[]
        for val in performance:
            labels.append([str(round(val*100,2))+"%"])
        count_x=0
        for y,label in zip(performance,labels):
            plt.bar(count_x,y,label=label)
            count_x+=1 
       
       
        plt.xticks(y_pos, objects)
        plt.ylim(0,1.0)
        plt.ylabel("Propability")
        plt.title("Percentage of classes with n violations")
        plt.legend()
        
        plt.savefig("Number_of_violations.png")
        plt.clf()

    
    '''
    method which creates histogram with the percentage of target dropped classes
    which have at least n number of faults
      
    '''        
    def create_bar_plots_min_faults(self):
        
        measures=return_meas_per_prop()
        
        cols=[]
        for property in measures:
            cols.append("Score of "+property)
            
        change_folder("Training")
        
        df=pd.read_csv("dropped_scores.csv",usecols=["Average_score"]+cols+["Positive_score"])
        df1=df.loc[:,"Average_score"]
        
        A=[]
        for count in range(0,len(df1)):
            A.append(0)
            for prop in cols:
                df_prop=df.loc[:,prop]
                if df_prop[count]>0.5:
                    A[count]+=1
        
        B=[]
        for count in range(0,7):
            B.append(0)
        
        for val in A:
            B[val]+=1
        
        sum_val=0
        for count in range(0,len(B)):
            val=B[count]
            B[count]=(len(A)-sum_val)/len(A)
            sum_val+=val
        
        objects=(1,2,3,4,5,6)
        y_pos=np.arange(len(objects))
        
        performance=[B[1],B[2],B[3],B[4],B[5],B[6]]
        
        labels=[]
        for val in performance:
            labels.append([str(round(val*100,2))+"%"])
        count_x=0
        for y,label in zip(performance,labels):
            plt.bar(count_x,y,label=label)
            count_x+=1 
       
       
        plt.xticks(y_pos, objects)
        plt.ylim(0,1.0)
        plt.ylabel("Propability")
        plt.title("Percentage of classes with at least n violations")
        plt.legend()
        
        plt.savefig("At_least_violations.png")
        plt.clf()
        
    '''
    method which produces distribution of scores for all properties  
    of target dropped classes
    ''' 
    def distribution_total_scores(self):
        measures=return_meas_per_prop()
        
        cols=[]
        for property in measures:
            cols.append("Score of "+property)
            
        change_folder("Training")
        
        df=pd.read_csv("dropped_scores.csv",usecols=["Average_score"]+cols+["Positive_score"])
        
        
        for property in measures:
            
            
            col="Score of "+property
            df_prop=df.loc[:,col]
            
            plt.hist(df_prop,weights=np.ones(len(df_prop))/len(df_prop),bins=20)
            plt.title("Distribution of scores "+property)
            #plt.ylim(0,1.0)
            
            plt.savefig('Distribution_of _scores_'+property+'.png')
            plt.clf()
            
            
    '''
    method which produces barplot with the percentage of prediction of target dropped classes
    for every property
    '''
    def barplot_predict_percentage_model(self):
        
        change_folder("Training")
        
        objects=("Cohesion","Complexity","Documentation","Size","Inheritance","Coupling","Final")
        y_pos=np.arange(len(objects))
        
        performance=[0.244,0.3547,0.5265,0.4783,0.2185,0.4007,0.9397]
        
        plt.figure(figsize=(10,4))
        labels=[]
        for val in performance:
            labels.append([str(round(val*100,2))+"%"])
        count_x=0
        for y,label in zip(performance,labels):
            plt.bar(count_x,y,label=label)
            count_x+=1 
       
       
        plt.xticks(y_pos, objects)
        plt.ylim(0,1.0)
        plt.ylabel("Propability")
        plt.title("Percentage of prediction per property")
        plt.legend()
        
        plt.savefig("Perce_predictions_models.png")
        plt.clf()

    '''
    method which produces distribution of final scores of target dropped classes
    '''
    def distribution_final_scores(self):
        
        measures=return_meas_per_prop()
        
        cols=[]
        for property in measures:
            cols.append("Score of "+property)
            
        change_folder("Training")
        
        df=pd.read_csv("dropped_scores.csv",usecols=["Average_score"]+cols+["Positive_score"])
          
        col="Average_score"
        df_prop=df.loc[:,col]
        
        plt.hist(df_prop,weights=np.ones(len(df_prop))/len(df_prop),bins=20)
        plt.title("Distribution of average scores ")
        #plt.ylim(0,1.0)
        
        plt.savefig('Distribution_of _scores_'+property+'.png')
        plt.clf()
        
        
    
        
         
                