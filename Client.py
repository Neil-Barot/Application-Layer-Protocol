import socket
import sys


serverIP = ""
serverPort = 31249

renderIP = ""
renderPort = 31250

HEADERSIZE = 10

DEFAULT_SEG_SIZE = 256

COMMANDS = ["list","render","pause","resume","restart","exit"]

def main():
    ###
    #serverIP = input("Server IP: ")
    #serverPort = int(input("Server Port: "))
    #renderIP = input("Renderer IP: ")
    #renderPort = int(input("Renderer Port: "))
    ###

    r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ##r.connect((renderIP, renderPort))
    r.connect((renderIP, 31250)) # For testing on local host

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ##s.connect((renderIP, renderPort))
    s.connect((serverIP, 31249)) # For testing on local host
    sendMsg(s, "controller connected")

    userInput = ""
    while True:
        userInput = inputCommand()

        ## Whole thing is pretty much broke. Fix it by adding in the separate commands again
        if userInput == "exit":
            sendMsg(r,"exit")
            break
        elif userInput == "render":
            # Tells renderer to render a certain file
            sendMsg(r,"render")
            userInput = input("Input file to render: ")
            sendMsg(r,userInput)
            ##print(recieveMsg(r)) # commented to see if rendering can be done in renderer
            ###
            #message = recieveMsg(r)
            #if message.lower() == "invalid":
                #print("Invalid filename")
            ###
        elif userInput == "list": 
            sendMsg(s,userInput)
            print(recieveMsg(s))
        elif userInput == "pause" or userInput == "resume" or userInput == "restart":
            sendMsg(r, userInput)
    r.close()

def inputCommand() -> str: # ensures a valid command is input at call, also ensures it is in lowercase
    printCommands()
    cm = input("Input Command: ").lower()

    while cm not in COMMANDS:
        printCommands()
        cm = input("Invalid command, Input command: ")
        

    return cm

def printCommands():
    print("Avalible commands:\n")
    line = "\t"
    for s in COMMANDS:
        line += s + " "
    print(line+"\n")

def recieveMsg(sock:socket.socket)-> str:
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

def sendMsg(sock:socket.socket, message:str):
    msg = f"{len(message):<{HEADERSIZE}}" + message
    sock.send(msg.encode())

if __name__ == "__main__":
    print("test")
    if(len(sys.argv) != 3):
        print("Invalid arguments, try Client.py <Server IP> <Renderer IP>")
        exit()
    else:
        serverIP = sys.argv[1]
        renderIP = sys.argv[2]
        
    main()