#!/usr/bin/env python
# coding: utf-8

# In[313]:


import pandas as pd

#import data and create a temp table

patient_df = pd.read_csv(r'C:\Users\bafna\Desktop\patient_df.csv')
response_df = pd.read_csv(r"C:\Users\bafna\Desktop\response_df.csv")
patient_df['name'] = patient_df['name'].str.split('.').str[-1]
temp_tab1 = response_df.copy()

# Get patients who have taken excluded medications
non_med_list = ['lubiprostone','osmoprep','plecanatide','trulance']
non_med = '|'.join(non_med_list)
df_non_med = temp_tab1[(temp_tab1['data_category'].str.lower() == 'medications') & (temp_tab1['response_value'].str.lower().str.contains(non_med))]

# drop the patients who have taken excluded medications from temp table
pat = df_non_med['patient_id']
out = temp_tab1['patient_id'].isin(pat)
temp_tab1.drop(temp_tab1[out].index,inplace = True)

# Get patients with current conditions as constipation
df_curr = temp_tab1[(temp_tab1['data_category'].str.lower() == 'current_conditions') & (temp_tab1['response_value'].str.lower().str.contains('constipation'))]


# Get patients with Past conditions from the listed symptoms
past_cond_list = ['ibsc','ibs-c','irritable syndrome constipation','chronic idiopathic',
            'idiopathic constipation','chronic idiopathic constipation','cic']
past_cond = '|'.join(past_cond_list)

df_past =  temp_tab1[(temp_tab1['data_category'].str.lower() == 'past_conditions') & (temp_tab1['response_value'].str.lower().str.contains(past_cond))]


# Get patients who have taken the listed medication
med_list = ['amitiza', 'cephulac','chronulac']
med = '|'.join(med_list)
df_med =temp_tab1[(temp_tab1['data_category'].str.lower() == 'medications') &(temp_tab1['response_value'].str.lower().str.contains(med))]


# Get patients with Past conditions from the listed symptoms and who have taken the listed medication
df_inner = pd.merge(df_past,df_med, left_on = 'patient_id', right_on = 'patient_id', how = 'inner')

# Data of patients with constipation
result = pd.concat([df_curr['patient_id'],df_inner['patient_id']],axis=0)
result.drop_duplicates(inplace = True)


# Join tables to get the desired columns
result = patient_df.merge(result, on ='patient_id' ,how = 'inner')
result = result.merge(response_df,on = 'patient_id', how = 'left')

result = result[['patient_id','name','sex','address','birthdate','response_value']]


#Calculate age
result['birthdate'] = pd.to_datetime(result['birthdate'])
result['Patient Age'] = (pd.to_datetime('now') - result['birthdate']).astype('<m8[Y]')


# Split first name and last name
result[['Patient First Name', 'Patient Last Name']] = result['name'].str.split(n=1, expand=True)
result.drop(columns=['name', 'birthdate'], inplace=True)


# Get state abbreviation from address
result['Address State'] = result['address'].str.extract(r',\s*(\w{2})')
result.drop(columns=['address'], inplace=True)



# Display the final result
result[['patient_id','Patient First Name','Patient Last Name','sex','Patient Age','Address State','response_value']]


# In[312]:


# Get count of unique patients
result.nunique()
# 311 Patients with constipation


# In[ ]:




