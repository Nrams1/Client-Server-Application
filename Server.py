import hashlib
import socket
import sys

BUFFER_SIZE = 1024
SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5070

def receiveFromSender():

    #connection
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket.bind((SERVER_HOST,SERVER_PORT))
    serverSocket.listen()
    print("waiting for connections.....")
    conn , address = serverSocket.accept()
    print("connected to client")

    # Protocol 
    header = conn.recv(BUFFER_SIZE).decode()
    headerSplit = header.split("/")

    fileName = "recv.pdf";
    key = headerSplit[1]
    fileHash = headerSplit[2]
    file_size = headerSplit[3]


    # Recieving The file
    with open(fileName ,'wb') as file:
            
            while True:
                byte_read = conn.recv(BUFFER_SIZE)

                if not byte_read:
                     break
                
                file.write(byte_read) 

    conn.close() # close connection 
    print("Connection to client closed") 

    # Compare Hash   & send confirmation
    if(hashFile(file.name)== fileHash):
        confirmation = 1
        # Store the file data : Filename , Key , Date , Size
        with open('Database.txt','w') as fileData:
            fileData.write(fileName+" "+key+" "+fileHash+" "+file_size)

    else :
            confirmation = 0

    sendToClient(confirmation)


def sendToClient(args):

    # connection
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket.bind((SERVER_HOST,SERVER_PORT+1))
    serverSocket.listen()
    conn , address = serverSocket.accept()
    print("connected to client")


    if (args==1 ):

        conn.send("File sent successfully".encode())   

    elif (args==0) :
         conn.send("File sent unsuccessfully".encode()) 

    elif (args=="download"):
    # Send file Download request

        fileName = conn.recv(BUFFER_SIZE).decode()

         
        with open('Database.txt' ,'rb') as fileData:

              
            for line in fileData:

                DataLine = line.decode().split(" ")
                file_name = DataLine[0]
                fileHash = DataLine[2]

                if (fileName == file_name):
                        break
                    
            
            conn.send(fileHash.encode())
      
            with open(file_name,'rb') as file:

                while True:
                    byte_read = file.read(BUFFER_SIZE)

                    if not byte_read:
                            break
                    
                    conn.sendall(byte_read)
                
            conn.close()

    elif(args=="list"):
         
        with open('Database.txt' ,'rb') as fileData:
                
                for line in fileData:

                    DataLine = line.decode().split(" ")
                    file_name = DataLine[0]
            #conn.recv(BUFFER_SIZE).decode()

def hashFile(FileName):
    
    sha1 = hashlib.sha1()
    with open(FileName , 'rb') as file:

        chunk = 0
        while chunk !=b'':
            chunk = file.read(BUFFER_SIZE)
            sha1.update(chunk)

            return sha1.hexdigest()
        
sendToClient("download")