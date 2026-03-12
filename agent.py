from agno.agent import Agent
from agno.models.groq import Groq
from tools import check_nulls, fill_null, fix_datatypes, check_duplicates, remove_duplicates, detect_outliers, get_summary
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")

df=None

def set_dataframe(dataframe):
    global df
    df=dataframe

def tool_check_nulls()->str:
    return check_nulls(df)

def tool_fill_null()->str:
    return fill_null(df)

def tool_check_duplicates()->str:
    return check_duplicates(df)

def tool_remove_duplicates()->str:
    return remove_duplicates(df)

def tool_detect_outliers()->str:
    return detect_outliers(df)

def tool_get_summary()-> str:
    return get_summary(df)

def tool_fix_datatypes()->str:
    return fix_datatypes(df)

data_cleaning_agent=Agent(
    name="Data Cleaning Agent",
    role="Clean the given csv data",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[tool_check_nulls, tool_fill_null, tool_fix_datatypes, tool_check_duplicates, tool_remove_duplicates, tool_detect_outliers, tool_get_summary],
    instructions="Start with giving summary of the uncleaned data. Next, check for null values and duplicates. Then replace null values, remove duplicates and fix datatypes if required. Finally return summary of cleaned data",
    markdown=True
)