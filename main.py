from fastapi import FastAPI
from typing import List
import uuid
import base64
import glob
import os
from pydantic import BaseModel
from fpdf import FPDF
from PIL import Image

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
    def photosColumn(self,idFolder,x):
        images = glob.glob(f"userPhotos/{idFolder}/*.jpg")
        y=0

        for img in images:
            width,height=Image.open(img).size
            self.image(img, x=x, y=y, w=84)
            y+=84/width*height+5
        return y

    def baner(self,text,x,y,marginX,marginY):
        with self.rotation(270,marginX,marginY):
            # self.set_y(y)
            self.cell(x,22,text,1)


def generatePDF():
    idFolderu="3505c8ab-a6fa-11ed-8eb7-b655614b3591"
    pdf=PDF()
    pdf.add_page()
    pdf.set_font("helvetica","",40)
    y=pdf.photosColumn(idFolderu,0)
    pdf.baner("siema", y, 84,46,70)
    pdf.photosColumn(idFolderu, 105)
    pdf.baner("elo", y, 185,220,-5)
    pdf.output(f"userPhotos/{idFolderu}/photos.pdf")

# function to create mocks
@app.get("/imgToBase64")
def photoToBase64():
    images =glob.glob("C:/Users/wobro/Desktop/mock/*")
    for id,img in enumerate(images):
        with open(img, "rb") as image_file:
            images[id] = base64.b64encode(image_file.read())

    return images





