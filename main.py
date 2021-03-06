from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import firestore

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

@app.get("/experiences/")
async def experiencesEndPoint():
  collection = db.collection(u'experiences')
  if not type == "":
    documents = collection.where("public","==",True).order_by("priority")
  experiencies = []
  for document in documents.stream():
    experiencies.append(document.to_dict())

  return experiencies

@app.get("/courses/")
async def coursesEndPoint():
  collection = db.collection(u'courses')
  if not type == "":
    documents = collection.where("public","==",True).order_by("priority")
  courses = []
  for document in documents.stream():
    courses.append(document.to_dict())

  return courses

@app.get("/skills/")
async def skillsEndPoint():
  collection = db.collection(u'skills')
  if not type == "":
    documents = collection.where("public","==",True).order_by("priority")
  skills = []
  for document in documents.stream():
    skills.append(document.to_dict())

  return skills

@app.get("/interviews/")
async def interviewsEndPoint():
  collection = db.collection(u'interviews')
  if not type == "":
    documents = collection.where("public","==",True).order_by("priority")
  interviews = []
  for document in documents.stream():
    interviews.append(document.to_dict())

  return interviews

@app.get("/beers/")
async def beersEndPoint():
  doc = db.collection(u'beers').document(u'count')
  count = doc.get().to_dict()

  return count

@app.get("/subtrack/")
async def subtrackEndPoint():
  doc = db.collection(u'beers').document(u'count')
  doc.update({u'left': firestore.Increment(-1)})
  
  return "hi"
