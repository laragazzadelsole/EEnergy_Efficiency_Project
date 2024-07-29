# remove unused imports
# group imports in similar sections
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import io
import numpy as np
from google.oauth2 import service_account
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from requests_oauthlib import OAuth2Session
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
# Its always better to avoid using *, because you can't easily trace back what you are importing
from fixed_components import *
import altair as alt

def initialize_session_state():
    # add a comment explaining why the fact that "key" is in session state is important :thinking:
    if 'key' not in st.session_state:
        st.session_state['key'] = 'value'
        st.session_state['consent'] = False
        st.session_state['submit'] = False
        st.session_state['No answer'] = ''
    
    # same for key as above
    if 'data' not in st.session_state:
        # this can be defined above as a constant or in an external file
        st.session_state['data'] = {
            'User Full Name': [],
            'User Working Position': [],
            'User Professional Category': [],
            'User Years of Experience': [],
            'Minimum Effect Size Q1': [],
            'Minimum Effect Size Q2': [],    
            'Minimum Effect Size Q3': [],
            'Minimum Effect Size Q4': [],
            'Minimum Effect Size Q5': [],
            'Minimum Effect Size Q6': [],
            'Minimum Effect Size Q7': [],
            'Minimum Effect Size Q8': [],
            'Minimum Effect Size Q9': [],
            'Cost-Benefit Ratio': [],
            'Risk Aversion': []
            # remove unused things
            #'RCT Q1': [],
            #'RCT Q2': [],
            #'RCT Q3': [],
            #'RCT Q4': [],
            #'RCT Q5': [],
            #'RCT Q6': []
            }
    
# this does not let you break, are you sure its what you need?
def safe_var(key):
    if key in st.session_state:
        return st.session_state[key]

def survey_title_subtitle(header_config):
    st.title(header_config['survey_title'])
    st.write(header_config['survey_description'])

def create_question(jsonfile_name):
# why do you need to cast to string?
    minor_value = str(jsonfile_name['minor_value'])
    min_value = jsonfile_name['min_value_graph']
    max_value = jsonfile_name['max_value_graph']
    interval = jsonfile_name['step_size_graph']
    major_value = str(jsonfile_name['major_value'])

    # you could define an external function for this
    # Create a list of ranges based on the provided values
    x_axis = [minor_value] + [f"{round(i, 1)} - {round((i + interval - 0.01), 2)}" for i in np.arange(min_value, max_value, interval)] + [major_value]

    # TODO find a way to remove it -> agree, this is super sad
    if jsonfile_name['min_value_graph'] == -1:
        x_axis.insert(6, 0)
        x_axis[1] = '-0.99 - -0.81'
        x_axis[7] = '0.01 - 0.19'
    elif jsonfile_name['min_value_graph'] == -15:
        x_axis.insert(4, 0)
        x_axis[5] = '0.01 - 4.99'
    elif jsonfile_name['min_value_graph'] == 0:    
        x_axis[1] = '0.01 - 4.99'

    y_axis = np.zeros(len(x_axis))

    # don't use generic names like column_1
    data = pd.DataFrame(list(zip(x_axis, y_axis)), columns=[jsonfile_name['column_1'], jsonfile_name['column_2']])
    
    st.subheader(jsonfile_name['title_question'])
    st.write(jsonfile_name['subtitle_question'])
    
    # comment and specify what you are doing in such complex functions
    data_container = st.container()
    with data_container:
        table, plot = st.columns([0.4, 0.6], gap="large")
        with table:
            # generic names
            bins_grid = st.data_editor(data, key= jsonfile_name['key'], hide_index=True, use_container_width=True, disabled=[jsonfile_name['column_1']])

            percentage_difference = 100 - sum(bins_grid[jsonfile_name['column_2']])

            # Display the counter -> external fuction
            if percentage_difference > 0:
                st.write(f"**You still have to allocate {percentage_difference} percent probability.**")
            elif percentage_difference == 0:
                st.write(f'**You have allocated all probabilities!**')
            else:
                st.write(f'**:red[You have inserted {abs(percentage_difference)} percent more, please review your percentage distribution.]**')           
                  
        with plot:
            # TODO check performance difference with matplotlib
            chart = alt.Chart(bins_grid).mark_bar().encode(
                x=alt.X(jsonfile_name['column_1'], sort=None),
                y=jsonfile_name['column_2']
            )

            st.altair_chart(chart, use_container_width=True)
    
    return pd.DataFrame(bins_grid), percentage_difference,  len(bins_grid)

