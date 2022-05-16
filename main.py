from xml.dom.minidom import Document
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from google.cloud import firestore

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = firestore.Client()

@app.get("/")
async def root():
  return {"message": "Hello, World!"}

@app.get("/projects/")
async def projectsEndPoint(type: str = ""):
  print(type)
  resources = db.collection(u'projects').where("type", "==", type).stream()
  documents = []
  for resource in resources:
    documents.append(resource.to_dict())

  return documents
