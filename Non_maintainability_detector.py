from System_non_maintainability.Merge_Data import *
from System_non_maintainability.Measures import *

def Non_maintainability_detector():
    
    measures=return_measures()
    
    projects=[]
        
    projects.append('apache_struts')
    projects.append('spring-projects_spring-framework')
    projects.append('hibernate_hibernate-orm')
    
    mergeData=MergeData(measures)
    
    mergeData.plot_distribution_changes(projects)
    mergeData.find_last_appear()
    mergeData.plot_distribution_last_appear()
    
    mergeData.create_model_data() 
    mergeData.create_multiple_candidate_models()
   
    mergeData.create_dropped_target_data() 
    mergeData.create_non_dropped_target_data() 
    
    mergeData.print_prediction_multiple_models()
    
    mergeData.create_final_models() 
    mergeData.create_distribution_scores_dropped()
    mergeData.create_distribution_scores_non_dropped()
    
    mergeData.create_csv_data_dropped(projects)
    mergeData.create_csv_data_non_dropped(projects)
    
    mergeData.create_histogram_percentage_faults()
    mergeData.create_bar_plots_min_faults()
    mergeData.barplot_predict_percentage_model()
    mergeData.distribution_total_scores()
    mergeData.distribution_final_scores()
    
    print("I am done")
    
Non_maintainability_detector()
    