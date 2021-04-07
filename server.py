import sys
import time
from keylogger import Keylogger
import os
import socket
import select
from Client import Player

end=0
end1=0

#def keylog_from_text(text):
    #config.k.change_mode(mode)
    #print(config.key.get_mode())
#    for char in text:
 #       config.k.simulated_key_pressed(char)
  #  return config.k.logged

def produce_text():
    f = open("sampletext.txt", "r")
    text = f.read()
    return text

def print_text(speed, text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    return text

def game_loop(players):
    caesarp1 = False
    caesarp2 = False
    while(1):
        global end, end1
        # Select waits for a given socket to be ready to read before trying
        ready = select.select([players[0].connection], [], [], 0.5)
        ready1 = select.select([players[1].connection], [], [], 0.5)

        # Handle messages from player 1
        if ready[0]:
            # Recieve length of word for score modification
            data = players[0].connection.recv(28).decode()
            if(data=="end"):
                end+=1
            else:
                score_string = ""
                data_dict = data.split()
                data = data_dict[0]
                if len(data_dict) > 1:
                    caesarp2 = True
                else:
                    caesarp2 = False
                # mod score serverside
                players[0].mod_score(data)
                # Create string to send to clients
                for i in range(len(players)):
                    if len(players) > 1:
                        # Seperate scores with spaces for easy splitting in client
                        score_string += str(players[i].score) + " "
                score_string += "1"
                if caesarp1:
                    print("Attack from p2")
                    score_string += " cca"
                    caesarp1 = False
                # Send score string to client 1
                        
                players[0].connection.sendall(bytes(score_string, 'utf-8'))

        # Handle messages from player 2
        if ready1[0]:
             # Recieve length of word for score modification
            data1 = players[1].connection.recv(28).decode()
            if(data1=="end"):
                end1+=1
            else:
                score_string = ""
                data_dict = data1.split()
                data1 = data_dict[0]
                if len(data_dict) > 1:
                    caesarp1 = True
                else:
                    caesarp1 = False
                # mod score serverside
                players[1].mod_score(data1)
                # Create string to send to clients
                for i in range(len(players)):
                    if len(players) > 1:
                        # Seperate scores with spaces for easy splitting in client
                        score_string += str(players[i].score) + " "
                score_string += "2"
                if caesarp2:
                    print("Attack from p1")
                    score_string += " cca"
                    caesarp2 = False
                # Send score string to client 2
                players[1].connection.sendall(bytes(score_string, 'utf-8'))

        if(end==1 & end1==1):
            players[0].connection.sendall(bytes("end", 'utf-8'))
            players[1].connection.sendall(bytes("end", 'utf-8'))
            
if __name__ == '__main__':
    connections = []
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = "random"
    k = Keylogger(mode)
    string_from_file = produce_text()
    port = input("Input the port to open: ")
    s = socket.socket()
    #player_count = input("Input the numbers of players")
    # Bind user inputted port to server socket
    s.bind(('', int(port)))
    # Log confirmation of opening connection to console
    print("Socket bound to ", port)
    s.listen(5)
    players = []
    data = []
    i = 1

    #loop terminates once the server has recieved two connections
    while len(connections) < 2:
        # Accept incomming connection from client
        c, addr = s.accept()   
        connections.append(c)
        # Recieve text from current connection
        data_str = c.recv(1024).decode()
        data.append(data_str)
        # Log Connection and text to console
        print(str(addr)+": " + data_str)
        #username isn't being sent to server anymore rn so I'm just replacing with numbers
        p = Player("player" + str(i))
        # add connection to player object
        p.connection = c
        # create list of players so they are easier to iterate through
        players.append(p)
        # player number
        i+=1
        
    #game_data = data1 + "######" + data2

    # Send player 1 the text from player 2 and player 2 the text from player 1
    players[0].connection.sendall(bytes(data[1], 'utf-8'))
    players[1].connection.sendall(bytes(data[0], 'utf-8'))
    # Start game loop that recieves and responds to messages
    game_loop(players)

