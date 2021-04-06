import sys
import time
from keylogger import Keylogger
import os
import socket
import select
from Client import Player



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
        
        # Select waits for a given socket to be ready to read before trying
        ready = select.select([players[0].connection], [], [], 0.5)
        ready1 = select.select([players[1].connection], [], [], 0.5)

        # Handle messages from player 1
        if ready[0]:
            # Recieve length of word for score modification
            data = players[0].connection.recv(28).decode()
            score_string = ""
            data_dict = data.split()
            data = data_dict[0]
            if len(data_dict) > 1:
                caesarp2 = True
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
            # Send score string to client 1
                    
            players[0].connection.sendall(bytes(score_string, 'utf-8'))

        # Handle messages from player 2
        if ready1[0]:
             # Recieve length of word for score modification
            data1 = players[1].connection.recv(28).decode()
            score_string = ""
            data_dict = data.split()
            data = data_dict[0]
            if len(data_dict) > 1:
                caesarp1 = True
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
            # Send score string to client 2
            players[1].connection.sendall(bytes(score_string, 'utf-8'))

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


    # old code for command line version of game
    # start = None
    # p_bool = False
    # #text = keylog_from_text(mode, string_from_file)
    # for char in string_from_file:
    #     file = open("powerup.txt", "r")
    #     p_up = file.read()
    #     if p_bool == False:
    #         if p_up == "A" or p_up == "B" or p_up == "C":
    #             p_bool = True
    #             start = time.time()
    #             if p_up == "A":
    #                 k.change_mode("none")  
    #             elif p_up == "B":
    #                 k.change_rand(20)
    #             elif p_up == "C":
    #                 speed = 0.5
    #     end = time.time()    
    #     if start is not None:
    #         elapsed = end - start
    #         if elapsed >= 5:
    #             open("powerup.txt", "w").close()
    #             k.change_mode(mode)
    #             k.change_rand(10)
    #             speed = 0.2    
    #             p_bool = False        
    #     c = k.simulated_key_pressed(char)
    #     print_text(speed, c)
    #     for client in connections:

    #         data = client.recv(28).decode()
    #         print("data recieved")
    #         send_data = "data sent"
    #         client.sendall(bytes(send_data, 'utf-8'))
    #     #print(speed)
    #     #print(k.get_mode())
    #     #print(k.get_rand())
    #file = open("powerup.txt", "w")
    #file.write("END")    
