
import hashlib
import socket 
import os
import sys 

 
BUFFER_SIZE = 1024
SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5070

def sendToServer():

    # connection
    clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientSock.connect((SERVER_HOST,SERVER_PORT))
    print("connected to server")

    # Enter File to UPLOAD 
    file_name = "send.pdf"
    
    file_size = int(os.path.getsize(file_name))

    # Enter Key OR UP(Unprotected)
    key = "password"

    # Hashing
    fileHash = hashFile(file_name)


    # Protocol : Header 
    header = file_name +"/"+ key +"/" + fileHash +"/"+ str(file_size)
   
    clientSock.send(header.encode())

    # Transfer The file (Body)
    with open(file_name ,'rb') as file:

        while True:
            byte_read = file.read(BUFFER_SIZE)

            if not byte_read:
                 break
            
            clientSock.sendall(byte_read)

    clientSock.close() # close connection
    print("Connection to server closed")
    # receieve Confirmation
    receiveFromServer("confirmation")
   
def receiveFromServer(arg):

    #connection
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientSocket.connect((SERVER_HOST,SERVER_PORT+1))
    print("waiting for connections.....")
    
    print("connected to server")

    if(arg=="confirmation"):
        confirmation = clientSocket.recv(BUFFER_SIZE).decode()
        print(confirmation)

    elif(arg=="download"):

        file_name = "recv.pdf"

        clientSocket.send(file_name.encode())
        fileHash = clientSocket.recv(BUFFER_SIZE).decode()

        with open("send.pdf" ,'wb') as file:
             
             while True:
                byte_read = clientSocket.recv(BUFFER_SIZE)

                if not byte_read:
                        break
                
                file.write(byte_read) 

        clientSocket.close()

        if(hashFile(file.name)==fileHash):
            #Send Confirmation and Store File Information
            confirmation = "file Recieved successfully"
        else :
                confirmation ="file not recieved"

        print(confirmation)

    elif (arg=="list"):
         a=""
         #clientSocket.send("list".encode())
   

def hashFile(FileName):
    
    sha1 = hashlib.sha1()
    with open(FileName , 'rb') as file:

        chunk = 0
        while chunk !=b'':
            chunk = file.read(BUFFER_SIZE)
            sha1.update(chunk)

            return sha1.hexdigest()


receiveFromServer("download")
