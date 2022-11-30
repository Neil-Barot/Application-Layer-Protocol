import socket
import select
import os

HEADERSIZE = 10

def main():

    

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Binds the render to localhost port 1234
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((socket.gethostname(), 1249)) 
    s.listen(5)

    socketList = [s] # This is probably unecessary, but storing the list of all connected clients for now
    clients = {}

    while True:
        readSocket, _, excepSocket = select.select(socketList, [], socketList)
        for sock in readSocket:
            if sock == s:
                clientSocket, clientAddress = s.accept()
                print("client has been accepted") # Just for testing
                clientType = recieveMsg(clientSocket)
                print(clientType) # Just for testing
                if clientType == False:
                    print("Client has disconnected\n")
                    continue
                socketList.append(clientSocket)
                clients[clientSocket] = clientType
                #print statement kinda iffy, fix or delete
                #print('Accepted connection from {}:{}, From: {}'.format(*clientAddress, clientType['data'].decode('utf-8')))
            else:
                message = recieveMsg(sock)

                if message == False:
                    #print statement kinda iffy, fix or delete
                    #print('Closed connection from: {}'.format(clients[sock]['data'].decode('utf-8')))
                    print("Connection was forcibly closed")
                    socketList.remove(sock)
                    del clients[sock]
                    continue
                elif message.lower() == "sendlist":
                    ##sendMsg(sock, getMediaList())
                    sendMsg(sock, "Example list")
                elif message.lower() == "pause": # Figure out how to do this
                    print("pausing stream")
                elif message.lower() == "resume": # Figure out how to do this
                    print("resuming stream")
                elif message.lower() == "restart": # Figure out how to do this
                    print("restarting stream")
                else: # If none of the previous messages match, assume that message is filename to be rendered
                    print('rendering file {}'.format(message)) # send stream to renderer if file found, else send invalid to renderer



def recieveMsg(sock : socket.socket):
    try:
        fullMsg = ""
        msgLen = 0
        newMsg = True
        while True:
            msg = sock.recv(20)
            if newMsg:
                msgLen = int(msg[:HEADERSIZE])
                newMsg = False

            fullMsg += msg.decode("utf-8")

            if len(fullMsg) - HEADERSIZE == msgLen:
                return fullMsg[HEADERSIZE:]
    except:
        return False

def sendMsg(sock :socket.socket, message : str):
    msg = f"{len(message):<{HEADERSIZE}}" + message
    sock.send(bytes(msg,"utf-8"))

def getMediaList()-> str:
    
    fileList = os.listdir('files')

    dataList = ""

    #print(fileList)

    for str in fileList:
        dataList += str + "\n"
    #print(dataList)

    #print(f"sending list of {len(dataList)}...")

    return dataList
    # Returns a string of all media in a file

def getFile(filename :str):

    fileList = os.listdir('files')

    if(filename in fileList):

        print(f"File \'{filename}\' found...")
        path = "files/"+filename
        return open(path).read()
    else:
        return "File not found"
                    


if __name__ == "__main__":
    print(getMediaList())
    print(getFile('stuff.txt'))
    #main()