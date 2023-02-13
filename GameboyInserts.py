"""Program to build a Insert for Gameboy Games in Cassette Cases."""
import customtkinter
import tkinter as tk
import sys
import os
from fpdf import FPDF
from PIL import Image, ImageTk
from tkinter import filedialog, colorchooser, messagebox


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("700x400")

insert = Image.new('RGB', (1030, 1030))
insert.save('tempInsert.jpg')
previewImage = Image.open(r"tempInsert.jpg")
previewImageTK = ImageTk.PhotoImage(previewImage)
previewImageLabel = tk.Label(image=previewImageTK, width=360, height=360)
previewImageLabel.place(anchor="center", x=500, y=200)

coverImagePath = ""
spineImagePath = ""
backcoverImagePath = ""

modelSelection = "Gameboy"
publisherSelection = "Nintendo"
backgroundColor = (128, 128, 128)

publisherOptions = {
    "Nintendo": resource_path(r"templateImages\Nintendo.png"),
    "THQ": resource_path(r"templateImages\THQ.png"),
    "Konami": resource_path(r"templateImages\Konami.png"),
    "Select File": ""
}

coverStrech = tk.StringVar()
spineStrech = tk.StringVar()
backStrech = tk.StringVar()


def createPreview():
    """Create a preview of the generated Insert"""
    global previewImage, previewImageTK, previewImageLabel, coverImagePath, spineImagePath, backcoverImagePath, insert

    backIm = Image.new('RGB', (253, 1030), color=backgroundColor)
    spineIm = Image.new('RGB', (127, 1030), color=backgroundColor)
    coverIm = Image.new('RGB', (650, 1030), color=backgroundColor)

    # handles resizing and streching of images
    if coverImagePath != "":
        if coverStrech.get() == "on":
            coverImage = Image.open(coverImagePath).resize((650, 837))
            hPlacement = 132
        else:
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
        if spineStrech.get() == "on":
            spineImage = Image.open(spineImagePath).rotate(
                270, Image.Resampling.NEAREST, expand=1)
            spineImage = spineImage.resize((127, 749))
            hPlacement = 260
        else:
            basewidth = 127
            spineImage = Image.open(spineImagePath).rotate(
                270, Image.Resampling.NEAREST, expand=1)
            wPercent = (basewidth/float(spineImage.size[0]))
            hSize = int((float(spineImage.size[1])*float(wPercent)))
            spineImage = spineImage.resize((basewidth, hSize))
            hPlacement = int((749 - hSize) / 2 + 260)
        try:
            spineIm.paste(spineImage, (0, hPlacement), spineImage)
        except:
            spineIm.paste(spineImage, (0, hPlacement))
    if backcoverImagePath != "":
        if backStrech.get() == "on":
            backImage = Image.open(backcoverImagePath).resize((253, 1030))
            hPlacement = 0
        else:
            basewidth = 253
            backImage = Image.open(backcoverImagePath)
            wPercent = (basewidth/float(backImage.size[0]))
            hSize = int((float(backImage.size[1])*float(wPercent)))
            backImage = backImage.resize((basewidth, hSize))
        try:
            backIm.paste(backImage, (0, 0), backImage)
        except:
            backIm.paste(backImage, (0, 0))

    bottom = Image.open(resource_path(r"templateImages\Down.png")).resize((650, 61))
    bottomSpline = bottom.crop((0, 0, 127, 61))
    coverIm.paste(bottom, (0, 969))
    spineIm.paste(bottomSpline, (0, 969))

    # Sets the Banner and Spline configs for the dropdown
    match modelSelection:
        case "Gameboy":
            banner = Image.open(
                resource_path(r"templateImages\GameboyBanner.png")).resize((650, 132))
            spineBanner = Image.open(
                resource_path(r"templateImages\GameboySpline.png")).resize((127, 260))
        case "Gameboy Color":
            banner = Image.open(
                resource_path(r"templateImages\GameboyColorBanner.png")).resize((650, 132))
            spineBanner = Image.open(
                resource_path(r"templateImages\GameboyColorSpline.png")).resize((127, 260))
        case "Gameboy Advance":
            banner = Image.open(
                resource_path(r"templateImages\GameboyAdvanceBanner.png")).resize((650, 153))
            spineBanner = Image.open(
                resource_path(r"templateImages\GameboyAdvanceSpline.png")).resize((127, 260))

    coverIm.paste(banner, (0, 0), banner)
    spineIm.paste(spineBanner)

    # publisher Logo
    logo = Image.open(publisherOptions[publisherSelection])
    if logo.size[1]*2.5 > logo.size[0]:
        baseheight = 40
        hPercent = (baseheight/float(logo.size[1]))
        wSize = int((float(logo.size[0])*float(hPercent)))
        logo = logo.resize((wSize, baseheight))
        xPlacement = (127-wSize)//2
        yPlacement = 980
    else:
        basewidth = 100
        wPercent = (basewidth/float(logo.size[0]))
        hSize = int((float(logo.size[1])*float(wPercent)))
        logo = logo.resize((basewidth, hSize))
        xPlacement = 13
        yPlacement = int((61 - hSize) / 2 + 969)
    try:
        spineIm.paste(logo, (xPlacement, yPlacement), logo)
    except:
        spineIm.paste(logo, (xPlacement, yPlacement))

    images = [backIm, spineIm, coverIm]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    insert = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        insert.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    insert.save('tempInsert.jpg')
    insert.resize((360, 360))
    previewImage = Image.open(r"tempInsert.jpg").resize((360, 360))
    previewImageTK = ImageTk.PhotoImage(previewImage)
    previewImageLabel.configure(image=previewImageTK)


