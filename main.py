import time
import json
from requests.models import Response

import serial
import requests
import logging

user= ""
meintoken=""

mcount=0
halb_moves=["", ""]
backs_moves=["", ""]
USB_Port="0"

#0 for nicht senden und 1 für senden
senden_ja_nein=1



felder_name=[
"a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
"a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
"a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
"a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
"a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
"a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
"a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
"a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
"z"
]

altser_data=["x","x","x"]
filter_data=["x","x"]


lesestat=0
#time.sleep(3)

def Serial():
    #print(mcount)
    try:
        ser = serial.Serial('/dev/ttyUSB'+USB_Port, 9600)

    except serial.serialutil.SerialException:
        print("Bitte DGT-Brett anschließen")


    else:
        try:
            ser_data = ser.readline()
        except serial.serialutil.SerialException:
            print("Bitte DGT-Brett anschließen")
        else:
            ser_data=str(ser_data)
            startd=ser_data.find("s//")+3
            endd=ser_data.find("//s")
            ser_data=ser_data[startd:endd]


            if len(ser_data)>=65:
                altser_data[2]=altser_data[1]
                altser_data[1]=altser_data[0]
                altser_data[0]=ser_data

                if altser_data[2]!= "x":

                    filter_data[1]=filter_data[0]
                    filter_data[0]=altser_data[0]

                    if filter_data[1]!="x":
                        maxChanges(filter_data[0], filter_data[1], mcount)
                else:
                    print("Keine Referenz")
            else:
                print("Datenübertragung ist zu kurz")


def checkGame():

    user="lucakreativ"

    userdatajason= requests.get("https://lichess.org/api/user/"+user)
    userdata=userdatajason.text
    data_dict = json.loads(userdata)

    url=data_dict["playing"][20:28]

    return url


def maxChanges(ser_data, altser_datan, mcount):
    changesz=0
    if ser_data!=altser_datan:
        for i in range(65):
            if ser_data[i]!=altser_datan[i]:
                changesz+=1
    Felder(ser_data, altser_datan, mcount, changesz)


def Felder(ser_data, altser_datan, mcount, changesz):
    if changesz<=2:

        for i in range(65):
            if ser_data[i]!=altser_datan[i]:
                if ser_data[i]=="0":
                    if halb_moves[0]=="":
                        ms=felder_name[i]

                        if ms!="z":
                            print("Erst: "+ms)
                                                      
                        halb_moves[0]=ms


                elif ser_data[i]=="1":
                    if halb_moves[0]!="":
                        me=felder_name[i]

                        print("Zweit :"+me)

                        halb_moves[1]=halb_moves[0]
                        halb_moves[0]=me

                        backs_moves[1]=halb_moves[1]
                        backs_moves[0]=halb_moves[0]

                        move=halb_moves[1]+halb_moves[0]

                        halb_moves[1]=halb_moves[0]
                        halb_moves[0]=""

                        if halb_moves[1]!="z" and halb_moves[0] != "z":
                            Move(move)
                        else:
                            print("Halbzug Manuell eingegeben")


        i+=1


def Move(move):
    print()
    print("Zug ist: "+move)
    if senden_ja_nein==1:
        sendMove(move)
    

def sendMove(move,):
    print()

    game_id=checkGame()
    resoponse=requests.post("https://lichess.org/api/board/game/"+game_id+"/move/"+move, headers={"Authorization":"Bearer "+meintoken})
    #resoponse=resoponse.text
    #data1=resoponse.json()
    print(resoponse.text)


while True:

    Serial()
