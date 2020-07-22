from socket import *
from threading import Thread

FILE_ACCOUNT="account.txt"

def Split(requestdata):
    list=requestdata.split("\r\n") 
    tmp=list[0].split(" ")
    dict["Method"]=tmp[0]
    dict["Url"]=tmp[1].lstrip("/")
    dict["Body"]=list[len(list)-1]
    return dict

def CheckExist(URL,account):
    f=open(URL,"r")
    data=f.read()
    f.close()
    list=data.split("\n")
    for i in list:
        tmp=i.split(" ")
        if(account==(tmp[0],tmp[1])):
            return True

    return False

def Account(Content):
    list=Content.split("&")
    user=list[0].split("=")[1]
    password=list[1].split("=")[1]
    return (user,password)

def MethodGet(URL):
    type=URL.split(".")[1]
    data = "HTTP/1.1 200 OK \r\n"
    if(type=="html"):
        data += "Content-Type: text/html; charset=utf-8 \r\n"
        URL="html/"+URL
    elif(type=="ico"):
        data += "Content-Type: image/x-icon; charset=utf-8 \r\n"
    elif(type=="jpg"):
        data += "Content-Type: image/jpeg; charset=utf-8 \r\n"
    elif(type=="png"):
        data += "Content-Type: image/png; charset=utf-8 \r\n"
    data+="\r\n"
    data=data.encode()  
    try:
        f=open(URL,"rb")
        data+=f.read()
        f.close()
    except: 
        data = "HTTP/1.1 404 OK \r\n"
        data=data.encode()
    
    return data

def MethodPost(Body):
    account=Account(Body)
    data = "HTTP/1.1 301 Moved Permanently \r\n"
    data += "Content-Type: text/html; charset=utf-8 \r\n"

    if(CheckExist(FILE_ACCOUNT,account)):
        data += "Location: /info.html"
    else:
        data += "Location: /404.html"
    data+="\r\n"
    return data.encode()

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        (Client,Client_addr)=Server.accept()
        
        Addresses[Client] = Client_addr
        Thread(target=handle_client, args=(Client,)).start()


def handle_client(Client):
    
    while True:
    
        #(Client,Client_addr)=Server.accept()
        
        rd= Client.recv(5000).decode()
        if(len(rd)<=0): continue
        dict=Split(rd)
        
        if(dict["Method"]=="GET"):
            data=MethodGet(dict["Url"])
        elif(dict["Method"]=="POST"):
            data=MethodPost(dict["Body"])

        Client.sendall(data)
        Client.shutdown(SHUT_WR)


#localhost:9000/index.html
Clients={}
Addresses={}
Server=socket(AF_INET,SOCK_STREAM)
HOST ="localhost"
PORT = 80
ADDR=(HOST,PORT)
try:
    Server.bind(ADDR)
except:
    ADDR=(HOST,9000)
    Server.bind(ADDR)
dict=dict()
if __name__ == "__main__":
    Server.listen(5)
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    Server.close()