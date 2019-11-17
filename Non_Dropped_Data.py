from System_non_maintainability.Folders import *
import json 
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

class NonDroppedData:
    
    project=''
    measures=[]
    
    def __init__(self,measures,project):
        NonDroppedData.measures=measures
        NonDroppedData.project=project
        
    
    #method which creates coefs between timelines for non_dropped classes and saves them in a json
    def create_coefs_between_timelines(self):
        change_folder("Results_Classes_"+NonDroppedData.project)
        
        with open("recalc_non_dropped_data.json",'r')as handle:
            recalc_data=json.load(handle)
        
        with open("timelines_releases.json",'r')as handle:
            timelines=json.load(handle)
        
        measures=NonDroppedData.measures
        
        X=[1,2]
        Xarray=np.asarray(X)
        Xarray=Xarray.reshape(-1,1)
        
        coefs_between_timelines={}
        
        for clas in recalc_data:
            
            coefs_between_timelines[clas]={}
            
            for count in range (0,len(timelines)-1):
                
                timeline="timeline"+str(count+1)
                next_timeline="timeline"+str(count+2)
                
                if timeline in recalc_data[clas] and next_timeline in recalc_data[clas]:
                    
                    coefs_between_timelines[clas][timeline]={}
                    for measure in measures:
                        
                        Y=[]
                        Y.append(recalc_data[clas][timeline]["Metrics "+measure][-1])
                        Y.append(recalc_data[clas][next_timeline]["Metrics "+measure][0])
                        Yarray=np.asarray(Y)
                        Yarray=Yarray.reshape(-1,1)
                        regr = linear_model.LinearRegression()
                        regr.fit(Xarray, Yarray)
                        b=regr.coef_[0][0] 
                        
                        coefs_between_timelines[clas][timeline][measure]=b
        
        with open("coefs_between_timelines_non_dropped.json",'w')as outfile:
            json.dump(coefs_between_timelines,outfile)
    '''
    method which creates final coefs based on coefs of timelines and between timelines coefs 
    for all non dropped coefs and saves them in a json 
    '''
    def final_coefs_non_dropped(self):
        
        change_folder("Results_Classes_"+NonDroppedData.project)
        
        with open("recalc_non_dropped_coefs.json",'r')as handle:
            recalc_coefs=json.load(handle)
        
        with open("coefs_between_timelines_non_dropped.json",'r')as handle:
            coefs_between_time=json.load(handle)
        
        final_coefs={}
        measures=NonDroppedData.measures
        for clas in recalc_coefs:
            
            final_coefs[clas]={}
            
            for measure in measures:
        
                count=recalc_coefs[clas][measure]['count_timelines']
                total=recalc_coefs[clas][measure]['average_coef']*count
                
                for timeline in coefs_between_time[clas]:
                    total+=coefs_between_time[clas][timeline][measure]
                    count+=1
                
                coef=total/count
                
                final_coefs[clas][measure]=coef
        
        with open("final_coefs_non_dropped.json",'w')as outfile:
            json.dump(final_coefs,outfile)    
    
    '''        
    method which recalculate coefs of timelines of linear regression based on the releases that classes change 
    also creates a json with the average of coefs of timelines           
    '''
    def create_recalculated_data(self):

        change_folder('Results_Classes_'+NonDroppedData.project)
        data={}
        
        measures=NonDroppedData.measures
        
        with open("timelines_releases.json",'r')as handle:
            releases=json.load(handle)

        with open("classes_data_measures_non_dropped.json","r")as handle:
            non_dropped_data=json.load(handle)
        
        string="Metrics "
        
        for clas in non_dropped_data:
            data[clas]={}
            for timeline in non_dropped_data[clas]:
                data[clas][timeline]={}
                length=len(non_dropped_data[clas][timeline][string+measures[0]])
                for count in range(0,length):
                    flag =False
                    if count==0:
                        for measure in measures:
                            string1=string+measure
                            data[clas][timeline][string1]=[]
                            data[clas][timeline][string1].append(non_dropped_data[clas][timeline][string1][0])
                    else:
                        for measure in measures:
                            string1=string+measure
                            if non_dropped_data[clas][timeline][string1][count]!=data[clas][timeline][string1][-1]:
                                flag=True     
                        if flag==True:
                            for measure in measures:
                                string1=string+measure
                                data[clas][timeline][string1].append(non_dropped_data[clas][timeline][string1][count])
              
        print("Checkpoint1")
        
        for clas in data:
            for timeline in data[clas]:
                X=[]
                for x in range(0,len(data[clas][timeline][string+measures[0]])):
                    X.append(x)
                Xarray=np.asarray(X)
                Xarray=Xarray.reshape(-1,1)
            
                for measure in measures:
                    
                    Yarray=np.asarray(data[clas][timeline][string+measure])
                    Yarray=Yarray.reshape(-1,1)
                    regr = linear_model.LinearRegression()
                    regr.fit(Xarray, Yarray)
                    b=regr.coef_[0][0] 
                    data[clas][timeline]['Coefs of '+measure]=b
        
        with open('recalc_non_dropped_data.json','w') as outfile:
            json.dump(data,outfile)   
        print("Checkpoint2")
        data1={}
        for clas in data:
            data1[clas]={}
            for measure in measures:
                data1[clas][measure]={}
                data1[clas][measure]['average_coef']=0
                data1[clas][measure]['count_timelines']=0
            for timeline in data[clas]:
                for measure in measures:
                    data1[clas][measure]['average_coef']+=data[clas][timeline]['Coefs of '+measure]
                    data1[clas][measure]['count_timelines']+=1
            
            for measure in measures:
                data1[clas][measure]['average_coef']=data1[clas][measure]['average_coef']/float(data1[clas][measure]['count_timelines'])
                         
    
        with open('recalc_non_dropped_coefs.json','w') as outfile:
            json.dump(data1,outfile)  
    
    '''
    method which creates json for all non_dropped classes with the number of the releases that the class has changed
    and the total number of releases that the class has appeared
    '''
    def create_json_changes(self):
        
        change_folder('Results_Classes_'+NonDroppedData.project)
        
        with open("timelines_releases.json",'r')as handle:
            releases=json.load(handle)
        
        with open('recalc_non_dropped_data.json','r')as handle:
            recalc_data=json.load(handle)
            
        with open("classes_data_measures_non_dropped.json",'r')as handle:
            non_dropped_data=json.load(handle)
        
        measures=NonDroppedData.measures
        
        string='timeline'
        data={}
        for clas in recalc_data:
            
            data[clas]={}
            data[clas]['changes']=0
            data[clas]['total']=-1
            
            for count in range(0,len(releases)):
                
                timeline='timeline'+str(count+1)
                if timeline in recalc_data[clas]:
                    data[clas]['changes']+=(len(recalc_data[clas][timeline]['Metrics '+measures[0]])-1)
                    data[clas]['total']+=len(non_dropped_data[clas][timeline]["Metrics "+measures[0]])
                    
                prev_timeline='timeline'+str(count)
                
                if count>0 and timeline in recalc_data[clas] and prev_timeline in recalc_data[clas]:
                    
                    flag=False
                    for measure in measures:
                        if  recalc_data[clas][timeline]['Metrics '+measure][0]!=recalc_data[clas][prev_timeline]['Metrics '+measure][-1]:
                            flag=True
                    
                    if flag==True:
                        data[clas]['changes']+=1
        
        with open("changes_non_dropped.json",'w')as outfile:
            json.dump(data,outfile)
        
    '''
    method which create json for non dropped classes with start timeline, end timeline that they appeared
    '''
    def create_json_limits(self):
        
        move_initial_folder()
        
        change_folder('Results_Classes_'+NonDroppedData.project)
        
        with open('classes_data_measures_non_dropped.json','r')as handle:
            parsed= json.load(handle)
            
        
        with open('timelines_releases.json','r')as handle:
            minors=json.load(handle)
        
        non_dropped_limits={}
        
        timelines=[]
        
        for x in range(0,len(minors)):
            timeline='timeline'+str(x+1)
            timelines.append(timeline)
            
        
        for clas in parsed:
            maxtimeline=-1
            mintimeline=1000
            for timeline in parsed[clas]:
                num_timel=int(timeline[-1])-1
                if num_timel>maxtimeline:
                    maxtimeline=num_timel
                if num_timel<mintimeline:
                    mintimeline=num_timel
            non_dropped_limits[clas]=[timelines[mintimeline],timelines[maxtimeline]]
            

    
        with open("non_dropped_classes_start_stop.json","w")as outfile:
            json.dump(non_dropped_limits,outfile)