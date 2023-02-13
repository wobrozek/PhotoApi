from fastapi import FastAPI
from fastapi.responses import FileResponse
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
    banerBgColor: str
    banerFontColor: str

app=FastAPI()

# @app.get("/pdf/{id}")
# def downloadPdf(id:str):
#     with open(f"userPhotos/{id}/photos.pdf", "rb") as pdf_file:
#         encodedBase64= base64.b64encode(pdf_file.read())
#         return {"pdf":encodedBase64}
#     return {"error":"wrongId"}

@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

@app.get("/pdf/{id}")
async def get_pdf(id: str):
    return FileResponse(f"userPhotos/{id}/photos.pdf")

@app.post("/pdf")
async def createPdf(data:dataPDF):
    idFolder=uuid.uuid1()
    os.mkdir(f"userPhotos/{str(idFolder)}")
    for id,img in enumerate(data.images):
        with open(f"userPhotos/{idFolder}/img{id}.jpg", "wb") as image_file:
            image_file.write(base64.b64decode((img)))

    generatePDF(idFolder,data.banerName,data.banerBgColor,data.banerFontColor)
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

    def setBackground(self,bgColor,idFolderu):
        img = Image.new('RGB', (210, 297),bgColor )
        img.save(f"userPhotos/{idFolderu}/bg_bgColor.png")

        # adding image to pdf page that e created using fpdf
        self.image(f"userPhotos/{idFolderu}/bg_bgColor.png", x=0, y=0, w=210, h=297, type='', link='')


def generatePDF(idFolderu,text,bgColor,fontColor):

    fontRGB=ImageColor.getcolor(fontColor,"RGB")
    pdf=PDF()
    pdf.add_page()
    pdf.setBackground(bgColor,idFolderu)
    pdf.set_text_color(fontRGB[0],fontRGB[1],fontRGB[2])
    pdf.set_font("helvetica","",40)
    y=pdf.photosColumn(idFolderu,0)-5
    pdf.baner(text, y, 84,104)
    pdf.photosColumn(idFolderu, 105)
    pdf.baner(text, y, 185,0)
    pdf.output(f"userPhotos/{idFolderu}/photos.pdf")