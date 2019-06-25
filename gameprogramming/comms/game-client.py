import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.on('message')
def my_message(data):
    if(data['sender']!=sio.sid):
        print('\n',data['sender']+": ", data['echo'])
#sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

def run():
    sio.connect('http://localhost:5000')
    i = ""

    while i is not "q":
        sio.
        mes = input("You:")
        sio.emit('update', mes)
    sio.wait()

if __name__=="__main__":
    run()
