from tkinter import SEL_FIRST, SEL_LAST
from fuzzer import Fuzzer
import PySimpleGUI as sg

def clear_sel_item():
    body_text = values["-Body-"].replace('§','')
    window["-Body-"].update(body_text)
    return body_text

def insert_sel_item(sel_text,x,y):
    body_text = clear_sel_item()
    window["-Body-"].update(body_text[:x]+f"§{sel_text}§"+body_text[y:])

def check_for_section():
    if values["-Body-"].count('§') == 0:
        sg.popup("There must be § in the body")
        return False
    else: 
        return True

if __name__ == '__main__':
    sg.theme('black')
    # Define the window's contents
    layout_l = [[sg.Text("Choose a fuzzlist: ")],
                [sg.Text("WSS Connection Address")],
                [sg.Text("Request delay (millisecs)")],
                [sg.Text("Body")]]
    layout_r = [[sg.Input(), sg.FileBrowse(key="-IN-")],
                [sg.Input(key="-WSS-", default_text="ws://localhost:8000")],
                [sg.Input(key="-DELAY-",default_text="0")],
                [sg.Multiline(key="-Body-", default_text = "§HERE§", s=(50, 5))],
                [sg.Button('Insert §'),sg.Button('Clear §')] ]
    layout = [[sg.Col(layout_l, p=5, vertical_alignment="t", element_justification='right'),sg.Col(layout_r, p=0)],
    [sg.Button('Fuzz It!')]]

    # Create the window
    window = sg.Window('Simple WebSocket Fuzzer', layout)
    get_sel_body = None

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event=="Exit":
            break
        if event == "Insert §":
            if window["-Body-"].Widget.tag_ranges('sel'):
                sel_range = window["-Body-"].Widget.tag_ranges('sel')
                get_sel_body = window["-Body-"].Widget.selection_get()
                insert_sel_item(get_sel_body, int(sel_range[0].string.split('.')[1]), int(sel_range[1].string.split('.')[1]))
        if event == "Clear §":
            clear_sel_item()
        if event == "Fuzz It!" and check_for_section():
            Fuzzer().open_fuzz_window(values)

