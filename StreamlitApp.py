import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file , get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGENERATOR import generate_evaluate_chain
from src.mcqgenerator.logger import logging
import time


# Construct the relative file path
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'json-respone', 'Response.json')

# Loading JSON File
with open(file_path, 'r') as file:
    Response_JSON=json.loads(file.read())
# creating Title
st.title("MCQs Creator Application with LangChain")

# Create a form
with st.form("user_inputs"):
    #File Upload
    uploaded_file=st.file_uploader("Upload a PDF or txt file ")
   

    #Input Fields
    mcq_count=st.number_input("No. of MCQs", min_value=3 , max_value=50)

    #Subjet
    subject=st.text_input("Insert Subject", max_chars=20)

    #Quiz_tone
    tone=st.text_input("Complexity level of Questions", max_chars=20 , placeholder="Simple")

    # Add Button
    button=st.form_submit_button("Create MCQs")


    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            time.sleep(5)
            try:
                text=read_file(uploaded_file)
                #count tokens and the cost of API call
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json":json.dumps(Response_JSON)
                        }
                    )
                # st.write(response)
            
            
            except Exception as e:
                traceback.print_exception(type(e),e, e.__traceback__)
                st.error("Error")

            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                # st.text_area(response)
                if isinstance(response,dict):
                    #extract the quiz data from response
                    quiz=response.get("quiz",None)
                   
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        # st.write(table_data)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            #Display the review in a text box as well
                            st.text_area(label="Review",value=response["review"])
                        else:
                            st.error("Error in table data")
                    else:
                        st.write(response)


        

