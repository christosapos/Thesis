import time
import json
from System_non_maintainability.Measures import *
from System_non_maintainability.Folders import *
from System_non_maintainability.Releases import *
from System_non_maintainability.Classes_Data import *
from System_non_maintainability.Dropped_Data import *
from System_non_maintainability.Non_Dropped_Data import *

def Life_Cycle_Analyzer():
    
    endwith="-Class.csv"
    
    projects=[]
    projects.append('apache_struts')
    projects.append('spring-projects_spring-framework')
    projects.append('hibernate_hibernate-orm')
    
    measures=return_measures()
    
    for project in projects:
        
        
        releases=Releases(endwith,project)
        releases.produce_paths()
        releases.state_minors()
        releases.produce_timelines_json()
        
        
        classesData=ClassesData(measures,project)
        
        classesData.seperate_dropped_non_dropped()
        classesData.produce_json('dropped')
        classesData.produce_json('non_dropped')
        
        droppedData=DroppedData(measures,project)
        droppedData.create_json_limits()
        droppedData.recalculate_coefs_dropped()
        droppedData.create_coefs_between_timelines()
        droppedData.final_coefs_dropped()
        
        droppedData.create_json_changes()
        
        droppedData.create_json_short_life()
        droppedData.create_json_anomalies()
        droppedData.create_json_pos_coefs()
        
        nondroppedData=NonDroppedData(measures,project)
    
        nondroppedData.create_json_limits()
        nondroppedData.create_recalculated_data()
        nondroppedData.create_json_changes()
        nondroppedData.create_coefs_between_timelines()
        nondroppedData.final_coefs_non_dropped()
        
             
    
    
    print("I am done")
Life_Cycle_Analyzer()