def effect_size_question(jsonfile_name):
    col1, _ = st.columns(2)
    with col1:
        st.markdown(jsonfile_name['effect_size'])
        st.text_input("Please insert a number or write 'I don't know'.", key = jsonfile_name['num_input_question'])

def RCT_questions():
    # this lines should be constants or external fules
    st.subheader('Questions on RCTs Evaluation')
    st.write('We would like to know your opinion regarding RCTs programs.')
    st.write('1. After my experience in being involved in this project, I am:')
    st.radio('Choose one of the following options:', ['More interested in using RCTs for evaluation of other government projects', 'Just as interested in using RCTs for evaluation of other government projects as I was before starting this one', 'Less interested in using RCTs for evaluation of other government projects'], key ='RCT_question1')
    st.write('2. We would like you to compare your experiences on this project that we are evaluating through an experiment to similar government projects you have worked on that have not had such an evaluation. Can you please compare this project to similar projects without an experimental evaluation in terms of:')
    st.write('- Design of the intervention')
    st.radio('Choose one of the following options:', ['The RCT improved the design of the intervention relative to projects without an RCT', 'The RCT did not change the design', 'The RCT led the intervention to be designed less well than projects without an RCT'], key='RCT_question2')
    st.write('- Speed of Implementation')
    st.radio('Choose one of the following options:', ['The RCT sped up implementation of the project', 'The RCT did not change the speed', 'The RCT slowed down the speed of implementation'], key='RCT_question3')
    st.write('- Trustiworthiness of program impacts')
    st.radio('Choose one of the following options:', ['I will trust estimates of the programs impacts from this RCT more than of other programs that use our standard M&E', "I will trust estimates of this program's impacts equally as much as other programs that use our standard M&E", "I will trust estimates of this program's impacts from the RCT less than those of other programs that use our standard M&E"], key='RCT_question4')
    st.write('- Do you think that thanks to the RCT you reached new beneficiaries? Do you think that it helped you disburse more funds than you originally planned?')
    st.text_input('Please, write about your experience (max 500 characters).',max_chars=500, key = 'RCT_question5')
    st.write('- Do you think allocating grants randomly amongst equally eligible potential beneficiaries is ethical? Did you think so before engaging in the RCT?')
    st.text_input('Please, write about your experience (max 500 characters).', max_chars=500, key = 'RCT_question6')

