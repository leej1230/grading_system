import PySimpleGUI as sg
import utils
import os
from screeninfo import get_monitors

monitor = get_monitors()[0]
WINDOW_SIZE = (monitor.width, monitor.height)

sg.theme('Dark Brown')
IMG_OUTPUT_DIR = 'page_cache'



image_filenames = utils.get_image_filenames()

images_layout = [
    [sg.Image(filename=os.path.join(IMG_OUTPUT_DIR, image), size=(None, None))]
    for image in image_filenames
]

score_layout = [
    [sg.Text('Score')],
    [sg.InputText(key='report_score')]
]

comment_layout = [
    [sg.Text('Comment')],
    [sg.InputText(key='report_comment')]
]

input_layout = [
    sg.Column(score_layout),
    sg.Column(comment_layout)
]

layout = [
    [sg.Text('Hello World!!')],
    [sg.Column(images_layout, scrollable=True, vertical_scroll_only=True, size=(WINDOW_SIZE[0], int(WINDOW_SIZE[1]*0.7)))],
    [sg.Frame('Input Grades', [input_layout])],
    [sg.Button("Exit")]
]

window = sg.Window('Report Grader', layout, resizable=True, finalize=True, size=WINDOW_SIZE)

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break

window.close()