import websockets
import asyncio
import PySimpleGUI as sg

class Fuzzer:

    def open_fuzz_window(self, main_window_values):
        self.main_window_values = main_window_values
        try:
            toprow = ['Sender', 'Payload', 'Length']
            tbl1 = sg.Table(headings=toprow, values=[],
            key="--Table--",
            auto_size_columns=False,
            col_widths=[10,50,10],
            display_row_numbers=False,
            enable_events=True,
            justification='left',
            selected_row_colors='red on yellow',
            num_rows=30,
            )
            layout = [[sg.Text("Fuzz List", key="new")],
            [sg.Button('Run'),tbl1]]
            # Create second window
            self.window2 = sg.Window("Fuzz List", layout, modal=True, size=(800,400), resizable=True)
            while True:
                self.event, values = self.window2.read()
                if self.event == "Exit" or self.event == sg.WIN_CLOSED:
                    break
                elif self.event == 'Run':
                    asyncio.run(self.fuzz())
        except Exception as err:
            print("Error: Could not run modal, ", err)

    async def fuzz(self):
        try:
            conn_str = "Connection Started, "+self.main_window_values["-WSS-"]
            self.update_table("Client", conn_str, self.window2)
            async with websockets.connect(self.main_window_values["-WSS-"]) as websocket:
                # Testing connection
                self.update_table("Client", "", self.window2)
                await websocket.send("")
                self.update_table("Server", await websocket.recv(), self.window2)

                # Open fuzzlist
                fuzzfile = open(self.main_window_values['-IN-'], "r")
                while fuzzfile:
                    line = fuzzfile.readline()
                    if line == "":
                        break
                    ws_msg = self.insert_line_into_body(line)
                    self.update_table("Client", ws_msg, self.window2)
                    await websocket.send(ws_msg)
                    self.update_table("Server", await websocket.recv(), self.window2)
                    # Time delay that was added in main window, convert to float
                    await asyncio.sleep(float(int(self.main_window_values['-DELAY-'])/1000))
                fuzzfile.close() 
        except Exception as err:
            print("Error: in fuzz def, ", err)

    def update_table(self, sender, msg, window2):
        msg_len = len(msg) if msg != "" else 0
        lists = [sender, msg, str(msg_len)]
        window2["--Table--"].Widget.insert('','end',values=lists)
        window2.refresh()

    def insert_line_into_body(self, line):
        index1 = self.main_window_values['-Body-'].index("§",0)
        index2 = self.main_window_values['-Body-'].index("§",index1+1)
        line = line.replace('\n', '')
        return self.main_window_values['-Body-'][:index1]+line+self.main_window_values['-Body-'][index2+1:]