# params names are too generic + could pass a dictionary and not a list of stuff
def add_submission(updated_bins_question_1_df, updated_bins_question_2_df, updated_bins_question_3_df, updated_bins_question_4_df, updated_bins_question_5_df, updated_bins_question_6_df, updated_bins_question_7_df, updated_bins_question_8_df, updated_bins_question_9_df):

    updated_bins_list = [updated_bins_question_1_df, updated_bins_question_2_df, updated_bins_question_3_df, updated_bins_question_4_df, updated_bins_question_5_df, updated_bins_question_6_df, updated_bins_question_7_df, updated_bins_question_8_df, updated_bins_question_9_df]
    # remove unused stuff
    # Extracting the first row of each transposed dataframe as column names
    #for i, transposed_df in enumerate(transposed_bins_list):
    #    transposed_df.columns = column_names_list[i]

    # Removing the first row (used as column names) from each dataframe
    #transposed_bins_list = [transposed_df.iloc[1:] for transposed_df in transposed_bins_list]

    # Adding prefix to column names of each dataframe
    #for i, transposed_df in enumerate(transposed_bins_list):
    #    prefix = f'Q{i + 1}  '
    #    transposed_df.columns =  [f'{prefix}{col}' for col in transposed_df.columns]

    # generic name of fucntion
    def restructure_df(df, i):
        transposed_df = df.transpose()
        transposed_df.columns =  [f'Q{i + 1}  {col}' for col in list(transposed_df.iloc[0])]
        transposed_df = transposed_df.iloc[1:]
        return transposed_df

    transposed_bins_list = []
    for i, df in enumerate(updated_bins_list):
        transposed_bins_list.append(restructure_df(df, i))

    # Concatenating transposed dataframes
    questions_df = pd.concat(transposed_bins_list, axis=1)

    # Resetting index if needed "if needed"?
    questions_df.reset_index(drop=True, inplace=True)

    # Update session state
    data = st.session_state['data']

    # should be at file level not here
    USER_FULL_NAME = 'User Full Name'
    USER_PROF_CATEGORY = 'User Professional Category'
    USER_POSITION = 'User Working Position'
    YEARS_OF_EXPERIENCE = 'User Years of Experience'
    MIN_EFF_SIZE_Q1 = 'Minimum Effect Size Q1'
    MIN_EFF_SIZE_Q2 = 'Minimum Effect Size Q2'
    MIN_EFF_SIZE_Q3 = 'Minimum Effect Size Q3'
    MIN_EFF_SIZE_Q4 = 'Minimum Effect Size Q4'
    MIN_EFF_SIZE_Q5 = 'Minimum Effect Size Q5'
    MIN_EFF_SIZE_Q6 = 'Minimum Effect Size Q6'
    MIN_EFF_SIZE_Q7 = 'Minimum Effect Size Q7'
    MIN_EFF_SIZE_Q8 = 'Minimum Effect Size Q8'
    MIN_EFF_SIZE_Q9 = 'Minimum Effect Size Q9'
    #MIN_EFF_SIZE_Q10 = 'Minimum Effect Size Q10'
    COST_BENEFIT_RATIO = 'Cost-Benefit Ratio'
    RISK_AVERSION = 'Risk Aversion'
    #RCT_Q1 = 'RCT Q1'
    #RCT_Q2 = 'RCT Q2'
    #RCT_Q3 = 'RCT Q3'
    #RCT_Q4 = 'RCT Q4'
    #RCT_Q5 = 'RCT Q5'
    #RCT_Q6 = 'RCT Q6'

    # do you really need to do it one by one?
    data[USER_FULL_NAME].append(safe_var('user_full_name'))
    data[USER_POSITION].append(safe_var('user_position'))
    data[USER_PROF_CATEGORY].append(safe_var('professional_category'))
    data[YEARS_OF_EXPERIENCE].append(safe_var('years_of_experience'))
    data[MIN_EFF_SIZE_Q1].append(safe_var('num_input_question1'))
    data[MIN_EFF_SIZE_Q2].append(safe_var('num_input_question2'))
    data[MIN_EFF_SIZE_Q3].append(safe_var('num_input_question3'))
    data[MIN_EFF_SIZE_Q4].append(safe_var('num_input_question4'))
    data[MIN_EFF_SIZE_Q5].append(safe_var('num_input_question5'))
    data[MIN_EFF_SIZE_Q6].append(safe_var('num_input_question6'))
    data[MIN_EFF_SIZE_Q7].append(safe_var('num_input_question7'))
    data[MIN_EFF_SIZE_Q8].append(safe_var('num_input_question8'))
    data[MIN_EFF_SIZE_Q9].append(safe_var('num_input_question9'))
    #data[MIN_EFF_SIZE_Q10].append(safe_var('num_input_question10'))
    data[COST_BENEFIT_RATIO].append(safe_var('cost_benefit'))
    data[RISK_AVERSION].append(safe_var('risk_aversion'))
    #data[RCT_Q1].append(safe_var('RCT_question1'))
    #data[RCT_Q2].append(safe_var('RCT_question2'))
    #data[RCT_Q3].append(safe_var('RCT_question3'))
    #data[RCT_Q4].append(safe_var('RCT_question4'))
    #data[RCT_Q5].append(safe_var('RCT_question5'))
    #data[RCT_Q6].append(safe_var('RCT_question6'))

    st.session_state['data'] = data
    
    session_state_df = pd.DataFrame(data)
    personal_data_df = session_state_df.iloc[:, :4]
    min_eff_df = session_state_df.iloc[:, 4:]

    concatenated_df = pd.concat([personal_data_df, questions_df.set_index(personal_data_df.index), min_eff_df.set_index(personal_data_df.index)], axis=1)
    
    
    st.session_state['submit'] = True
    
    #save data to google sheet -> constants or external file
    # external function
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(secrets_to_json(), scope)
    client = gspread.authorize(creds)
 
    sheet = client.open("EEnergy_Efficiency_Survey_Data").sheet1

    # remove unused stuff
    column_names_list = concatenated_df.columns.tolist()
    #column_names = sheet.append_row(column_names_list)

    sheet_row_update = sheet.append_rows(concatenated_df.values.tolist()) #.values.tolist())
    
    #Navigate to the folder in Google Drive. Copy the Folder ID found in the URL. This is everything that comes after “folder/” in the URL.
    backup_sheet = client.create(f'Backup_{data[USER_FULL_NAME]}_{datetime.now()}', folder_id= secrets_to_json()['folder_id']).sheet1
    backup_sheet = backup_sheet.append_rows(concatenated_df.values.tolist()) #(new_bins_df.iloc[:2].values.tolist())
    #backup_sheet.share('', perm_type = 'user', role = 'writer')

