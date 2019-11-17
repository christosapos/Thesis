from System_non_maintainability.Folders import *
import json
import matplotlib.pyplot as plt 
import numpy as np
from sklearn import linear_model

class DroppedData:
    
    project=''
    measures=[]
    
    def __init__(self,measures,project):
        DroppedData.measures=measures
        DroppedData.project=project
    
    #method which create coefs of linear regression  between timelines and saves them in a .json
    def create_coefs_between_timelines(self):
        
        change_folder('Results_Classes_'+DroppedData.project)
        
        with open("recalc_dropped_data.json",'r')as handle:
            recalc_data=json.load(handle)
        
        with open("timelines_releases.json",'r')as handle:
            timelines=json.load(handle)
        
        measures=DroppedData.measures
        
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
        
        with open("coefs_between_timelines_dropped.json",'w')as outfile:
            json.dump(coefs_between_timelines,outfile)
    '''
    method which calculate final coef for all metrics based on coefs of timelines and between timelines coefs 
    '''
    def final_coefs_dropped(self):
        
        change_folder("Results_Classes_"+DroppedData.project)
        
        with open("recalc_dropped_coefs.json",'r')as handle:
            recalc_coefs=json.load(handle)
        
        with open("coefs_between_timelines_dropped.json",'r')as handle:
            coefs_between_time=json.load(handle)
        
        final_coefs={}
        measures=DroppedData.measures
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
        
        with open("final_coefs_dropped.json",'w')as outfile:
            json.dump(final_coefs,outfile)
    '''        
    method which recalculate coefs of timelines of linear regression based on the releases that classes change 
    also creates a json with the average of coefs of timelines           
    '''
    def recalculate_coefs_dropped(self):
        
        change_folder('Results_Classes_'+DroppedData.project)
        data={}
        
        with open("timelines_releases.json",'r')as handle:
            releases=json.load(handle)

        with open("classes_data_measures_dropped.json","r")as handle:
            dropped_data=json.load(handle)
        
        with open("dropped_classes_start_stop.json","r")as handle:
            dropped_limits=json.load(handle)
        
        measures=DroppedData.measures
        
        for clas in dropped_data:
            data[clas]={}
            for timeline in releases:
                if timeline in dropped_data[clas]:
                    data[clas][timeline]={}
                    string="Metrics "
                    length=len(dropped_data[clas][timeline][string+measures[0]])
                    for count in range(0,length):
                        flag=False
                        if count==0:
                            for measure in measures:
                                string1=string+measure
                                data[clas][timeline][string1]=[]
                                data[clas][timeline][string1].append(dropped_data[clas][timeline][string1][0])
                        else:
                            for measure in measures:
                                string1=string+measure
                                if dropped_data[clas][timeline][string1][count]!=data[clas][timeline][string1][-1]:
                                    flag=True
                            
                            if flag==True:
                                for measure in measures:
                                    string1=string+measure
                                    data[clas][timeline][string1].append(dropped_data[clas][timeline][string1][count])
        
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
        
        with open('recalc_dropped_data.json','w') as outfile:
            json.dump(data,outfile)       
        
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
                         
    
        with open('recalc_dropped_coefs.json','w') as outfile:
            json.dump(data1,outfile)
        
    '''
    method which create json for dropped classes with start timeline, start point,end timeline, end point
    '''
    def create_json_limits(self):
    
        move_initial_folder()
        change_folder('Results_Classes_'+DroppedData.project)
        
        with open('classes_data_measures_dropped.json','r')as handle:
            parsed= json.load(handle)
            
        
        with open('timelines_releases.json','r')as handle:
            minors=json.load(handle)
            
        print(len(parsed))
        dropped_limits={}
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
            if maxtimeline< (len(timelines)-1):
                dropped_limits[clas]=[timelines[mintimeline],parsed[clas][timelines[mintimeline]]['Start']]
                dropped_limits[clas].extend([timelines[maxtimeline],parsed[clas][timelines[maxtimeline]]['End']])
            else:
                if parsed[clas][timelines[maxtimeline]]['End']<(len(minors[timelines[maxtimeline]])-1):
                    dropped_limits[clas]=[timelines[mintimeline],parsed[clas][timelines[mintimeline]]['Start']]
                    dropped_limits[clas].extend([timelines[maxtimeline],parsed[clas][timelines[maxtimeline]]['End']])
        
        print(len(dropped_limits))
        with open("dropped_classes_start_stop.json","w")as outfile:
            json.dump(dropped_limits,outfile)
    
    '''
    method which creates json for all dropped classes with the number of the releases that the class has changed
    and the total number of releases that the class has appeared
    '''
    def create_json_changes(self):
        
        change_folder('Results_Classes_'+DroppedData.project)
        
        with open("timelines_releases.json",'r')as handle:
            releases=json.load(handle)
        
        with open('recalc_dropped_data.json','r')as handle:
            recalc_data=json.load(handle)
            
        with open("classes_data_measures_dropped.json",'r')as handle:
            dropped_data=json.load(handle)
        
        measures=DroppedData.measures
        
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
                    data[clas]['total']+=len(dropped_data[clas][timeline]["Metrics "+measures[0]])
                    
                prev_timeline='timeline'+str(count)
                
                if count>0 and timeline in recalc_data[clas] and prev_timeline in recalc_data[clas]:
                    
                    flag=False
                    for measure in measures:
                        if  recalc_data[clas][timeline]['Metrics '+measure][0]!=recalc_data[clas][prev_timeline]['Metrics '+measure][-1]:
                            flag=True
                    
                    if flag==True:
                        data[clas]['changes']+=1
        
        with open("changes_dropped.json",'w')as outfile:
            json.dump(data,outfile)

    '''
    method which creates json with dropped classes with life cycle less than 10 releases
    ''' 
    def create_json_short_life(self):
        
        change_folder("Results_Classes_"+DroppedData.project)
        
        with open("dropped_classes_start_stop.json",'r')as handle:
            dropped_limits=json.load(handle)
        
        with open("timelines_releases.json",'r')as handle:
            timelines_relea=json.load(handle)
            
        distances={}
        
        for clas in dropped_limits:
            
            distances[clas]=0
            
            stop=int(dropped_limits[clas][2][-1])
            start=int(dropped_limits[clas][0][-1])
            dif=stop-start+1
            if dropped_limits[clas][0]==dropped_limits[clas][2]:
                dist=dropped_limits[clas][3]-dropped_limits[clas][1]+1
        
            else:
                  
                dist=0
                for a in range(0,dif):
                    if a==0:
                        dist+=(len(timelines_relea['timeline'+str(start)])-dropped_limits[clas][1])
                    elif a==(dif-1):
                        dist+=dropped_limits[clas][3]+1
                    else:
                        dist+=len(timelines_relea['timeline'+str(start+a)])

            distances[clas]=dist
        
        short_lif_clas={}
        
        for clas in distances:
            if distances[clas]<=10:
                short_lif_clas[clas]={}
        
        with open('short_life_classes.json','w') as outfile:
            json.dump(short_lif_clas,outfile)
    '''
    method which creates json with dropped classes with at least on positive final coeff in one metric
    '''  
    def create_json_pos_coefs(self):
            
        filter={}
        
        measures=DroppedData.measures
        
        change_folder('Results_Classes_'+DroppedData.project)
         
        with open("final_coefs_dropped.json",'r')as handle:
            final_coefs=json.load(handle)   
            
        for measure in measures:
            
            for clas in final_coefs:
                if final_coefs[clas][measure]>0:
                    filter[clas]={}
        
        with open("filter_classes.json","w")as outfile:
            json.dump(filter,outfile)
    '''
    method which creates json with dropped classes where at least for one metric final coef does not follows
    start and end value
    ''' 
    def create_json_anomalies(self):
    
        anomalies={}
        
        change_folder("Results_Classes_"+DroppedData.project)
        
        with open("recalc_dropped_data.json",'r')as handle:
            recalc_data=json.load(handle)
        
        with open("final_coefs_dropped.json",'r')as handle:
            final_coefs=json.load(handle)
            
        with open("dropped_classes_start_stop.json",'r')as handle:
            limits=json.load(handle)
        
        measures=DroppedData.measures
                
        for clas in recalc_data:
            
                end_timeline=limits[clas][2]
                start_timeline=limits[clas][0]
                
                for measure in measures:
                    
                    start_value=recalc_data[clas][start_timeline]['Metrics '+measure][0]
                    end_value=recalc_data[clas][end_timeline]['Metrics '+measure][-1]
                    coef=final_coefs[clas][measure]
                
                    if end_value-start_value>0 and coef<=0 :
                        
                        if clas not in anomalies:
                            anomalies[clas]={}
                    if end_value-start_value==0 and coef!=0:
                        
                        if clas not in anomalies:
                            anomalies[clas]={}
                    if end_value-start_value<0 and coef>=0:
                        
                        
                        if clas not in anomalies:
                            anomalies[clas]={}
    
        with open('anomalies.json','w')as outfile:
            json.dump(anomalies,outfile)
                
                    
                    
                    