import os
from natsort import natsorted
import re
from System_non_maintainability.Folders import *
import json

class Releases:
    endwith="" #sufix of the files which contains the metrics of the releases  
    project="" #Name of the project
    paths=[] #All sorted paths of the releases
    Minors=[] #Groups of minor releases
    
    def __init__(self,endwith,project):
        Releases.endwith=endwith
        Releases.project=project
        
    # produce_paths method that return a list with all the sorted paths of the releases that end with the given endwith "-Class.csv" or "-Method.csv"
    def produce_paths(self):
        result=[]
        project_path=os.path.join(os.getcwd(),Releases.project)
        for root,dirs,files in os.walk(project_path):
            for file in files:
                if file.endswith(Releases.endwith):
                    result.append(os.path.join(root,file))
        
        Releases.paths=natsorted(result)
    
        
    #method which produce a json with all the timelines and their corresponding releases
    def produce_timelines_json(self):
        #create a folder with the name Results-project if does not exist to put inside the json
        change_folder('Results_Classes_'+Releases.project)
        
        data={}
        string='timeline'
        for k in range(0,len(Releases.Minors)):
            string1=string+str(k+1)
            data[string1]=[]
            for q in range(0,len(Releases.Minors[k])):
                path=Releases.Minors[k][q]
                i=re.findall('\d+',path)
                i1=i[0] #first digit of the path
                i2=i[1] #second digit of the path
                if len(i)>2:
                    i3=i[2]
                
                a=int(i1+i2+i3)
                b=int(i1+i2)
                data[string1].append([Releases.Minors[k][q],a,b])
        with open('timelines_releases.json','w') as outfile:
            json.dump(data,outfile)
    
    #method which state in which timeline belongs every path 
    def state_minors(self):

        if(Releases.project=='apache_struts'):
            minors_endwith=Releases.project1_minors(self)
        if(Releases.project=='spring-projects_spring-framework'):
            minors_endwith=Releases.project2_minors(self)
        if(Releases.project=='hibernate_hibernate-orm'):
            minors_endwith=Releases.project3_minors(self)

        Minors={}
        for timeline in minors_endwith:

            Minors[timeline]=[]
            
            for endwith in minors_endwith[timeline]:
            
                for path in Releases.paths:
                    
                    if path.endswith(endwith+Releases.endwith):
                        Minors[timeline].append(path)
        Releases.Minors=Minors
    
    #method which states tags of project apache_struts        
    def project1_minors(self): #apache_struts
        
        minors={}
        minors[0]=[]
        
        minors[0].append("STRUTS_2_0_0")
        minors[0].append("STRUTS_2_0_1")
        minors[0].append("STRUTS_2_0_2")
        minors[0].append("STRUTS_2_0_3")
        minors[0].append("STRUTS_2_0_4")
        minors[0].append("STRUTS_2_0_5")
        minors[0].append("STRUTS_2_0_6")
        minors[0].append("STRUTS_2_0_7")
        minors[0].append("STRUTS_2_0_8")
        minors[0].append("STRUTS_2_0_9")
        minors[0].append("STRUTS_2_0_10")
        minors[0].append("STRUTS_2_0_11")
        minors[0].append("STRUTS_2_0_11_1")
        minors[0].append("STRUTS_2_0_11_2")
        minors[0].append("STRUTS_2_0_12")
        minors[0].append("STRUTS_2_0_13")
        minors[0].append("STRUTS_2_0_14")
        minors[0].append("STRUTS_2_0_X")
        
        minors[1]=[]
        minors[1].append("STRUTS_2_1_0")
        minors[1].append("STRUTS_2_1_1")
        minors[1].append("STRUTS_2_1_2")
        minors[1].append("STRUTS_2_1_3")
        minors[1].append("STRUTS_2_1_4")
        minors[1].append("STRUTS_2_1_5")
        minors[1].append("STRUTS_2_1_6")
        minors[1].append("STRUTS_2_1_7")
        minors[1].append("STRUTS_2_1_8")
        minors[1].append("STRUTS_2_1_8_1")
        
        minors[2]=[]
        minors[2].append("STRUTS_2_2_0")
        minors[2].append("STRUTS_2_2_1")
        minors[2].append("STRUTS_2_2_1_1")
        minors[2].append("STRUTS_2_2_2")
        minors[2].append("STRUTS_2_2_3")
        minors[2].append("STRUTS_2_2_3_1")
    
        minors[3]=[]
        minors[3].append("STRUTS_2_3_1")
        minors[3].append("STRUTS_2_3_1_1")
        minors[3].append("STRUTS_2_3_1_2")
        minors[3].append("STRUTS_2_3_2")
        minors[3].append("STRUTS_2_3_3")
        minors[3].append("STRUTS_2_3_4")
        minors[3].append("STRUTS_2_3_4_1")
        minors[3].append("STRUTS_2_3_5")
        minors[3].append("STRUTS_2_3_6")
        minors[3].append("STRUTS_2_3_7")
        minors[3].append("STRUTS_2_3_8")
        minors[3].append("STRUTS_2_3_9")
        minors[3].append("STRUTS_2_3_10")
        minors[3].append("STRUTS_2_3_11")
        minors[3].append("STRUTS_2_3_12")
        minors[3].append("STRUTS_2_3_13")
        minors[3].append("STRUTS_2_3_14")
        minors[3].append("STRUTS_2_3_14_1")
        minors[3].append("STRUTS_2_3_14_2")
        minors[3].append("STRUTS_2_3_14_3")
        minors[3].append("STRUTS_2_3_15")
        minors[3].append("STRUTS_2_3_15_1")
        minors[3].append("STRUTS_2_3_15_2")
        minors[3].append("STRUTS_2_3_15_3")
        minors[3].append("STRUTS_2_3_16")
        minors[3].append("STRUTS_2_3_16_1")
        minors[3].append("STRUTS_2_3_16_2")
        minors[3].append("STRUTS_2_3_16_3")
        minors[3].append("STRUTS_2_3_17")
        minors[3].append("STRUTS_2_3_19")
        minors[3].append("STRUTS_2_3_20")
        minors[3].append("STRUTS_2_3_20_1")
        minors[3].append("STRUTS_2_3_20_2")
        minors[3].append("STRUTS_2_3_20_3")
        minors[3].append("STRUTS_2_3_21")
        minors[3].append("STRUTS_2_3_22")
        minors[3].append("STRUTS_2_3_23")
        minors[3].append("STRUTS_2_3_24")
        minors[3].append("STRUTS_2_3_24_1")
        minors[3].append("STRUTS_2_3_24_2")
        minors[3].append("STRUTS_2_3_24_3")
        minors[3].append("STRUTS_2_3_25")
        minors[3].append("STRUTS_2_3_26")
        minors[3].append("STRUTS_2_3_27")
        minors[3].append("STRUTS_2_3_28")
        minors[3].append("STRUTS_2_3_28_1")
        minors[3].append("STRUTS_2_3_29")
        minors[3].append("STRUTS_2_3_30")
        minors[3].append("STRUTS_2_3_31")
        minors[3].append("STRUTS_2_3_32")
        minors[3].append("STRUTS_2_3_33")
        minors[3].append("STRUTS_2_3_34")
        
        minors[4]=[]
        minors[4].append("STRUTS_2_5_BETA1")
        minors[4].append("STRUTS_2_5_BETA2")
        minors[4].append("STRUTS_2_5_BETA3")
        minors[4].append("STRUTS_2_5")
        minors[4].append("STRUTS_2_5_1")
        minors[4].append("STRUTS_2_5_2")
        minors[4].append("STRUTS_2_5_3")
        minors[4].append("STRUTS_2_5_4")
        minors[4].append("STRUTS_2_5_5")
        minors[4].append("STRUTS_2_5_6")
        minors[4].append("STRUTS_2_5_7")
        minors[4].append("STRUTS_2_5_8")
        minors[4].append("STRUTS_2_5_9")
        minors[4].append("STRUTS_2_5_10")
        minors[4].append("STRUTS_2_5_10_1")
        minors[4].append("STRUTS_2_5_11")
        minors[4].append("STRUTS_2_5_12")
        minors[4].append("STRUTS_2_5_13")
        minors[4].append("STRUTS_2_5_14")
        minors[4].append("STRUTS_2_5_14_1")
        minors[4].append("STRUTS_2_5_15")
        minors[4].append("STRUTS_2_5_16")
        
        return minors
    
    
    #method which states tags of project spring_framework 
    def project2_minors(self): 
        
        minors={}
        minors[0]=[]
        minors[0].append("v3.0.0.M1")
        minors[0].append("v3.0.0.M2")
        minors[0].append("v3.0.0.M3")
        minors[0].append("v3.0.0.M4")
        minors[0].append("v3.0.0.RC1")
        minors[0].append("v3.0.0.RC2")
        minors[0].append("v3.0.0.RC3")
        minors[0].append("v3.0.0.RELEASE")
        minors[0].append("v3.0.1.RELEASE")
        minors[0].append("v3.0.1.RELEASE-A")
        minors[0].append("v3.0.1.RELEASE.A")
        minors[0].append("v3.0.2.RELEASE")
        minors[0].append("v3.0.3.RELEASE")
        minors[0].append("v3.0.4.RELEASE")
        minors[0].append("v3.0.5.RELEASE")
        minors[0].append("v3.0.6.RELEASE")
        minors[0].append("v3.0.7.RELEASE")
        
        minors[1]=[]
        minors[1].append("v3.1.0.M1")
        minors[1].append("v3.1.0.M2")
        minors[1].append("v3.1.0.RC1")
        minors[1].append("v3.1.0.RC2")
        minors[1].append("v3.1.0.RELEASE")   
        minors[1].append("v3.1.1.RELEASE")
        minors[1].append("v3.1.2.RELEASE")
        minors[1].append("v3.1.3.RELEASE")
        minors[1].append("v3.1.4.RELEASE")
        
        minors[2]=[]
        minors[2].append("v3.2.0.M1")
        minors[2].append("v3.2.0.M2")
        minors[2].append("v3.2.0.RC1")
        minors[2].append("v3.2.0.RC2-A")
        minors[2].append("v3.2.0.RC2")
        minors[2].append("v3.2.0.RELEASE")
        minors[2].append("v3.2.1.RELEASE")
        minors[2].append("v3.2.2.RELEASE")
        minors[2].append("v3.2.3.RELEASE")
        minors[2].append("v3.2.4.RELEASE")
        minors[2].append("v3.2.5.RELEASE")
        minors[2].append("v3.2.6.RELEASE")
        minors[2].append("v3.2.7.RELEASE")
        minors[2].append("v3.2.8.RELEASE")
        minors[2].append("v3.2.9.RELEASE")
        minors[2].append("v3.2.10.RELEASE")
        minors[2].append("v3.2.11.RELEASE")
        minors[2].append("v3.2.12.RELEASE")
        minors[2].append("v3.2.13.RELEASE")
        minors[2].append("v3.2.14.RELEASE")
        minors[2].append("v3.2.15.RELEASE")
        minors[2].append("v3.2.16.RELEASE")
        minors[2].append("v3.2.17.RELEASE")
        minors[2].append("v3.2.18.RELEASE")
    
    
        minors[3]=[]
        minors[3].append("v4.0.0.M1")
        minors[3].append("v4.0.0.M2")
        minors[3].append("v4.0.0.M3")
        minors[3].append("v4.0.0.RC1")
        minors[3].append("v4.0.0.RC2")
        minors[3].append("v4.0.0.RELEASE")
        minors[3].append("v4.0.1.RELEASE")
        minors[3].append("v4.0.2.RELEASE")
        minors[3].append("v4.0.3.RELEASE")
        minors[3].append("v4.0.4.RELEASE")
        minors[3].append("v4.0.5.RELEASE")
        minors[3].append("v4.0.6.RELEASE")
        minors[3].append("v4.0.7.RELEASE")
        minors[3].append("v4.0.8.RELEASE")
        minors[3].append("v4.0.9.RELEASE")
        
        minors[4]=[]
        minors[4].append("v4.1.0.RC1")
        minors[4].append("v4.1.0.RC2")
        minors[4].append("v4.1.0.RELEASE")
        minors[4].append("v4.1.1.RELEASE")
        minors[4].append("v4.1.2.RELEASE")
        minors[4].append("v4.1.3.RELEASE")
        minors[4].append("v4.1.4.RELEASE")
        minors[4].append("v4.1.5.RELEASE")
        minors[4].append("v4.1.6.RELEASE")
        minors[4].append("v4.1.7.RELEASE")
        minors[4].append("v4.1.8.RELEASE")
        minors[4].append("v4.1.9.RELEASE")
        
        minors[5]=[]
        minors[5].append("v4.2.0.RC1")
        minors[5].append("v4.2.0.RC2")
        minors[5].append("v4.2.0.RC3")
        minors[5].append("v4.2.0.RELEASE")
        minors[5].append("v4.2.1.RELEASE")
        minors[5].append("v4.2.2.RELEASE")
        minors[5].append("v4.2.3.RELEASE")
        minors[5].append("v4.2.4.RELEASE")
        minors[5].append("v4.2.5.RELEASE")
        minors[5].append("v4.2.6.RELEASE")
        minors[5].append("v4.2.7.RELEASE")
        minors[5].append("v4.2.8.RELEASE")
        minors[5].append("v4.2.9.RELEASE")
        
        minors[6]=[]
        minors[6].append("v4.3.0.RC1")
        minors[6].append("v4.3.0.RC2")
        minors[6].append("v4.3.0.RELEASE")
        minors[6].append("v4.3.1.RELEASE")
        minors[6].append("v4.3.2.RELEASE")
        minors[6].append("v4.3.3.RELEASE")
        minors[6].append("v4.3.4.RELEASE")
        minors[6].append("v4.3.5.RELEASE")
        minors[6].append("v4.3.6.RELEASE")
        minors[6].append("v4.3.7.RELEASE")
        minors[6].append("v4.3.8.RELEASE")
        minors[6].append("v4.3.9.RELEASE")
        minors[6].append("v4.3.10.RELEASE")
        minors[6].append("v4.3.11.RELEASE")
        minors[6].append("v4.3.12.RELEASE")
        minors[6].append("v4.3.13.RELEASE")
        minors[6].append("v4.3.14.RELEASE")
        
        minors[7]=[]
        minors[7].append("v5.0.0.M1")
        minors[7].append("v5.0.0.M2")
        minors[7].append("v5.0.0.M3")
        minors[7].append("v5.0.0.M4")
        minors[7].append("v5.0.0.M5")
        minors[7].append("v5.0.0.RC1")
        minors[7].append("v5.0.0.RC2")
        minors[7].append("v5.0.0.RC3")
        minors[7].append("v5.0.0.RC4")
        minors[7].append("v5.0.0.RELEASE")
        minors[7].append("v5.0.1.RELEASE")
        minors[7].append("v5.0.2.RELEASE")
        minors[7].append("v5.0.3.RELEASE")
        
        return minors
        
    #method which states tags of project hibernate
    def project3_minors(self): 
        
        minors={}
        minors[0]=[]
        minors[0].append("3.6.0.Beta1")
        minors[0].append("3.6.0.Beta2")
        minors[0].append("3.6.0.Beta3")
        minors[0].append("3.6.0.Beta4")
        minors[0].append("3.6.0.CR1")
        minors[0].append("3.6.0.CR2")
        minors[0].append("3.6.0.Final")
        minors[0].append("3.6.1.Final")
        minors[0].append("3.6.2.Final")
        minors[0].append("3.6.3.Final")
        minors[0].append("3.6.4.Final")
        minors[0].append("3.6.5.Final")
        minors[0].append("3.6.6.Final")
        minors[0].append("3.6.7.Final")
        minors[0].append("3.6.8.Final")
        minors[0].append("3.6.9.Final")
        minors[0].append("3.6.10.Final")
        
        minors[1]=[]
        minors[1].append("4.0.0.Alpha1")
        minors[1].append("4.0.0.Alpha2")
        minors[1].append("4.0.0.Alpha3")
        minors[1].append("4.0.0.Beta1")
        minors[1].append("4.0.0.Beta2")
        minors[1].append("4.0.0.Beta3")
        minors[1].append("4.0.0.Beta4")
        minors[1].append("4.0.0.Beta5")
        minors[1].append("4.0.0.CR1")
        minors[1].append("4.0.0.CR2")
        minors[1].append("4.0.0.CR3")
        minors[1].append("4.0.0.CR4")
        minors[1].append("4.0.0.CR5")
        minors[1].append("4.0.0.CR6")
        minors[1].append("4.0.0.CR7")
        minors[1].append("4.0.0.Final")
        minors[1].append("4.0.1")
        
        minors[2]=[]
        minors[2].append("4.1.0.Final")
        minors[2].append("4.1.1")
        minors[2].append("4.1.2")
        minors[2].append("4.1.2.Final")
        minors[2].append("4.1.3.Final")
        minors[2].append("4.1.4.Final")
        minors[2].append("4.1.5.Final")
        minors[2].append("4.1.5.SP1")
        minors[2].append("4.1.6.Final")
        minors[2].append("4.1.7.Final")
        minors[2].append("4.1.8.Final")
        minors[2].append("4.1.9.Final")
        minors[2].append("4.1.10.Final")
        minors[2].append("4.1.11.Final")
        minors[2].append("4.1.12.Final")
        
        minors[3]=[]
        minors[3].append("4.2.0.CR1")
        minors[3].append("4.2.0.CR2")
        minors[3].append("4.2.0.Final")
        minors[3].append("4.2.1.Final")
        minors[3].append("4.2.2.Final")
        minors[3].append("4.2.3.Final")
        minors[3].append("4.2.0.SP1")
        minors[3].append("4.2.4.Final")
        minors[3].append("4.2.5.Final")
        minors[3].append("4.2.6.Final")
        minors[3].append("4.2.7.Final")
        minors[3].append("4.2.7.SP1")
        minors[3].append("4.2.8.Final")
        minors[3].append("4.2.9.Final")
        minors[3].append("4.2.10.Final")
        minors[3].append("4.2.11.Final")
        minors[3].append("4.2.12.Final")
        minors[3].append("4.2.13.Final")
        minors[3].append("4.2.14.Final")
        minors[3].append("4.2.15.Final")
        minors[3].append("4.2.16.Final")
        minors[3].append("4.2.17.Final")
        minors[3].append("4.2.18.Final")
        minors[3].append("4.2.19.Final")
        minors[3].append("4.2.20.Final")
        minors[3].append("4.2.21.Final")
        minors[3].append("4.2.22.Final")
        minors[3].append("4.2.23.Final")
        minors[3].append("4.2.24.Final")
        minors[3].append("4.2.25.Final")
        minors[3].append("4.2.26.Final")
        minors[3].append("4.2.27.Final")
        
        minors[4]=[]
        minors[4].append("4.3.0.Beta1")
        minors[4].append("4.3.0.Beta2")
        minors[4].append("4.3.0.Beta3")
        minors[4].append("4.3.0.Beta4")
        minors[4].append("4.3.0.Beta5")
        minors[4].append("4.3.0.CR1")
        minors[4].append("4.3.0.CR2")
        minors[4].append("4.3.0.Final")
        minors[4].append("4.3.1.Final")
        minors[4].append("4.3.2.Final")
        minors[4].append("4.3.3.Final")
        minors[4].append("4.3.4.Final")
        minors[4].append("4.3.5.Final")
        minors[4].append("4.3.6.Final")
        minors[4].append("4.3.7.Final")
        minors[4].append("4.3.8.Final")
        minors[4].append("4.3.9.Final")
        minors[4].append("4.3.10.Final")
        minors[4].append("4.3.11.Final")
        
        minors[5]=[]
        minors[5].append("5.0.0.Beta1")
        minors[5].append("5.0.0.Beta2")
        minors[5].append("5.0.0.CR1")
        minors[5].append("5.0.0.CR2")
        minors[5].append("5.0.0.CR3")
        minors[5].append("5.0.0.CR4")
        minors[5].append("5.0.0.Final")
        minors[5].append("5.0.1.Final")
        minors[5].append("5.0.2.Final")
        minors[5].append("5.0.3")
        minors[5].append("5.0.4")
        minors[5].append("5.0.5")
        minors[5].append("5.0.6")
        minors[5].append("5.0.7")
        minors[5].append("5.0.8")
        minors[5].append("5.0.9")
        minors[5].append("5.0.10")
        minors[5].append("5.0.11")
        minors[5].append("5.0.12")
        minors[5].append("5.0.13")
        minors[5].append("5.0.14")
        minors[5].append("5.0.15")
        minors[5].append("5.0.16")
        
        minors[6]=[]
        minors[6].append("5.1.0")
        minors[6].append("5.1.1")
        minors[6].append("5.1.2")
        minors[6].append("5.1.3")
        minors[6].append("5.1.4")
        minors[6].append("5.1.5")
        minors[6].append("5.1.6")
        minors[6].append("5.1.7")
        minors[6].append("5.1.8")
        minors[6].append("5.1.9")
        minors[6].append("5.1.10")
        minors[6].append("5.1.11")
        minors[6].append("5.1.12")
        minors[6].append("5.1.13")
        
        minors[7]=[]
        minors[7].append("5.2.0")
        minors[7].append("5.2.1")
        minors[7].append("5.2.2")
        minors[7].append("5.2.3")
        minors[7].append("5.2.4")
        minors[7].append("5.2.5")
        minors[7].append("5.2.6")
        minors[7].append("5.2.7")
        minors[7].append("5.2.8")
        minors[7].append("5.2.9") 
        minors[7].append("5.2.10")
        minors[7].append("5.2.11")
        minors[7].append("5.2.12")
        minors[7].append("5.2.13")
        minors[7].append("5.2.14")
        minors[7].append("5.2.15")
        minors[7].append("5.2.16")
        
        minors[8]=[]
        minors[8].append("5.3.0.Beta1")
        minors[8].append("5.3.0.Beta2")
    
    
        return minors