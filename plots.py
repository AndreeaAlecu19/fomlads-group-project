import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import warnings
from SoftmaxRegression import SoftmaxRegression
from sklearn.ensemble import RandomForestClassifier
from modelconstruct import train_test_data
from metrics import accuracy
from metrics import confusion_matrix
from metrics import precision_and_recall
from metrics import micro_average_f1_score
from metrics import macro_average_f1_score
from sklearn.neighbors import KNeighborsClassifier
plt.style.use('seaborn-whitegrid')
warnings.filterwarnings("ignore")

def rf_hyperparameters(dataset):
    X_train, Y_train, X_test, Y_test = train_test_data(dataset, 0.8) #runs train_test_split function
    n_range=range(10, 100)
    acc_scores=[]
    mi_f1=[]
    ma_f1=[]
    for i in n_range:
        RFClassifier = RandomForestClassifier(n_estimators=i, random_state=4, max_features='log2')
        RFClassifier.fit(X_train,Y_train)
        y_pred_RF = RFClassifier.predict(X_test)
        acc = accuracy(y_pred_RF, Y_test) 
        cm = confusion_matrix(Y_test, y_pred_RF) 
        prm = precision_and_recall(cm) 
        micro_f1 = micro_average_f1_score(cm)
        macro_f1 = macro_average_f1_score(prm) 
        acc_scores.append(acc)
        mi_f1.append(micro_f1)
        ma_f1.append(macro_f1)

    print("For Random Forest, the maximum value for accuracy, micro F1 And macro F1 scores are ",max(acc_scores),", ",max(mi_f1),", ",max(ma_f1), " respectively. These are achieved at n_estimator =", acc_scores.index(max(acc_scores)+1))
    plt.plot(n_range, acc_scores, label='Accuracy on test data')
    plt.title('Test Accuracy vs Number of trees')
    plt.xlabel('Number of trees (n_estimators)')
    plt.ylabel('Test Accuracy')
    plt.legend()
    plt.savefig('RandomForestAccuracyGraph')
    plt.close()

    plt.plot(n_range, mi_f1, label='Micro F1 Score')
    plt.plot(n_range, ma_f1, label='Macro F1 Score')
    plt.title('F1 Score vs Number of trees')
    plt.xlabel('Number of trees (n_estimators)')
    plt.ylabel('F1 Score')
    plt.legend()
    plt.savefig('RandomForestF1ScoreGraph')
    plt.close()
    
    

def oob_error_rf(dataset):
    X_train, Y_train, X_test, Y_test = train_test_data(dataset, 0.8) #runs train_test_split function
    n_range=range(10,100)
    oob_errors=[]
    for i in n_range:
        RFClassifier = RandomForestClassifier(n_estimators=i, oob_score=True, random_state=4)
        RFClassifier.fit(X_train,Y_train)
        oob_errors.append(1-RFClassifier.oob_score_)

    plt.plot(n_range, oob_errors)
    plt.title('OOB error vs Number of trees')
    plt.xlabel('Number of trees (n_estimators)')
    plt.ylabel('OOB Error')
    plt.savefig('RandomForestLossFunctionGraph')
    plt.close()
    
 
# not scaled, below:

# n is the test_train_split value below:
def Knn_hyperparameters(dataset):
    X_train, Y_train, X_test, Y_test = train_test_data(dataset,0.8) #runs train_test_split function
    # Train test split can take different values. However, we will choose a=0.8 as in RandomForest.py, to make the test as fair as possible.
    #Create some empy lists which will be used for plots
    acc_scores_Knn=[]
    mi_f1_Knn=[]
    ma_f1_Knn=[]
    # Start to implement the Knn, using the same data for train_split_test as for Random Forest classifier in order to make the tests as fair as possible.        
    for i in range(1,103,2):
        knnClassifier=KNeighborsClassifier(n_neighbors=i)
        knnClassifier.fit(X_train,Y_train)
        y_pred_Knn = knnClassifier.predict(X_test)
        # Now we shall compute 5 metrics (Accuracy, confusion Matrix, precision, recall and f1 (both types))
        acc_Knn=accuracy(y_pred_Knn, Y_test) #computes accuracy
        cm_Knn=confusion_matrix(Y_test, y_pred_Knn) #computes test confusion matrix
        prm_Knn = precision_and_recall(cm_Knn) #computes precision and recall and represents the in a matrix
        micro_f1_Knn = micro_average_f1_score(cm_Knn) #Micro f1, uses the global precision and recall (prone to imbalanced datasets)
        macro_f1_Knn = macro_average_f1_score(prm_Knn) #Macro f1, uses the average of individual classes' precision and recalls (better for imbalanced datasets)
        acc_scores_Knn.append(acc_Knn)
        mi_f1_Knn.append(micro_f1_Knn)
        ma_f1_Knn.append(macro_f1_Knn)

    plt.plot(range(1,103,2),acc_scores_Knn,label='Accuracy on test for Knn')
    plt.title('Test Accuracy vs K neighbors')
    plt.xlabel('Number of neighbors (k neighbors)')
    plt.ylabel('Test Accuracy')
    plt.legend()
    plt.savefig('KnnAccuracyGraph')
    plt.close()

    plt.plot(range(1,103,2),mi_f1_Knn,label='Micro f1 score for Knn')
    plt.plot(range(1,103,2), ma_f1_Knn, label='Macro F1 Score')
    plt.title('F1 Score vs K neighbors')
    plt.xlabel('Number of neighbors (k neighbors)')
    plt.ylabel('F1 Score')
    plt.legend()
    plt.savefig('KnnF1ScoreGraph')
    plt.close()
    


