from fastapi import FastAPI
from typing import List
import uuid
import base64
import glob
import os
from pydantic import BaseModel
from fpdf import FPDF

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


class PDF(FPDF):
    def photo(self,id,idFolder,x_,y_):
        self.image(f"userPhotos/{idFolder}/img{id}.jpg",x=x_ ,y=y_,w=30)

def generatePDF():
    idFolderu="3505c8ab-a6fa-11ed-8eb7-b655614b3591"
    pdf=PDF()
    pdf.add_page()
    pdf.photo(0,idFolderu,0,0)
    pdf.photo(1, idFolderu, 0, 30)
    pdf.output(f"userPhotos/{idFolderu}/photos.pdf")

# function to create mocks
@app.get("/imgToBase64")
def photoToBase64():
    images =glob.glob("C:/Users/wobro/Desktop/mock/*")
    for id,img in enumerate(images):
        with open(img, "rb") as image_file:
            images[id] = base64.b64encode(image_file.read())

    return images





