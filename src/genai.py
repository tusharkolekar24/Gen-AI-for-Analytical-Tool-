
import json
import os
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

with open('src\openai_key.json','r') as jsonfile:
     openai_key_info = json.load(jsonfile)

openai_api_key = openai_key_info["api_key"]
os.environ["OPENAI_API_KEY"] = openai_api_key


def get_analysis_info(dataset, query):
    llm = ChatOpenAI(
        model_name="gpt-4o",
        temperature=0
    )

    agent = create_pandas_dataframe_agent(
        llm,
        dataset,
        verbose=True,
        return_intermediate_steps=True,
        allow_dangerous_code=True
    )

    full_query = query  # Remove system_instruction for now

    final_answer = agent.invoke(input=full_query)

    python_code = []
    for step in final_answer.get('intermediate_steps', []):
        action = step[0]
        if action.tool == "python_repl_ast":
            python_code.append(action.tool_input)

    output = final_answer.get("output", "").strip()
    if not output or "does not contain" in output.lower():
        output = "The given data does not contain an answer to the question."

    return {
        "input": final_answer.get("input", ""),
        "output": output,
        "intermediate_steps": "\n\n".join(python_code)
    }

# def get_analysis_info(data, query):
#     llm = OpenAI(openai_api_key=openai_api_key)
#     agent = create_pandas_dataframe_agent(llm, 
#                                           data, 
#                                           verbose=True, 
#                                           allow_dangerous_code=True, 
#                                           return_intermediate_steps=True)
    
#     final_answer = agent.invoke(input=query, return_intermediate_steps=True)
    
#     if len(final_answer['intermediate_steps'])!=0:
#         python_code = []
#         for step in final_answer['intermediate_steps']:
#             action = step[0]
#             observation = step[1]
#             if action.tool == "python_repl_ast":
#                 # print(action.tool_input)
#                 python_code.append(action.tool_input)
#         intermediate_steps = '\n\n'.join(python_code)
        
#     if len(final_answer['intermediate_steps'])==0:   
#           intermediate_steps = ''

#     return {'input':final_answer['input'], 
#             'output':final_answer['output'],
#             'intermediate_steps':intermediate_steps}
