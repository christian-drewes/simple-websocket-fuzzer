import asyncio
 
import websockets
 
# create handler for each connection
 
async def handler(websocket, path):
    while True:
        try:
            data = await websocket.recv()
        except websockets.ConnectionClosed:
            print(f"Terminated connection")
            break
        print("Client sent, ", data)
 
        reply = f"Data recieved as:  {data}"
 
        await websocket.send(reply)
 
 
 
start_server = websockets.serve(handler, "localhost", 8000)
 
 
 
asyncio.get_event_loop().run_until_complete(start_server)
 
asyncio.get_event_loop().run_forever()