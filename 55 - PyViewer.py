import PySimpleGUI as sg
import os.path
import PIL.Image
import io
import base64

def convert_to_bytes(file_or_bytes, resize=None):
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    preview_size = (400, 400)
    img.thumbnail(preview_size, PIL.Image.ANTIALIAS)

    
    if resize:
        new_width, new_height = resize
        scale = min(new_height/400, new_width/400)
        img = img.resize((int(400*scale), int(400*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    
    del img
    return bio.getvalue()

    

# Window layout, 2 columns

left_col = [
    [sg.Text("Folder"), sg.In(size=(25,1), enable_events=True, key="-FOLDER-"), sg.FolderBrowse()],
    [sg.Listbox(values=[], enable_events=True, size=(40,20), key="-FILE LIST-")],
    [sg.Text("Resize to"), sg.In(key="-W-", size=(5,1)), sg.In(key="-H-", size=(5,1))]
     ]

# Show name of the chosen file.
preview_col = [
    [sg.Text("Image preview")],
    [sg.Text(size=(40,1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")]
    ]

# Full layout.

layout = [
    [sg.Column(left_col, element_justification="c"), sg.VSeperator(), sg.Column(preview_col, element_justification="c")]
    ]

sg.theme("Light Blue")

# Create window.

window = sg.Window("PyViewer", layout, resizable=False)


# Event loop.

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Exit"):
        break
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [f for f in file_list if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp"))]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":
        try:
            filename = os.path.join(values["-FOLDER-"], values ["-FILE LIST-"][0])
            window["-TOUT-"].update(filename)
            if values["-W-"] and values["-H-"]:
                new_size = int(values["-W-"]), int(values["-H-"])
            else:
                new_size = None
            window["-IMAGE-"].update(data=convert_to_bytes(filename, resize = new_size))
        except Exception as E:
            print(f"**Error {E} **")
            pass
window.close()
