import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
import pickle

def read_file():
    path_to_file = 'Patient_Data_Clusters.csv'
    dataset = pd.read_csv(path_to_file, sep = ';')
    return(dataset)

def dataset_preparing(n = str()):
    df = read_file()[(read_file()['CounterDrugs'] == 1) & 
                     (read_file()['AntihypertensiveClassCombined'] == n)]    
    Patient_profile = np.array([[df['Systolic'].iloc[i], df['Diastolic'].iloc[i], df['Sex'].iloc[i], 
                                 df['Age'].iloc[i], df['BMI'].iloc[i], df['Smoke'].iloc[i], 
                                 df['Hereditary'].iloc[i], df['Dyslipidemia'].iloc[i], 
                                 df['Diabetes'].iloc[i], df['IGT'].iloc[i], df['LVH'].iloc[i], 
                                 df['Microalbuminuria'].iloc[i], df['CKDStage'].iloc[i], 
                                 df['CHF'].iloc[i], df['IHD'].iloc[i]] for i in range(0, len(df))])
    Treatment_outcome = np.array([df['TreatmentOutcome'].iloc[i] for i in range(0, len(df))]) 
    return(Patient_profile, Treatment_outcome)

def dataset_random_split(n = str()):
    X = dataset_preparing(n)[0]
    Y = dataset_preparing(n)[1]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.25, random_state = 17)
    return(X_train, X_test, Y_train, Y_test)

def classifier_building(n = str(), depth = int()):
    X_train = dataset_random_split(n)[0]
    Y_train = dataset_random_split(n)[2]
    model_parameters = tree.DecisionTreeClassifier(random_state = 17, criterion = 'gini', 
                                                   max_depth = depth)
    model = model_parameters.fit(X_train, Y_train)
    return(model)

def classifier_score(n = str(), depth = int()):
    model = classifier_building(n, depth)
    X_test = dataset_random_split(n)[1] 
    Y_test = dataset_random_split(n)[3]
    predict_class = model.predict(X_test)
    CM = confusion_matrix(Y_test, predict_class)
    sensitivity = CM[1,1]/(CM[1,1] + CM[1,0]) 
    specificity = CM[0,0]/(CM[0,0] + CM[0,1])
    return(sensitivity, specificity)

def decision_tree_store(n = str(), depth = int(), name = str()):
    output = open(name, 'wb')
    pickle.dump(classifier_building(n, depth), output)
    output.close()

if __name__ == "__main__":
    decision_tree_BB = decision_tree_store('1', 4, 'Treatment_BB.pkl') 
    decision_tree_iACE = decision_tree_store('2', 4, 'Treatment_iACE.pkl')
    decision_tree_ARB = decision_tree_store('3', 4, 'Treatment_ARB.pkl')
    decision_tree_CaCB = decision_tree_store('4', 4, 'Treatment_CaCB.pkl')
    decision_tree_D = decision_tree_store('5', 5, 'Treatment_D.pkl')
    

         