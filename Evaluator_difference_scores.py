from System_non_maintainability.DifferenceScore import *

def Evaluator_dif_scores():
    
    
    projects=[]
        
    projects.append('apache_struts')
    projects.append('spring-projects_spring-framework')
    projects.append('hibernate_hibernate-orm')
    
    
    for project in projects:
        difference_score=Diferrence_Score(project)
        difference_score.produce_average_measures_of_methods()
    difference_score.plots_histograms_diference_score_dropped()
    
Evaluator_dif_scores()