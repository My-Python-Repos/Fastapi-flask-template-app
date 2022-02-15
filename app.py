# Core packages
from fastapi import FastAPI,Request
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask ,render_template
import uvicorn 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# utils
import json
import joblib 
import os

with open("data/netflix_titles.json") as f:
    movielist=json.load(f)
    
def load_model(model_file):
    model=joblib.load(open(os.path.join(model_file),'rb'))
    return model

# NETFLIX_LOAD_MODEL=load_model("models/pipe_lr_cv")

    
#Initialize the app
api=FastAPI(cors=True)
flask_app=Flask(__name__)

#Mount Flask on Fastapi#
api.mount('/blog',WSGIMiddleware(flask_app))


# Api routes/Endpoints
# https:/127.0.0.1:8000/api/v1/titles
# https:/127.0.0.1:8000/api/v1/titles/?limit=10:::Queryparam
# https:/127.0.0.1:8000/api/v1/titles/title/key
# https:/127.0.0.1:8000/api/v1/titles/{show_id}
# https:/127.0.0.1:8000/api/v1/titles/predict/{searchterm}

@api.get("/api",include_in_schema=False)
async def root_app():
    return {'text':'Hello This is fastpi based recommender system'}


# https:/127.0.0.1:8000/api/v1/titles
#Query param
@api.get("/api/v1/titles")
async def read_all_titles(limit:int=10):
    """Return a Movie of List of Movies/Shows"""
    return {"data":movielist[:limit]}
    
# https:/127.0.0.1:8000/api/v1/titles/{name}
# Path Param
@api.get("/api/v1/titles/{name}")
async def read_title(name:str):
    """Return a Movie of List of Movies/Shows"""
    currentTitle=[item for item in movielist if item['title']==name.title() ]
    return {"data":currentTitle}


# https:/127.0.0.1:8000/api/v1/titles/{show_id}
# Path Param
@api.get("/api/v1/titles/{show_id}")
async def read_title_by_show_id(show_id:str):
    """Return a Movie of List of Movies/Shows"""
    currentTitle=[item for item in movielist if item['show_id']==name.title() ]
    return {"data":currentTitle}
    
# https:/127.0.0.1:8000/api/v1/titles/{name}/{key}
# Path Param
@api.get("/api/v1/titles/{name}/{key}")
async def read_title_details(name:str,key:str):
    """Return a Movie of List of Movies/Shows"""
    currentTitle=[item for item in movielist if item['title']==name.title() ]
    curtrentTitleAttribute=currentTitle[0].get(key)
    return {"data":currentTitle}


# FastApi Templating
#Location for the html
templates=Jinja2Templates(directory='templates/docs')
@api.get("/",response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse('docs_fastapi.html',{'request':request})

@api.get("/mlpredict",response_class=HTMLResponse)
async def mlpredict_title(request:Request):
    prediction=MODEL.predict([searchterm])
    return templates.TemplateResponse('docs_fastapi.html',{'request':request,'results':prediction,"searchTerm":searchTerm})
    

# Flask Section
@flask_app.route('/')
def blog_page():
    return render_template("index.html")

@flask_app.route('/about')
def about_page():
    return render_template("about.html")

if __name__=='__main__':
    uvicorn.run(api,host='127.0.0.1',port=8000)

