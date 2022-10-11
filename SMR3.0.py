import os
import PySimpleGUI as sg
import cv2

whichCam = 0

def main():
    sg.theme("DarkAmber")
    
    cam = cv2.VideoCapture(whichCam)
    height, width, layers = cam.read()[1].shape
    outputFile = os.path.dirname(__file__) + "\SMROutput.mp4"
    video = cv2.VideoWriter(outputFile, -1, 1, (width, height))

    def Capture(i):
        print("Capturing {} ... ".format(i), end="")
        video.write(cam.read()[1])
        print("done")

    layout = [
        [sg.Text("Preview Scale: "), sg.Slider(range=(0, 1), default_value=0.5, size=(30, 10), orientation="horizontal", resolution=0.01 , key="-ScaleSlider-")],
        [sg.Image(key="-IMAGE-")],
        [sg.Button("Capture"), sg.Button("Render")]
    ]

    window = sg.Window("Stop Motion Recorder 3.0", layout)

    i = -1
    while True:
        event, values = window.read(timeout=20)

        if event == sg.WIN_CLOSED or event == "Render":
            break

        ret, frame = cam.read()
        frame = cv2.resize(src=frame, dsize=((int)(width * values["-ScaleSlider-"]), (int)(height * values["-ScaleSlider-"])))
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)

        if event == "Capture":
            i = i + 1
            Capture(i)

    video.release()
    window.close()

main()
