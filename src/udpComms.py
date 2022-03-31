#!/usr/bin/env python3.10

#Created by Adithya Shastry

import socket
import pickle
import time

class UDPComms:
    '''
    This class will facilitate basic communications between the server running
    on the robot and any devices that are connected to that server
    '''

    def __init__(self,IP,PORT,Server):
        '''
        Parameters:
            - IP: the IP address of the device
            - Port: the post number to use for the UDP connection
            - Server: (Boolean) tells us if the device is a server or a client
        '''
        self.IP = IP
        self.PORT = PORT
        self.Server = Server
        self.connections = dict() #Will be used to keep a table of current connections

        #set up the socket
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #We will set a time out for the socket
        self.socket.settimeout(0.5)
        #Now we can bind the socket
        self.socket.bind((self.HOST,self.PORT)) 
    
    def send(self,MSG,IP,PORT):
        '''
        This method will send a message 
        Inputs:
            - MSG: the message to be sent
            - IP: IP of the destination device
            - PORT: Port of the destination device
        Output:
            - status of the message sent
        '''
        MSG = pickle.dumps(MSG)
        self.socket.sendto(MSG,(IP,PORT))
    def recieve(self):
        '''
        Will wait and recieve a message
        Output:
            - unpickled message
            - sender address
        '''
        data,senderAddress = self.socket.recvfrom(20 * 1024)
        data = pickle.loads(data)
        #The Address Tuple is of the form (IP,PORT)
        return data,senderAddress
    def secureSend(self,IP,PORT,MSG):
        '''
        Will try to send the message five times before timing out
        Inputs:
            - IP: the destination IP
            - PORT: destination port
            - MSG: message to send
        Output:
            - 100: if there was an error
            - 200: if the message was send succesfully
        '''
        #we want to first pickle the msg
        MSG = pickle.dumps(MSG)
        #then we want to try five times to send the message
        for i in range(5):
            #try to send the message
            self.send(MSG,IP,PORT)
            try:
                ACK,_ = self.recieve()
                if ACK == 'ACK':
                    #if we got a ack, then we are good to go!
                    return 200
            except socket.timeout as e:
                print("Timed out, will try {} more time(s)".format(i))
        #The message wasn't send correctly
        return 100
    def secureRecieve():
        '''
        Will try to securely recieve data and send an ack message when it does
        Output:
            - data
        '''
        while True:
            try:
                #we want to try to recieve data
                rdata,Address = self.recieve()
                if rdata != None:
                    #We recieved the data so we are good!
                    break
            except socket.timeout as e:
                #we want to just continue to recieve data
                continue
        #we want to send the ack packet
        #The Address Tuple is of the form (IP,PORT)
        self.send('ACK',Address[1],Address[0])

        
