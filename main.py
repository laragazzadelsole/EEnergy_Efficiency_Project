#import streamlit as st
import json
from fixed_components import *
from changing_components import *
import numpy as np

st.set_page_config(layout="wide")



# Read the JSON file
config = json.load(open('config.json'))

initialize_session_state()


survey_title_subtitle(config['header'])

consent_form()

if st.session_state['consent'] == True:

    personal_information()

    #entrepreneur_firm_representative_question()
    
    sustainability_advisors_question()

    #st.button("Next Page", on_click=next_page)
    

    st.subheader(SECTION_TWO)
    instructions()

    q1_config = config['question1']
    updated_bins_question_1_df, percentage_difference1, num_bins1 = create_question(q1_config)
    
    ##if st.session_state['professional_category'] in ['Policy implementer (EENergy consortium working package leaders)', 'Donor (European Commission)', 'Researcher', 'Sustainability Advisor','Entrepreneur/Firm Representative']:
    effect_size_question1 = effect_size_question(q1_config)
    
    q2_config = config['question2']
    updated_bins_question_2_df, percentage_difference2, num_bins2 = create_question(q2_config)
    
    #if st.session_state['professional_category'] in ['Policy implementer (EENergy consortium working package leaders)', 'Donor (European Commission)', 'Researcher', 'Sustainability Advisor', 'Entrepreneur/Firm Representative']:
    effect_size_question2 = effect_size_question(q2_config)
    
    q3_config = config['question3']
    updated_bins_question_3_df, percentage_difference3, num_bins3 = create_question(q3_config)
    
    #if st.session_state['professional_category'] in ['Policy implementer (EENergy consortium working package leaders)', 'Donor (European Commission)', 'Researcher', 'Sustainability Advisor', 'Entrepreneur/Firm Representative']:
    effect_size_question3 = effect_size_question(q3_config)
    
    q4_config = config['question4']
    updated_bins_question_4_df, percentage_difference4, num_bins4 = create_question(q4_config)
    
    #if st.session_state['professional_category'] in ['Policy implementer (EENergy consortium working package leaders)', 'Donor (European Commission)', 'Researcher', 'Sustainability Advisor', 'Entrepreneur/Firm Representative']:
    effect_size_question4 = effect_size_question(q4_config)
    
    q5_config = config['question5']
    updated_bins_question_5_df, percentage_difference5, num_bins5 = create_question(q5_config)
    
    #if st.session_state['professional_category'] in ['Policy implementer (EENergy consortium working package leaders)', 'Donor (European Commission)', 'Researcher', 'Sustainability Advisor', 'Entrepreneur/Firm Representative']:
    effect_size_question5 = effect_size_question(q5_config)
    
    
    q6_config = config['question6']
    updated_bins_question_6_df, percentage_difference6, num_bins6 = create_question(q6_config)
        
    #if st.session_state['professional_category'] in ['Policy implementer (EENergy consortium working package leaders)', 'Donor (European Commission)', 'Researcher', 'Sustainability Advisor', 'Entrepreneur/Firm Representative']:    
    effect_size_question6 = effect_size_question(q6_config)
        
    
    q7_config = config['question7']
    updated_bins_question_7_df, percentage_difference7, num_bins7 = create_question(q7_config)
    #effect_size_question9 = effect_size_question(q9_config)
    
    col2, _ = st.columns(2)
    with col2:
        st.image("SatSunGraph.png", width = 350)
    st.write("Saturday and Sunday temperatures in Washington DC for each weekend in 2022. As we might expect, there is a strong correlation between the temperature on a Saturday and on the Sunday, since some parts of the year are hot, and others colder. The correlation here is 0.88.")
    
    q8_config = config['question8']
    updated_bins_question_8_df, percentage_difference8, num_bins8 = create_question(q8_config)    
    
    percentage_differences = [percentage_difference1, percentage_difference2] #, percentage_difference3, percentage_difference4, percentage_difference5
    updated_bins_list = [updated_bins_question_1_df, updated_bins_question_2_df]#, updated_bins_question_3_df, updated_bins_question_4_df, updated_bins_question_5_df
    
    
    st.subheader("Question 9 - Cost/Benefit Ratio")
    st.write("In simple terms, a cost-benefit ratio is used to compare the costs of a project against the benefits it delivers. For instance, if a program costs €100.000 and the monetized value of its benefits is €150.000, the cost-benefit ratio would be 1:1.5. This means that for every euro spent, the program delivers one and a half euro in benefits. A higher ratio indicates greater efficiency and value for money. This question prompts to consider the efficiency and economic justification for scaling a program, ensuring that the decision aligns with both fiscal responsibility and the desired impact. At what cost-benefit ratio would you consider scaling the EEnergy Efficiency Project?\n Consider “benefits” that occurred after two years of running the program and “costs” as the total expenses incurred to implement, operate, and maintain a program or project (including administration and overhead costs).")
    
    col1, _= st.columns(2)
    with col1:
        # list needed later in the cost/benefit question
        cost_benefit_list = [f"1:{round(i, 1)}" for i in np.arange(0.6, 3.1, .2)]
        st.select_slider("Please move the slider to indicate your preference.", cost_benefit_list, key = "cost_benefit")
    
    st.subheader("Question 10 - Risk Aversion")
    st.write("Rate your willingness to take risks in general on a 10-point scale, with 1 completely unwilling and 10 completely willing.")
    
    col1, _= st.columns(2)
    with col1:   
        st.slider("Please move the slider to indicate your preference.", 1, 10, key= "risk_aversion")
    
    ##if st.session_state['professional_category'] in ['Government Official/Donor', 'Program Implementer/Practitioner']:
        #RCT_questions() 
    
    # Submission button + saving data 
    if all(percentage == 0 for percentage in percentage_differences):
        submit = st.button("Submit", on_click = add_submission, args = ([updated_bins_question_1_df, updated_bins_question_2_df, updated_bins_question_3_df, updated_bins_question_4_df, updated_bins_question_5_df, updated_bins_question_6_df, updated_bins_question_7_df, updated_bins_question_8_df]))

    if st.session_state['submit']:
        st.success(f"Thank you for completing the Survey on {config['header']['survey_title']}!")
        # TODO add download button
        #st.write("You can now download your answers as csv file.")
        #concatenated_csv = convert_df(concatenated_df)
        #st.download_button("Download here!", concatenated_csv, 'Foundational Digital Transformation in North-East Romania Survey Answers.csv')
