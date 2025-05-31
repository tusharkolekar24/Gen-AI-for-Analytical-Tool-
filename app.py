import os
import secrets
import pandas as pd
import numpy as np
import pandas as pd 
import warnings
warnings.filterwarnings('ignore')

from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   send_file, session, url_for)

from datetime import datetime, timedelta
from src.genai import get_analysis_info

# from src.rag import retrival_info
# from langchain.prompts import PromptTemplate
# from langchain.llms import OpenAI 
# from langchain.chains import LLMChain


current_date = str(datetime.now()).split(" ")[0]
date_obj = datetime.strptime(current_date, "%Y-%m-%d")

one_year_ago = date_obj + timedelta(days=1)  # 365, 450
current_date_info = one_year_ago.strftime("%Y-%m-%d")

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(24))

# metainfo
metainfo = dict()
metainfo['rag_content']    = ''
metainfo['mcq_content']    = ''
metainfo['file_name']      = ''
metainfo['content']        = pd.DataFrame()
metainfo['username']       = "admin"
metainfo['model_info']     = 'gpt-4o'
metainfo['temp_info']      = '0.7'
metainfo['question']       = ''

# User data for Demonstration
USERS               = {"admin": "1234"}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if USERS.get(username) == password:
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials, please try again.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("home_form_data", None)  # Clear home form data from the session
    session.pop("page_form_data", None)  # Clear page form data from the session
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# Define a route for the sectoral page
@app.route('/')
def home():
    if "username" in session:
       
        metainfo['username']       = session["username"]
        return render_template(
            "home.html",
            username=session["username"],
            form_data=metainfo,
            current_date=current_date,
        )
    
    return redirect(url_for("login"))

@app.route("/submit_home_form", methods=["POST"])
def submit_home_form():
    # Retrieve form data from home.html

    model_info      = request.form.get('type_model')
    temp_info       = request.form.get('temp_info')

    metainfo['model_info'] = model_info
    metainfo['temp_info']  = temp_info
    
    flash("Form submitted successfully for Home page!", "success")
    return redirect(url_for("home"))


@app.route('/upload', methods=['POST'])
def upload_file():
     
    file = request.files.get('file')
    if file and file.filename.endswith('.csv'):
        
        file.save(f"artifacts/{file.filename}")  # Save uploaded file
        metainfo['file_name']      = file.filename

        csv_file_loc = f"artifacts/{file.filename}"
        
        print(csv_file_loc,"Uploaded")
        # query = "Tell me the name of the person who get maximum salary"

        data = pd.read_csv(csv_file_loc)
        # analytical_info  = get_analysis_info(data = data,
        #                                      query = query)
        # print(analytical_info)
        metainfo['content']        = data

        return render_template(
                "home.html",
                username= metainfo['username'] ,
                form_data=metainfo,
                current_date=current_date,
            )
    
    return redirect(url_for("login"))

@app.route("/process_input", methods=["POST"])
def process_input():
    question_info = request.form.get("user-input")

    print(question_info,type(question_info),'question_info')
    # print(metainfo['content'],'content')

    if (question_info !='') & (metainfo['content'].shape[0]!=0):

        try :
            analytical_info  = get_analysis_info(dataset  = metainfo['content'],
                                                query    = question_info)
            #print(analytical_info)
        except:
               analytical_info = {"intermediate_steps":'','output':''}
  
        metainfo['rag_content']    = analytical_info['intermediate_steps']

        if analytical_info['intermediate_steps']!='':
            metainfo['mcq_content'] = analytical_info['output']
            metainfo['rag_content'] = 'import pandas as pd\n\n df = pd.read_csv(r"artifacts/employees.csv")\n\n'+analytical_info['intermediate_steps']

        if analytical_info['intermediate_steps']=='':
            metainfo['mcq_content'] = 'Given Data does not have Answer for ask question'
            metainfo['rag_content'] = 'Given Data does not have Answer for ask question'

        metainfo['question']       = question_info

        return render_template(
                "home.html",
                username=metainfo["username"],
                form_data=metainfo,
                current_date=current_date,
            )
    
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)