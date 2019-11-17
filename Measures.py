'''
return_measures method which returns a list with measures
'''
def return_measures():
    
    #measures list with the name of the metrics 
    measures=[]

    #cohesion metrics    
    measures.append("LCOM5")

    
    #complexity metrics
    measures.append("NL")
    measures.append("NLE")
    measures.append("WMC")
    
    #coupling metrics
    measures.append("CBO")
    measures.append("CBOI")
    measures.append("NII")
    measures.append("NOI")
    measures.append("RFC")
    
    #inheritance metrics 
    measures.append("DIT")
    measures.append("NOA")
    measures.append("NOC")
    measures.append("NOD")
    measures.append("NOP")
    
    #documentation metrics
    measures.append("TCD")
    measures.append("DLOC")
    measures.append("TCLOC")
    
    #size metrics
    measures.append("LLOC")
    measures.append("LOC")
    measures.append("NA")
    measures.append("NG")
    measures.append("NLA")
    measures.append("NLG")
    measures.append("NLM")
    measures.append("NLPA")
    measures.append("NLPM")
    measures.append("NLS")
    measures.append("NM")
    measures.append("NOS")
    measures.append("NPA")
    measures.append("NPM")
    measures.append("NS")
    measures.append("TLLOC")
    measures.append("TLOC")
    measures.append("TNA")
    measures.append("TNG")
    measures.append("TNLA")
    measures.append("TNLG")
    measures.append("TNLM")
    measures.append("TNLPA")
    measures.append("TNLPM")
    measures.append("TNLS")
    measures.append("TNM")
    measures.append("TNOS")
    measures.append("TNPA")
    measures.append("TNPM")
    measures.append("TNS")
    
    return measures
      
'''
return_meas_per_prop method which returns a dictionary 
keys of dictionary: properties
values of keys: measures which belong to properties
for property size only measures which are not comment out used to train models
'''

def return_meas_per_prop():
    
    measures={}
    
    measures['cohesion']=[]
    measures['cohesion'].append('LCOM5')
    
    
    measures['complexity']=[]
    measures['complexity'].append('NL')
    measures['complexity'].append('NLE')
    measures['complexity'].append('WMC')
    
    
    measures['coupling']=[]
    measures['coupling'].append('CBO')
    measures['coupling'].append('CBOI')
    measures['coupling'].append('NII')
    measures['coupling'].append('NOI')
    measures['coupling'].append('RFC')
    
    
    measures['inheritance']=[]
    measures['inheritance'].append('DIT')
    measures['inheritance'].append('NOA')
    measures['inheritance'].append('NOC')
    measures['inheritance'].append('NOD')
    measures['inheritance'].append('NOP')
    
    
    measures['documentation']=[]
    measures['documentation'].append('TCD')
    measures['documentation'].append('DLOC')
    measures['documentation'].append('TCLOC')
    
    
    measures['size']=[]
    #measures['size'].append('LLOC')
    #measures['size'].append('LOC')
    #measures['size'].append('NA')
    #measures['size'].append('NG')
    #measures['size'].append('NLA')
    #measures['size'].append('NLG')
    #measures['size'].append('NLM')
    #measures['size'].append('NLPA')
    #measures['size'].append('NLPM')
    #measures['size'].append('NLS')
    #measures['size'].append('NM')
    #measures['size'].append('NOS')
    #measures['size'].append('NPA')
    #measures['size'].append('NPM')
    #measures['size'].append('NS')
    measures['size'].append('TLLOC')
    measures['size'].append('TLOC')
    measures['size'].append('TNA')
    measures['size'].append('TNG')
    #measures['size'].append('TNLA')
    #measures['size'].append('TNLG')
    #measures['size'].append('TNLM')
    #measures['size'].append('TNLPA')
    #measures['size'].append('TNLPM')
    #measures['size'].append('TNLS')
    measures['size'].append('TNM')
    measures['size'].append('TNOS')
    #measures['size'].append('TNPA')
    #measures['size'].append('TNPM')
    measures['size'].append('TNS')

    
    return measures
    

    