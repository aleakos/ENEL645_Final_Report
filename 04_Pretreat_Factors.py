# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 09:12:27 2022

@author: owenpaetkau

Use this code to pull in pre-treatment factors and return the following:
    Tumour site
    Gender
    Tumour stage (T and N)
    Alcohol status
    Smoking status
    MDADI_SUM score
    Categorized MDADI_SUM score    

"""

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

input_path = 'H:/HN_TransferLearning/0_data/'
output_path = 'H:/HN_TransferLearning/2_output/04_pretreat_results/'

df = pd.read_excel(input_path + 'pro_data_133pts.xlsx')

# Drop index 130, HN_220, until I can figure out registration.
df = df.drop(130)

# ----------------------------------------------------------------------------
# ----------- Exporting pre-treatment information-----------------------------
# ----------------------------------------------------------------------------

# Pull out easy information.
np.save(output_path + 'hn_id.npy',np.array(df.QoLID))
np.save(output_path + 'gender.npy',np.array(df.Gender))
np.save(output_path + 't_stage.npy',np.array(df.Tstage))
np.save(output_path + 'n_stage.npy',np.array(df.Nstage))
np.save(output_path + 'alcohol_intake.npy',np.array(df.AlcoholIntake))
np.save(output_path + 'smoking_history.npy',np.array(df.SmokingHistory))

# Create key for categorizing MDADI information.
col = 'MDADI_TOTAL_SUM'
conditions = [(df[col] >= 0) & (df[col] < 20),
    (df[col] >= 20) & (df[col] < 40),
    (df[col] >= 40) & (df[col] < 60),
    (df[col] >= 60) & (df[col] < 80),
    (df[col] > 80)]

# create a list of the values we want to assign for each condition
values = ['none', 'mild', 'moderate', 'severe','profound']
values_oh = [0,0,1,2,2]

values_binary = ['asymptomatic','asymptomatic', 'dysphagia','dysphagia','dysphagia']
values_binary_oh = [0,0,1,1,1]

# create a new column and use np.select to assign values to it using our lists as arguments
mdadi_cat = np.select(conditions, values)
mdadi_cat_oh = np.select(conditions, values_oh)

mdadi_binary = np.select(conditions, values_binary)
mdadi_binary_oh = np.select(conditions, values_binary_oh)

np.save(output_path + 'mdadi_labels.npy', mdadi_cat)
np.save(output_path + 'mdadi_labels_oh.npy', mdadi_cat_oh)

np.save(output_path + 'mdadi_labels_binary.npy', mdadi_binary)
np.save(output_path + 'mdadi_labels_binary_oh.npy', mdadi_binary_oh)

# ----------------------------------------------------------------------------
# ----------- Creating balanced train, validation and test sets  -------------
# ----------------------------------------------------------------------------


# Replace CancerSite categories with Oropharynx, Nasopharynx, Other
df = df.replace(['Nasal Cavity','Larynx','Hypopharynx',
                 'Oral Cavity','Unknown'],'Other')
np.save(output_path + 'cancer_site.npy',np.array(df.CancerSite))


df['MDADI_Categories'] = mdadi_cat
df['MDADI_Binary'] = mdadi_binary

# Select the training set - 70% training, 15% validation, 15% test.
X_train, X_test, y_train, y_test = train_test_split(df, pd.concat([df['MDADI_Categories'], df.CancerSite], axis=1), 
                                                    test_size = 0.30, random_state = 42, 
                                                    stratify = pd.concat([df.MDADI_Categories, df.CancerSite], axis=1))

# Select the validation - 15% validation, 15% test.
X_val, X_test, y_val, y_test = train_test_split(X_test, pd.concat([y_test, X_test.CancerSite], axis = 1), 
                                                test_size = 0.50, random_state = 42, 
                                                stratify = pd.concat([y_test, X_test.CancerSite], axis = 1))

train = np.array(X_train.index)
test = np.array(X_test.index)
validation = np.array(X_val.index)

np.save(output_path + 'training_set.npy', train)
np.save(output_path + 'test_set.npy', test)
np.save(output_path + 'validation_set.npy', validation)