# Error rate
    
def error_function_Knn(dataset):
    error_rate=[]
    X_train, Y_train, X_test, Y_test = train_test_data(dataset,0.8) #runs train_test_split function
    for i in range(1,103,2):
        knnClassifier=KNeighborsClassifier(n_neighbors=i)
        knnClassifier.fit(X_train,Y_train)
        y_pred_Knn = knnClassifier.predict(X_test)
        error_rate.append(np.mean(y_pred_Knn!=Y_test))
    
    plt.plot(range(1,103,2),error_rate,color='blue', linestyle='dashed', marker='o',
            markerfacecolor='red', markersize=5)
    plt.title('Error Rate vs. K Value')
    plt.xlabel('K neighbors')
    plt.ylabel('Error Rate')
    plt.savefig('KnnErrorFunction')
    plt.close()



#Finding the ideal k for test_train_split=0.8:

def ideal_k(dataset):
    # Train test split can take different values. However, we will choose a=0.8 as in RandomForest.py, to make the test as fair as possible.
    X_train, Y_train, X_test, Y_test = train_test_data(dataset,0.8) 
    listacc=[] #Create an empty list
    i_range=range(1,103,2) # Give different odd values to k_neighbors
    for i in i_range: 
        # Start to implement the Knn, using the same data for train_split_test as for Random Forest classifier in order to make the tests as fair as possible.        
        knnClassifier=KNeighborsClassifier(n_neighbors=i)
        knnClassifier.fit(X_train,Y_train)
        y_pred_Knn = knnClassifier.predict(X_test)
        # Now we shall compute 5 metrics (Accuracy, confusion Matrix, precision, recall and f1 (both types))
        # We have used accuracy as a very important metric to measure how capable a model is for classification
        acc=accuracy(y_pred_Knn, Y_test) #computes accuracy
        listacc.append(acc)
    max_value=max(listacc)
    print("The maximum value of accuracy is ", max_value , "and the ideal k to achieve this value is ", 2*listacc.index(max_value)+1)  
    # The step is 2, and we start the counting of indices from 0. So, to find k, we multiply by 2 the index of maximum value of accuracy and then add 1.
    print("List of accuracy is ", listacc) 

    #Let us now plot the graph which shows the evolution of accuracy vs values of k from 1 up to and including 101.
    plt.plot(i_range,listacc)
    plt.title('Accuracy vs. values of k')
    plt.xlabel('K neighbors')
    plt.ylabel('Accuracy')
    plt.savefig('Ideal k and accuracy')
    plt.close()

ideal_k('MobilePricingUpdated.csv')
Knn_hyperparameters('MobilePricingUpdated.csv')
error_function_Knn('MobilePricingUpdated.csv')
rf_hyperparameters('MobilePricingUpdated.csv')
oob_error_rf('MobilePricingUpdated.csv')






#tried to use the code from the main py as a function but stuck, for now will have this plotting idea as it is in the main file and for the separate model plots can have the in this file
"""
def accuracy_graph(model):
    nvals=[0.5,0.6,0.7,0.8,0.9]
    models=['Random Forest', 'KNN']
    fig=plt.figure()
    plt.xlabel('Train-test splits')
    plt.title('Accuracy vs Train-test splits')
    fig_2=plt.figure()
    plt.xlabel('Train-test splits')
    plt.title('F1 Score vs Train-test splits')

    for i in model:
        accuracy_test=[]
        microf1_scores=[]
        macrof1_scores=[]
        for n in nvals:
            acc_test, confusion_mat, pr_mat, microf1, macrof1, run_time = model[i]
            accuracy_test.append(acc_test)
            microf1_scores.append(microf1)
            macrof1_scores.append(macrof1)
        fig += plt.plot(nvals, acc_test, label='Accuracy on test data ('+models[i]+')')
        plt.legend()
        
        plt.plot(nvals, microf1_scores, label='Micro average f1 score ('+models[i]+')')
        plt.plot(nvals, macrof1_scores, label= 'Macro average f1 score ('+models[i]+')')
        plt.plot()
        plt.legend()
   
"""
