from screeninfo import get_monitors
import PySimpleGUI as sg
import utils
import sys
import os

# Choosing Theme
sg.theme('Dark Brown')

# Get monitor size
monitor = get_monitors()[0]
WINDOW_SIZE = (monitor.width, monitor.height)

TEXT_FONT_SIZE = 20
IMG_OUTPUT_DIR = 'page_cache'

# Initialize
current_sid,current_file = utils.get_sid_with_file()
if not current_sid:
    print('ERROR: You have completed grading!')
    sys.exit()
while not current_file:
    utils.update_grade(current_sid, '0', 'FILE NOT EXIST')
    current_sid,current_file = utils.get_sid_with_file()
if not current_file:
    print('ERROR: You have completed grading!')
    sys.exit()

utils.convert_pdf_to_images(current_file)
image_filenames = utils.get_image_filenames()

images_layout = [
    [sg.Image(filename=os.path.join(IMG_OUTPUT_DIR, image), size=(None, None))]
    for image in image_filenames
]

score_layout = [
    [sg.Text('Score', font=(None,TEXT_FONT_SIZE))],
    [sg.InputText(key='report_score', font=(None,TEXT_FONT_SIZE))]
]

comment_layout = [
    [sg.Text('Comment', font=(None,TEXT_FONT_SIZE))],
    [sg.InputText(key='report_comment', font=(None,TEXT_FONT_SIZE))]
]

input_layout = [
    sg.Column(score_layout),
    sg.Column(comment_layout),
    sg.Button('Submit Score', font=(None,TEXT_FONT_SIZE))
]

layout = [
    [sg.Text('Hello World!!')],
    [sg.Column(images_layout, scrollable=True, vertical_scroll_only=True, size=(WINDOW_SIZE[0], int(WINDOW_SIZE[1]*0.7)))],
    [sg.Frame('Input Grades', [input_layout], size=(WINDOW_SIZE[0],int(WINDOW_SIZE[1]*0.3)), font=(None,TEXT_FONT_SIZE))],
]

window = sg.Window('Report Grader', layout, resizable=True, finalize=True, size=WINDOW_SIZE)

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Submit Score':
        submitted_score = values['report_score']
        submitted_comment = values['report_comment']
        sg.popup(f'Score you submitted: {submitted_score}, Comment you submitted: {submitted_comment}')

window.close()