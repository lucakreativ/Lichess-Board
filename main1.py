import requests
import asyncio
from lichess_client import APIClient
import serial
import time

user= "lucakreativ"
meintoken="QHwDl55O3vSbY9Ec"

mcount=0
halb_moves=["", ""]
#id_game="VKdMtBsg"
#moves="e2e4"

felder_name=[
"a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
"a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
"a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
"a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
"a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
"a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
"a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
"a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
]

altser_data=["x","x", "x"]


lesestat=0
#time.sleep(3)

def Serial(lesestat):
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)

    except serial.serialutil.SerialException:
        print("Bitte DGT-Brett anschließen")
        #lesSerial()

    else:
        #print("angeschlossen")
        try:
            ser_data = ser.readline()
        except serial.serialutil.SerialException:
            print("Bitte DGT-Brett anschließen")
        else:
            #print(ser_data)
            if len(ser_data)>=66:
                #print("Groß Genug")

                altser_data[2]=altser_data[1]
                altser_data[1]=altser_data[0]
                altser_data[0]=ser_data

                if altser_data[2]!= "x":
                    #print("nicht x")
                    Felder(ser_data, altser_data[1], mcount)
                else:
                    print("Keine Referenz")
            else:
                print("Datenübertragung ist zu kurz")


def checkGame():
    userdatajason= requests.get("https://lichess.org/api/user/"+user)
    userdata=userdatajason.text

    posP = userdata.find("playing")

    if posP<=1250:
        #print("Spielt gerade")

        id_game=userdata[posP+30:posP+38]
        #print(id_game)
        return(id_game)
    else:
        #print("Spielt gerade nicht")
        return("0")


def Felder(ser_data, altser_datan, mcount):
    if ser_data!=altser_datan:
        print("neues Spielfeld")
        #print(altser_data)

        #i=0
        for i in range(63):
            if ser_data[i]!=altser_datan[i]:
                if mcount==0:
                    ms=felder_name[i]
                    #print(ms)

                    halb_moves[1]=halb_moves[0]
                    halb_moves[0]=ms

                    if halb_moves[1]==halb_moves[0]:
                        mcount=0
                    else:
                        mcount=1


                elif mcount==1:
                    me=felder_name[i]
                    #print(me)

                    halb_moves[1]=halb_moves[0]
                    halb_moves[0]=me

                    if halb_moves[0]==halb_moves[1]:
                        mcount=1
                    else:
                        move=halb_moves[0]+halb_moves[1]

                        mcount=0
                        Move(move)


        i+=1


def Move(move):
    print("Zug ist: "+move)
    rf = input("Richtig/Fasch (y/n): ")
    if rf=="y":
        sendMove(move)
        print()
    elif rf=="n":
        print()
        print("Zürückstellen innerhalb 5 Sekunden und dann nochmal machen")
        time.sleep(5)
    else:
        print()
        print("Bitte Ja oder Nein eingeben (y/n)")
        Move(move)


def sendMove(move):
    print()

    game_id=checkGame()
    if game_id!="0":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(move, game_id))
    else:
        print("Du bist gerade in keinem Spiel, bitte Figur zurückstellen(innerhalb 5 Sekunden) und ein Spiel starten")


async def main(move, id_game):
    client = APIClient(token=meintoken)
    response = await client.boards.make_move(game_id=id_game, move=move)
    #print(response)
    Lichess_response(response)


def Lichess_response(response):
    pos=find.response("content")
    posE=find.response("}", pos)
    zurück_lichess=response[pos+12:posE-1]
    pos=find.zurück_lichess("ok")

    if pos==-1:
        print(zurück_lichess)
    else:
        print("Zuck wurde erfolgreich ausgeführt")




while True:
    #lesestat=Serial(lesestat)
    Serial(lesestat)
    
    time.sleep(0.1)