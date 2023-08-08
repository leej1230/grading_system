import PySimpleGUI as sg

frame_ratio = 3

sg.theme('Dark Brown')

pdf_frame   = sg.Frame('',[], key='pdf_frame', size=(500, 700))
grade_frame = sg.Frame('',[], key='grade_frame')

# layout = [
#     [pdf_frame],
#     [grade_frame],
#     [sg.Button('Exit')]
# ]

layout = [
    [sg.Text('Hello World!!')],
    [sg.Column(
        layout=[
            [
                sg.Frame("Frame 1", layout=[
                    [sg.Text("Frame 1 content")],
                    [sg.Input()]
                ], expand_x=True, expand_y=True, key="-FRAME1-")  # Allow Frame 1 to expand vertically
            ],
            [
                sg.Frame("Frame 2", layout=[
                    [sg.Text("Frame 2 content")],
                    [sg.Button("Button")]
                ],expand_x=True, expand_y=True, key="-FRAME2-")  # Allow Frame 2 to expand vertically
            ]
        ],
        expand_x=True,
        expand_y=True,
        key="-COLUMN-"
    )],
    [sg.Button("Exit")]
]


window = sg.Window('Report Grader', layout, resizable=True, finalize=True)

# window["pdf_frame"].expand(expand_x=True)
# window["grade_frame"].expand(expand_x=True)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    # sg.theme(values['-LIST-'][0])
    # entered_text = sg.popup_get_text('This is {}'.format(values['-LIST-'][0]))
    # if entered_text:
    #     sg.popup('You Entered {}!'.format(entered_text))
    
    window_size = window.get_size()
    column_height = window_size[1]
    frame1_height = column_height * (1 / (frame_ratio + 1))
    frame2_height = column_height - frame1_height

    window["-FRAME1-"].update(size=(None, frame1_height))
    window["-FRAME2-"].update(size=(None, frame2_height))

window.close()