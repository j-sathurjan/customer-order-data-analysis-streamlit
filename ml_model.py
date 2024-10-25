import streamlit as st
from db.db_connector import get_db_connection
from filter import filter_customer_by_amount
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import time

engine = get_db_connection()

def data_preprocessing_for_model_build():
    if engine:
        data_frame = filter_customer_by_amount(0,0)
        data_frame.rename(columns={"total_spent":"total_revenue","number_of_orders":"total_orders"}, inplace=True)
        data_frame['repeat_purchaser'] =  data_frame['total_orders']>1
        
        processingData = data_frame[['total_revenue','total_orders','repeat_purchaser']]
        
        # Count rows with null values
        null_rows_count = processingData.isnull().any(axis=1).sum()
        
        #Frequency of repeat_purchaser
        frequency = processingData['repeat_purchaser'].value_counts()
        
        # split the features and target variables
        X = processingData[['total_revenue','total_orders']]  # Features (total_revenue, total_orders)
        y = processingData['repeat_purchaser']   # Target variable (repeat_purchaser)
        
        return X , y
    return st.error("database connection failed!")

def train_the_lr_model(X,y):
    # Logistic Regression
    model = LogisticRegression()
    
    n_folds = 5
    skf = StratifiedKFold(n_splits=n_folds)
    
    # prepare the features and target
    standardizer = StandardScaler()
    x_label = standardizer.fit_transform(X)
    y_label = np.ravel(y)
    
    test_accuracy = np.zeros((n_folds))
    test_precision = np.zeros((n_folds))
    test_recall = np.zeros((n_folds))
    test_f1 = np.zeros((n_folds))
    test_time = np.zeros((n_folds))

    for i, (train_index, test_index) in enumerate(skf.split(x_label, y_label)):
        
        # Measure execution time
        start_time = time.time()
    
        model.fit(x_label[train_index], y_label[train_index])
        y_pred = model.predict(x_label[test_index])
        
        # Calculate execution time
        end_time = time.time()
        
        # performance metrics
        test_accuracy[i] = accuracy_score(y_label[test_index], y_pred)
        test_precision[i] = precision_score(y_label[test_index], y_pred)
        test_recall[i] = recall_score(y_label[test_index], y_pred)
        test_f1[i] = f1_score(y_label[test_index], y_pred)
        test_time[i]= end_time - start_time
        
    kfold_metric = pd.DataFrame(index=['K-1','K-2','K-3','K-4', 'K-5'],
                            columns=['Accuracy', 'Precision', 'Recall', 'F1score','Time'])
    kfold_metric['Accuracy'] = test_accuracy
    kfold_metric['Precision'] = test_precision
    kfold_metric['Recall'] = test_recall
    kfold_metric['F1score'] = test_f1
    kfold_metric['Time'] = test_time
    
    average_metric = pd.DataFrame(index=['LR'],
                            columns=['Accuracy', 'Precision', 'Recall', 'F1score','Time'])

    average_metric['Accuracy'] = test_accuracy.mean()
    average_metric['Precision'] = test_precision.mean()
    average_metric['Recall'] = test_recall.mean()
    average_metric['F1score'] = test_f1.mean()
    average_metric['Time'] = test_time.mean()

    average_metric_err = pd.DataFrame(index=['LR'],columns=['Accuracy', 'Precision', 'Recall', 'F1score','Time'])

    average_metric_err['Accuracy'] = test_accuracy.std()
    average_metric_err['Precision'] = test_precision.std()
    average_metric_err['Recall'] = test_recall.std()
    average_metric_err['F1score'] = test_f1.std()
    average_metric_err['Time'] = test_time.std()
    
    st.subheader("K-Fold Validation Metrics (K=5)")
    st.write(kfold_metric)
    
    st.subheader("Average metrics")
    st.write(average_metric)
    
    st.subheader("Standard deviation")
    st.write(average_metric_err)
    
    return model, kfold_metric, average_metric_err, average_metric

def predict_results_from_model(data):
    try:
        X,y=data_preprocessing_for_model_build()
        model, kfold_metric, average_metric_err, average_metric = train_the_lr_model(X,y)
        
        standardizer = StandardScaler()
        predict_data = standardizer.fit_transform(data)
        y_predict = model.predict(predict_data)
        
        if y_predict == 1:
            return st.success(f"customer is repeat purchaser.")
        return st.info(f"customer is not repeat purchaser")
    except Exception:
        return st.error("something went wrong on prediction!")