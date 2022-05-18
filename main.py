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
  collection = db.collection(u'projects')
  if not type == "":
    documents = collection.where("public","==",True).where("type", "array_contains_any", type.split(",")).order_by("priority")
  proyects = []
  for document in documents.stream():
    proyects.append(document.to_dict())

  return proyects
