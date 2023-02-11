"""Program to build a Insert for Gameboy Games in Cassette Cases."""
import customtkinter
import tkinter as tk
import sys
import os
from fpdf import FPDF
from PIL import Image, ImageTk
from tkinter import filedialog, colorchooser, messagebox

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

dir = os.getcwd()

root = customtkinter.CTk()
root.geometry("600x400")

insert = Image.new('RGB', (1030, 1030))
insert.save('test.jpg')
previewImage = Image.open(r"test.jpg")
previewImageTK = ImageTk.PhotoImage(previewImage)
previewImageLabel = tk.Label(image=previewImageTK, width=360, height=360)
previewImageLabel.place(anchor="center", x=400, y=200)

coverImagePath = ""
spineImagePath = ""
backcoverImagePath = ""

modelSelection = "Gameboy"
publisherSelection = ""
backgroundColor = (128,128,128)

publisherOptions = {
    "Nintendo" : dir + r"\templateImages\Nintendo.png",
    "THQ" : dir + r"\templateImages\THQ.png",
    "Konami" : dir + r"\templateImages\Konami.png",
    "Select File" : ""
    }

def createPreview():
    global previewImage, previewImageTK, previewImageLabel, coverImagePath, spineImagePath, backcoverImagePath, insert
    backIm = Image.new('RGB', (253, 1030), color=backgroundColor)
    splineIm = Image.new('RGB', (127, 1030), color=backgroundColor)
    coverIm = Image.new('RGB', (650, 1030), color=backgroundColor)

    if coverImagePath != "":
        basewidth = 650
        coverImage = Image.open(coverImagePath)
        wPercent = (basewidth/float(coverImage.size[0]))
        hSize = int((float(coverImage.size[1])*float(wPercent)))
        coverImage = coverImage.resize((basewidth, hSize))
        hPlacement = int((837 - hSize) / 2 + 132)
        try:
            coverIm.paste(coverImage, (0, hPlacement), coverImage)
        except:
            coverIm.paste(coverImage, (0, hPlacement))
    if spineImagePath != "":
        basewidth = 127
        splineImage = Image.open(spineImagePath).rotate(270, Image.NEAREST, expand = 1)
        wPercent = (basewidth/float(splineImage.size[0]))
        hSize = int((float(splineImage.size[1])*float(wPercent)))
        splineImage = splineImage.resize((basewidth, hSize))
        hPlacement = int((749 - hSize) / 2 + 260)
        try:
            splineIm.paste(splineImage, (0, hPlacement), splineImage)
        except:
            splineIm.paste(splineImage, (0, hPlacement))
    if backcoverImagePath != "":
        basewidth = 253
        backImage = Image.open(backcoverImagePath)
        wPercent = (basewidth/float(backImage.size[0]))
        hSize = int((float(backImage.size[1])*float(wPercent)))
        backImage = backImage.resize((basewidth, hSize))
        try:
            backIm.paste(backImage, (0, 0), backImage)
        except:
            backIm.paste(backImage, (0, 0))

    bottom = Image.open(dir + r"\templateImages\Down.png").resize((650,61))
    bottomSpline = bottom.crop((0, 0, 127, 61))
    coverIm.paste(bottom, (0,969))
    splineIm.paste(bottomSpline, (0,969))

    match modelSelection:
        case "Gameboy":
            banner = Image.open(dir + r"\templateImages\GameboyBanner.png").resize((650,132))
            splineBanner = Image.open(dir + r"\templateImages\GameboySpline.png").resize((127,260))
        case "Gameboy Color":
            banner = Image.open(dir + r"\templateImages\GameboyColorBanner.png").resize((650,132))
            splineBanner = Image.open(dir + r"\templateImages\GameboyColorSpline.png").resize((127,260))
        case "Gameboy Advance":
            banner = Image.open(dir + r"\templateImages\GameboyAdvanceBanner.png").resize((650,153))
            splineBanner = Image.open(dir + r"\templateImages\GameboyAdvanceSpline.png").resize((127,260))
            
    coverIm.paste(banner, (0, 0), banner)
    splineIm.paste(splineBanner)


    images = [backIm, splineIm, coverIm]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    insert = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
      insert.paste(im, (x_offset,0))
      x_offset += im.size[0]

    insert.save('test.jpg')
    insert.resize((360,360))
    previewImage = Image.open(r"test.jpg").resize((360,360))
    previewImageTK = ImageTk.PhotoImage(previewImage)
    previewImageLabel.configure(image=previewImageTK)


def publisherSelectionCallback(choice):
    global publisherSelection
    publisherSelection = choice
    createPreview()

def modelSelectionCallback(choice):
    global modelSelection
    modelSelection = choice
    createPreview()

def select_file(position):
    """Opens File Explorer file selection and saves selected filepath to the varibale given in position."""
    global coverImagePath, spineImagePath, backcoverImagePath, backgroundColor
    
    filetypes = (
        ('Images', '.png .jpg .jpeg'),
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    match position:
        case "coverImagePath":
            coverImagePath = filename

            #estimates the dominant color in the image and sets it as background color
            img = Image.open(coverImagePath)
            img = img.convert("RGB")
            backgroundColor = img.getpixel((0, img.height//2))
        case "spineImagePath":
            spineImagePath = filename
        case "backcoverImagePath":
            backcoverImagePath = filename

    createPreview()

def choose_color():
    """Opens default Windows color picking menu and saves it as lable background color."""
    global backgroundColor

    color_code = colorchooser.askcolor(title ="Choose color")
    backgroundColor = color_code[0]
    createPreview()

def exportPDF():
    """Saves lable shown in the Preview as printable PDF."""
    global insert

    root.filename =  filedialog.askdirectory(initialdir = "/")
    insert.save("temp.jpg")
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.image('temp.jpg', w = 103, h = 103)
    pdf.output(root.filename + r"/insert.pdf")
    os.remove("temp.jpg")

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        os.remove("test.jpg")
        root.destroy()



coverButton = customtkinter.CTkButton(root, text="Cover", command= lambda: select_file("coverImagePath"))
coverButton.place(anchor="center", x=100, y=57)

splineButton = customtkinter.CTkButton(root, text="Spline", command= lambda: select_file("spineImagePath"))
splineButton.place(anchor="center", x=100, y=114)

backButton = customtkinter.CTkButton(root, text="Back", command= lambda: select_file("backcoverImagePath"))
backButton.place(anchor="center", x=100, y=171)

platformVariable = tk.StringVar(root)
platformVariable.set("Gameboy")
platform = customtkinter.CTkOptionMenu(root, values=["Gameboy", "Gameboy Color", "Gameboy Advance"], command=modelSelectionCallback)
platform.place(anchor="center", x=100, y=228)

colorSelector = customtkinter.CTkButton(root, text="Background Color", command = choose_color)
colorSelector.place(anchor="center", x=100, y=285)

pdfExport = customtkinter.CTkButton(root, text="Export PDF", command = exportPDF)
pdfExport.place(anchor="center", x=100, y=342)


#creates the preview Image that will be shown at starup
createPreview()




#start the customTkinter GUI
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()