def publisherSelectionCallback(choice):
    global publisherSelection
    if choice == "Select File":
        publisherSelection = choice
        select_file("publisher")
    else:
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

            # estimates the dominant color in the image and sets it as background color
            img = Image.open(coverImagePath)
            img = img.convert("RGB")
            backgroundColor = img.getpixel((0, img.height//2))
        case "spineImagePath":
            spineImagePath = filename
        case "backcoverImagePath":
            backcoverImagePath = filename
        case "publisher":
            publisherOptions["Select File"] = filename

    createPreview()


def choose_color():
    """Opens default Windows color picking menu and saves it as lable background color."""
    global backgroundColor

    color_code = colorchooser.askcolor(title="Choose color")
    backgroundColor = color_code[0]
    createPreview()


def exportPDF():
    """Saves lable shown in the Preview as printable PDF."""
    global insert

    root.filename = filedialog.askdirectory(initialdir="/")
    insert.save("temp.jpg")
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.image('temp.jpg', w=103, h=103)
    pdf.output(root.filename + r"/insert.pdf")
    os.remove("temp.jpg")


def on_closing():
    """Deletes the temporary file on close."""
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        os.remove("tempInsert.jpg")
        root.destroy()


coverButton = customtkinter.CTkButton(
    root, text="Cover", command=lambda: select_file("coverImagePath"))
coverButton.place(anchor="center", x=80, y=57)
coverStrechCheckbox = customtkinter.CTkCheckBox(
    master=root, text="Strech Cover", variable=coverStrech, onvalue="on", offvalue="off", command=createPreview)
coverStrechCheckbox.place(anchor="center", x=230, y=57)

spineButton = customtkinter.CTkButton(
    root, text="Spline", command=lambda: select_file("spineImagePath"))
spineButton.place(anchor="center", x=80, y=114)
spineStrechCheckbox = customtkinter.CTkCheckBox(
    master=root, text="Strech Spine", variable=spineStrech, onvalue="on", offvalue="off", command=createPreview)
spineStrechCheckbox.place(anchor="center", x=230, y=114)

backButton = customtkinter.CTkButton(
    root, text="Back", command=lambda: select_file("backcoverImagePath"))
backButton.place(anchor="center", x=80, y=171)
backStrechCheckbox = customtkinter.CTkCheckBox(
    master=root, text="Strech Back", variable=backStrech, onvalue="on",  offvalue="off", command=createPreview)
backStrechCheckbox.place(anchor="center", x=230, y=171)

platform = customtkinter.CTkOptionMenu(root, values=[
                                       "Gameboy", "Gameboy Color", "Gameboy Advance"], command=modelSelectionCallback)
platform.place(anchor="center", x=80, y=228)

platform = customtkinter.CTkOptionMenu(root, values=list(
    publisherOptions.keys()), command=publisherSelectionCallback)
platform.place(anchor="center", x=230, y=228)

colorSelector = customtkinter.CTkButton(
    root, text="Background Color", command=choose_color)
colorSelector.place(anchor="center", x=80, y=285)

pdfExport = customtkinter.CTkButton(root, text="Export PDF", command=exportPDF)
pdfExport.place(anchor="center", x=80, y=342)


# creates the preview Image that will be shown at starup
createPreview()

# start the customTkinter GUI
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
