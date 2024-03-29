from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import os

# Load env vars
if os.environ.get("CLOUD_PROJECT_ID", "none") == "none":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path=".env")

CLOUD_PROJECT_ID = os.environ.get("CLOUD_PROJECT_ID", "no_set")
DATA_BASE_ID = os.environ.get("DATA_BASE_ID", "no_set")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = firestore.Client(project=CLOUD_PROJECT_ID, database=DATA_BASE_ID)

@app.get("/")
async def root():
  return {"message": "Hello, World!"}

@app.get("/projects/")
async def projectsEndPoint(type: str = "", tldr: str = ""):
  collection = db.collection(u'projects')
  if not type == "":
    if tldr == "":
      documents = collection.where(filter=FieldFilter("public","==",True)).where(filter=FieldFilter("type", "array_contains_any", type.split(","))).order_by("priority")
      proyects = []
      for document in documents.stream():
        proyects.append(document.to_dict())
      return proyects
    else:
      tldr_document = db.collection(u'tldr').document(tldr).get()
      projects = []
      if tldr_document.exists:
        tldr = tldr_document.to_dict()
        for document_id in tldr["projects"]:
          project = collection.document(document_id).get().to_dict()
          if not project == None and type in project["type"]:
            projects.append(project)
      return projects
      


@app.get("/experiences/")
async def experiencesEndPoint():
  collection = db.collection(u'experiences')
  if not type == "":
    documents = collection.where(filter=FieldFilter("public","==",True)).order_by("priority")
  experiencies = []
  for document in documents.stream():
    experiencies.append(document.to_dict())

  return experiencies

@app.get("/courses/")
async def coursesEndPoint():
  collection = db.collection(u'courses')
  if not type == "":
    documents = collection.where(filter=FieldFilter("public","==",True)).order_by("priority")
  courses = []
  for document in documents.stream():
    courses.append(document.to_dict())

  return courses

@app.get("/skills/")
async def skillsEndPoint():
  collection = db.collection(u'skills')
  if not type == "":
    documents = collection.where(filter=FieldFilter("public","==",True)).order_by("priority")
  skills = []
  for document in documents.stream():
    skills.append(document.to_dict())

  return skills

@app.get("/interviews/")
async def interviewsEndPoint():
  collection = db.collection(u'interviews')
  if not type == "":
    documents = collection.where(filter=FieldFilter("public","==",True)).order_by("priority")
  interviews = []
  for document in documents.stream():
    interviews.append(document.to_dict())

  return interviews

@app.get("/posts/")
async def postsEndPoint(id: str = ""):
  if id == "":
    collection = db.collection(u'posts')
    documents = collection.where(filter=FieldFilter("public","==",True))
    posts = []
    for document in documents.stream():
      post = document.to_dict()
      post["id"] = document.id
      posts.append(post)
    return posts
  else:
    document = db.collection(u'posts').document(id).get().to_dict()
    return document

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
