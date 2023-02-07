from fastapi import FastAPI
from typing import List
import uuid
import base64
import glob
import os
from pydantic import BaseModel
from fpdf import FPDF
from PIL import Image,ImageColor

class dataPDF(BaseModel):
    images:List[str]
    banerName:str
    banerbgColor: str
    banerFontColor: str

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

    def baner(self,text,x,y,marginX):
        with self.rotation(270,105,105):
            self.set_xy(0,marginX)
            self.cell(x,22,text,align="c")

    def setBackground(self,bgColor):
        img = Image.new('RGB', (210, 297),bgColor )
        img.save('bg_bgColor.png')

        # adding image to pdf page that e created using fpdf
        self.image('bg_bgColor.png', x=0, y=0, w=210, h=297, type='', link='')


def generatePDF():
    idFolderu="3505c8ab-a6fa-11ed-8eb7-b655614b3591"
    text = "Bal wydzialowy MS"
    bgColor="#afeafe"
    fontColor="#fff"
    
    fontRGB=ImageColor.getcolor(fontColor,"RGB")

    pdf=PDF()
    pdf.add_page()
    pdf.setBackground(bgColor)
    pdf.set_text_color(fontRGB[0],fontRGB[1],fontRGB[2])
    pdf.set_font("helvetica","",40)
    y=pdf.photosColumn(idFolderu,0)-5
    pdf.baner(text, y, 84,104)
    pdf.photosColumn(idFolderu, 105)
    pdf.baner(text, y, 185,0)
    pdf.output(f"userPhotos/{idFolderu}/photos.pdf")

# function to create mocks
@app.get("/imgToBase64")
def photoToBase64():
    images =glob.glob("C:/Users/wobro/Desktop/mock/*")
    for id,img in enumerate(images):
        with open(img, "rb") as image_file:
            images[id] = base64.b64encode(image_file.read())

    return images