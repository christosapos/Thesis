
#method which returns values for every method which will be used as rules in training of non_maintainable models
def set_thresholds_measures(self):
        
        thresholds={}
        
        thresholds['LCOM5']=1
        
        thresholds['NL']=2
        thresholds['NLE']=2
        thresholds['WMC']=10
        
        thresholds['CBO']=10
        thresholds['CBOI']=4
        thresholds['NII']=6
        thresholds['NOI']=10
        thresholds['RFC']=20
        
        thresholds['DIT']=3
        thresholds['NOA']=4
        thresholds['NOC']=1
        thresholds['NOD']=1
        thresholds['NOP']=1
        
        thresholds['TCD']=0.03 #negative logic
        thresholds['DLOC']=2#negative logic
        thresholds['TCLOC']=2 #negative logic 
        
        thresholds['LLOC']=90
        thresholds['LOC']=90
        thresholds['NA']=7
        thresholds['NG']=6
        thresholds['NLA']=5
        thresholds['NLG']=3
        thresholds['NLM']=10
        thresholds['NLPA']=1
        thresholds['NLPM']=8
        thresholds['NLS']=2
        thresholds['NM']=20
        thresholds['NOS']=30
        thresholds['NPA']=4
        thresholds['NPM']=20
        thresholds['NS']=8
        thresholds['TLLOC']=105
        thresholds['TLOC']=100
        thresholds['TNA']=10
        thresholds['TNG']=7
        thresholds['TNLA']=5
        thresholds['TNLG']=4
        thresholds['TNLM']=10
        thresholds['TNLPA']=1
        thresholds['TNLPM']=8
        thresholds['TNLS']=2
        thresholds['TNM']=25
        thresholds['TNOS']=25
        thresholds['TNPA']=4
        thresholds['TNPM']=20
        thresholds['TNS']=6
        
        
        return thresholds

