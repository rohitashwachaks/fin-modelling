from sklearn import metrics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def print_confusion(model, train_X, train_y, test_X, test_y, plots = True):
    '''
    Prints the confusion matrix and accuracy score for the model
    Plots the confusion matrix if plots = True
    Plots the ROC curve
    '''
    y_pred_proba = model.predict_proba(test_X)[::,1] # Predict the probability of the positive class (default)

    #create ROC curve
    fpr, tpr, _ = metrics.roc_curve(test_y,  y_pred_proba) # Calculate the ROC curve
    auc = metrics.roc_auc_score(test_y, y_pred_proba) # Calculate the AUC score for the model
    
    # # Youden’s J statistic
    # metric = tpr - fpr
    # GMean Statistic
    metric = np.sqrt(tpr*(1-fpr)) # Calculate the GMean score for the model, This helps to determine the optimal threshold

    # Find index of largest value
    ix = np.argmax(metric) # Find the index of the largest value in the metric. This is the index of the optimal threshold (from the )
    
    threshold = round(_[ix],4) # Get the threshold value for the optimal threshold
    
    y_pred = np.where(y_pred_proba > threshold, 1, 0) # Predict the class for the test data
    test_acc = (test_y == y_pred).mean() # Calculate the accuracy score for the model
    
    if (test_y == model.predict(test_X)).mean() > test_acc: # Edge case handling
        threshold = 0.5

    train_acc = (train_y == np.where(model.predict_proba(train_X)[::,1] > threshold, 1, 0)).mean() # Calculate the training accuracy score for the model
    print('\tTraining accuracy', round(train_acc,2))
    

    print('\tValidation accuracy', round(test_acc,2))
    

    print('\tValidation AUC-Score', round(auc,2))
    
    cf_matrix = metrics.confusion_matrix(test_y, y_pred) # Calculate the confusion matrix

    if plots: # Plot the confusion matrix and ROC curve
        fig, ax = plt.subplots(1,2, figsize=(10, 5))

        ax[0].plot(fpr,tpr,label="AUC="+str(round(auc,4)))
        ax[0].plot([0,1], [0,1], linestyle='--', label='No Skill')
        ax[0].scatter(fpr[ix], tpr[ix], marker='o', color='black', label= f'Best at {round(threshold, 4)}')
        ax[0].legend(loc=4)
        ax[0].set_ylabel('True Positive Rate')
        ax[0].set_xlabel('False Positive Rate')
        ax[0].set_title('ROC Curve')
        # plt.show()

        group_names = ['True Neg','False Neg','False Pos','True Pos']
        group_counts = ['{0:0.0f}'.format(value) for value in cf_matrix.flatten()]
        labels = [f'{v1}\n{v2}' for v1, v2 in zip(group_names,group_counts)]
        # group_percentages = ['{0:.2%}'.format(value) for value in cf_matrix.flatten()/np.sum(cf_matrix)]
        # labels = [f'{v1}\n{v2}\n{v3}' for v1, v2, v3 in zip(group_names,group_counts,group_percentages)]
        labels = np.asarray(labels).reshape(2,2)
        
        ax[1] = sns.heatmap(cf_matrix, annot= labels, fmt= '', cmap='Blues')
        ax[1].set_xlabel('Actual')
        ax[1].set_ylabel('Predicted')
        ax[1].set_xticklabels(['No Default','Default'])
        ax[1].set_yticklabels(['No Default','Default'])
        ax[1].set_title(f'Confusion Matrix @ threshold = {round(threshold,2)}')
        plt.show()
        
    return {'train_acc': train_acc, 
            'test_acc': test_acc, 
            'threshold': threshold, 
            'auc': auc
        }


# Use it as: 
# 
# model_result = print_confusion(model = base_model, 
#                               train_X = X_train, train_y = y_train, 
#                               test_X = X_val, test_y = y_val, 
#                               plots = True)
