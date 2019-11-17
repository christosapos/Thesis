from System_non_maintainability.Folders import *
from System_non_maintainability.Releases import *
import pandas as pd
import json
import matplotlib.pyplot as plt
import sys
string='ccis-java-evaluation-modelling-master'
sys.path.insert(0,string)
from evaluator import Evaluator
import numpy as np

class Diferrence_Score():
    
    
    project=''
    
    
    def __init__(self,project):
        Diferrence_Score.project=project
    
    '''
    produce_average_measures_of_methods method that produces a json with the average values
    of given measures for methods for every release.
    '''
    def produce_average_measures_of_methods(self):
        
        move_initial_folder()
        
        endwith="-Method.csv"
        
        releases2=Releases(endwith,Diferrence_Score.project)
        releases2.produce_paths()
        
        releases2.state_minors()
                
        
        data={}
        measures=[]
        measures.append("McCC")
        measures.append("NUMPAR")
        count1=0
        
        print("Produce average measures of methods")
        for minor in releases2.Minors:
            for release in releases2.Minors[minor]:
                
                data[release]={}
                count1+=1
                print("I am in release",count1,release)
                dfmeas=[]
                dfdub=pd.read_csv(release,usecols=["LongName"]+measures)
                df=dfdub.drop_duplicates('LongName') # remove all dublicates methods 
                df1=df.loc[:,"LongName"] 
                df1=df1.reset_index(drop=True)
                for k in range(0,len(measures)):
                    dfmeas.append([])
                    dfmeas[k]=df.loc[:,measures[k]]
                    dfmeas[k]=dfmeas[k].reset_index(drop=True)
            
                for q in range(0,len(df1)):
                    method=df1[q]
                    L=[]
                    L=method.rsplit(".",1)
                    if L[0] not in data[release]:
                        data[release][L[0]]={}
                    for t in  range(0,len(measures)):
                        val_meas=dfmeas[t][q]
                        
                        if measures[t] not in data[release][L[0]]:
                            data[release][L[0]][measures[t]]=[]
                            data[release][L[0]][measures[t]].append(0)
                            data[release][L[0]][measures[t]].append(0)
                        
                        data[release][L[0]][measures[t]][0]+=val_meas
                        data[release][L[0]][measures[t]][1]+=1.0
                
                for clas in data[release]:
                    for measure in data[release][clas]:
                        data[release][clas][measure][0]=data[release][clas][measure][0]/data[release][clas][measure][1]
    
        change_folder('Results_Classes_'+Diferrence_Score.project)
        
        with open('average_measures_of_methods.json','w') as outfile:
            json.dump(data,outfile)
    
    
    '''
    plots_histograms_diference_score_dropped method that produces plots for every category of measures
    Every plot contains all the differences(first appearance to last appearance) of the scores of
    all dropped classes.Creates a barplot for all categories based on the signs of the diferrences scores.
    Also creates for all category of measures distributions of start scores and last scores of dropped classes.
    '''    
    def plots_histograms_diference_score_dropped(self):
        
        
        projects=[]
        
        projects.append('apache_struts')
        projects.append('spring-projects_spring-framework')
        projects.append('hibernate_hibernate-orm')
        
        #change_folder('Results_Classes_'+Diferrence_Score.project)
        
        measures=[]
        #complexity metrics
        measures.append('WMC')
        #measures.append('McCC') 
        measures.append('NL')
        #coupling metrics
        measures.append('NII')
        measures.append('RFC')
        measures.append('CBO')
        #documentation metrics
        measures.append('TCD')
        measures.append('DLOC')
        measures.append('TCLOC')
        #inheritance metrics
        measures.append('DIT')
        measures.append('NOC')
        #size metrics
        #measures.append('NUMPAR')
        measures.append('TNG')
        measures.append('TNA')
        measures.append('NPA')
        measures.append('TLLOC')
        measures.append('TNLS')
        
        info1=[]
        info2=[]
        
        
        for project in projects:
            
            change_folder("Results_Classes_"+project)
            
            with open('dropped_classes_start_stop.json','r')as handle:
                dropped=json.load(handle)
            
            with open("recalc_dropped_data.json",'r')as handle:
                parsed=json.load(handle)
            
            with open('average_measures_of_methods.json','r')as handle:
                parsed1=json.load(handle)

            with open('timelines_releases_b.json','r')as handle:
                parsed2=json.load(handle)
            
            with open("anomalies.json","r")as handle:
                anomalies=json.load(handle)
            
            with open("filter_classes.json",'r')as handle:
                filter=json.load(handle)
            
            with open("short_life_classes.json",'r')as handle:
                short_life=json.load(handle)
                
        
            for clas in dropped:
                
                if clas in filter and clas not in short_life and clas not in anomalies:
                    
            
                    metrics1={}
                    metrics2={}
                    point1=dropped[clas][0]
                    point2=dropped[clas][1]
                    point3=dropped[clas][2]
                    point4=dropped[clas][3]
                    
                    release1=parsed2[point1][point2][0]
                    T=release1.rsplit("-",1)
                    release1=T[0]+'-Method.csv'
                    
                    release2=parsed2[point3][point4][0]
                    T=release2.rsplit("-",1)
                    release2=T[0]+'-Method.csv'
                    
                    if clas in parsed1[release1] and clas in parsed1[release2]:
                        string="Metrics "
                        for measure in measures:
                            metrics1[measure]=parsed[clas][point1][string+measure][0]
                            metrics2[measure]=parsed[clas][point3][string+measure][-1]
                            
                        for measure in parsed1[release1][clas]:
                            metrics1[measure]=parsed1[release1][clas][measure][0]
                        
                        for measure in parsed1[release2][clas]:
                            metrics2[measure]=parsed1[release2][clas][measure][0]
                        
                        info1.append(metrics1)
                        info2.append(metrics2)
            
        
        move_initial_folder()
        change_folder('ccis-java-evaluation-modelling-master')
    
        evaluator1=Evaluator()
        
        r=[]
        k=[]
        info =[]
        info.append(info1)
        info.append(info2)
        
        
        metrics_category=[]
        metrics_category.append('complexity')
        metrics_category.append('coupling')
        metrics_category.append('documentation')
        metrics_category.append('inheritance')
        metrics_category.append('size')
        metrics_category.append('final_score')
        
        for q in range(0,len(info)):
            r.append([])
            r[q].append(evaluator1.evaluate_complexity(info[q], 'Class')[0])
            r[q].append(evaluator1.evaluate_coupling(info[q],'Class')[0])
            r[q].append(evaluator1.evaluate_documentation(info[q],'Class')[0])
            r[q].append(evaluator1.evaluate_inheritance(info[q],'Class')[0])
            r[q].append(evaluator1.evaluate_size(info[q],'Class')[0])
            r[q].append(evaluator1.evaluate_all_properies(info[q],'Class'))
            k.append([])
            k[q].append(r[q][0].loc[:,"complexity_score"])
            k[q].append(r[q][1].loc[:,"coupling_score"])
            k[q].append(r[q][2].loc[:,"documentation_score"])
            k[q].append(r[q][3].loc[:,"inheritance_score"])
            k[q].append(r[q][4].loc[:,"size_score"])
            k[q].append(r[q][5].loc[:,"final_score"])

        
        L=[]
        for t in range(0,len(k[0])):
            L.append([]) 
            for q in range(0,len(k[0][t])):
                L[t].append(k[0][t][q]-k[1][t][q]) 
        
        
        change_folder("Evaluator")
        
        for t in range(0,len(L)):
            plt.plot(L[t],'ro')
            plt.xlabel('classes')
            plt.ylabel("difference_values_"+metrics_category[t])
            plt.savefig('plot_'+metrics_category[t])
            plt.clf()
        
        for t in range(0,len(L)):
            
            A=[]
            A.append(0)
            A.append(0)
            A.append(0)
        
            for val in L[t]:
                if val>0:
                    A[0]+=1
                elif val<0:
                    A[1]+=1
                else:
                    A[2]+=1

            
            objects=("Negative_distance","Zero_distance","Positive_distance")
            y_pos = np.arange(len(objects))
            sum1=A[0]+A[1]+A[2]
            performance = [A[1]/sum1,A[2]/sum1,A[0]/sum1]
            plt.bar(y_pos, performance, align='center', alpha=0.5)
            plt.xticks(y_pos, objects)
            plt.title("Percentage of differences scores :"+metrics_category[t])
            plt.ylim(0,1.0)
            plt.savefig("Barplot_difference_score_"+metrics_category[t])
            plt.clf()
            
            
    
        for t in range(0,len(L)):
            plt.hist(k[1][t],weights=np.ones(len(k[1][t]))/len(k[1][t]),bins=10)
                     
            plt.ylabel('Probability')
            plt.ylim(0,1.0)
            plt.savefig('histogram_final_scores_'+metrics_category[t])
            plt.clf()
        
        
        for t in range(0,len(L)):
            plt.hist(k[0][t],density=True,bins=10)
            plt.ylabel('Probability')
            plt.savefig('histogram_start_scores_'+metrics_category[t])
            plt.clf()
        
            
            