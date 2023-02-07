from fastapi import FastAPI
from typing import List
import uuid
import base64
import glob
import os
from pydantic import BaseModel

class dataPDF(BaseModel):
    images:List[str]
    banerName:str
    banerColor: str

app=FastAPI()

@app.get("/pdf/{serieID}")
def downloadPdf():
    return {"name":"first data"}

@app.post("/images")
def createPdf(data:dataPDF):
    idFolder=uuid.uuid1()
    os.mkdir(str(idFolder))
    for id,img in enumerate(data.images):
        with open(f"userPhotos/{idFolder}/img{id}.jpg", "wb") as image_file:
            image_file.write(base64.b64decode((img)))

    return str(idFolder)

@app.get("/imgToBase64")
def photoToBase64():
    images =glob.glob("C:/Users/wobro/Desktop/mock/*")
    for id,img in enumerate(images):
        with open(img, "rb") as image_file:
            images[id] = base64.b64encode(image_file.read())

    return images





