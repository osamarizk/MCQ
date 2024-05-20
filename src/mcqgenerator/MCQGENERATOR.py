import os
import json
import pandas as pd
import traceback
import PyPDF2
from dotenv import load_dotenv
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file, get_table_data

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback


load_dotenv()

# we can use if we defined the key with name not defined for langchain
# key=os.getenv("OPENAI_API_KEY") 

# temperature that take a value between 0 nad 2 ( near 0 is less creative)
llm=ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.3
)

# define your template

template="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

# design your Prompt template
quiz_generation_prompt=PromptTemplate(
    input_variables=["text","number","subject","tone","response_json"],
    template=template
)
# collect the output inside this variable (output_key="quiz" and am use it in the below Evaluate Template)
quiz_chain=LLMChain(
    llm=llm,
    prompt=quiz_generation_prompt,
    output_key="quiz",
)

# Template for Evluation
template2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students. \
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for the complexity analysis
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student ability.
Quiz_MCQs:
{quiz}

check from an expert English Writer of the above quiz:
"""

# design your Prompt template2
quiz_evaluation_prompt=PromptTemplate(
    input_variables=["subject","quiz"],
    template=template2
)

review_chain=LLMChain(
    llm=llm,
    prompt=quiz_evaluation_prompt,
    output_key="review",
)

# Sequential Chain ( output variable get from output_key from every chain)
generate_evaluate_chain=SequentialChain(
    chains=[quiz_chain,review_chain],
    input_variables=["text","number","subject","tone","response_json"],
    output_variables=["quiz","review"],
)