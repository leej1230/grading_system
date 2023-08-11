from screeninfo import get_monitors
import PySimpleGUI as sg
import base64
import utils
import sys

icon_base64 = base64.b64decode(open('icon.txt', "r").read())

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
    if not current_sid:
        print('ERROR: You have completed grading!')
        sys.exit()

img = utils.convert_pdf_to_images(current_file, first=True)
while not img:
    utils.update_grade(current_sid, '0', 'FILE CORRUPTED')
    current_sid,current_file = utils.get_sid_with_file()
    if not current_sid:
        print('ERROR: You have completed grading!')
        sys.exit()
    while not current_file:
        utils.update_grade(current_sid, '0', 'FILE NOT EXIST')
        current_sid,current_file = utils.get_sid_with_file()
        if not current_sid:
            print('ERROR: You have completed grading!')
            sys.exit()
image_elem = sg.Image(data=img, size=(WINDOW_SIZE[0], None), key='-IMAGE-')

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
    [sg.Text(f'{utils.len_ungraded()} more reports to go!!', font=(None,TEXT_FONT_SIZE), key='-TITLE-')],
    # [image_elem],
    [sg.Column([[image_elem]], scrollable=True, vertical_scroll_only=True, size=(WINDOW_SIZE[0], int(WINDOW_SIZE[1] * 0.7)))],
    # [sg.Image(data=img, size=(WINDOW_SIZE[0], int(WINDOW_SIZE[1]*0.7)), key='-IMAGE-')],
    [sg.Frame('Input Grades', [input_layout], size=(WINDOW_SIZE[0],int(WINDOW_SIZE[1]*0.3)), font=(None,TEXT_FONT_SIZE))],
]

window = sg.Window('Report Grader', layout, resizable=True, finalize=True, size=WINDOW_SIZE, icon=icon_base64)

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Submit Score':
        # Retrieve score
        submitted_score = '0' if not values['report_score'] else values['report_score']
        submitted_comment = '' if not values['report_comment'] else values['report_comment']

        # Record the score
        utils.update_grade(current_sid, submitted_score, submitted_comment)

        # Reset comment input
        window['report_comment'].update('')

        current_sid,current_file = utils.get_sid_with_file()

        if not current_sid:
            sg.popup(f'You have finish grading!')
            sys.exit()
        while not current_file:
            utils.update_grade(current_sid, '0', 'FILE NOT EXIST')
            current_sid,current_file = utils.get_sid_with_file()
            if not current_sid:
                sg.popup(f'You have finish grading!')
                sys.exit()

        img = utils.convert_pdf_to_images(current_file)
        while not img:
            utils.update_grade(current_sid, '0', 'FILE CORRUPTED')
            current_sid,current_file = utils.get_sid_with_file()
            if not current_sid:
                sg.popup(f'You have finish grading!')
                sys.exit()
            while not current_file:
                utils.update_grade(current_sid, '0', 'FILE NOT EXIST')
                current_sid,current_file = utils.get_sid_with_file()
                if not current_sid:
                    sg.popup(f'You have finish grading!')
                    sys.exit()
        window['-IMAGE-'].update(data=img, size=(WINDOW_SIZE[0], None))
        window['-TITLE-'].update(f'{utils.len_ungraded()} more reports to go!!', font=(None,TEXT_FONT_SIZE))

window.close()