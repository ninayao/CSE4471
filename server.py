import sys
import time
from keylogger import Keylogger
import os
import socket
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
    s.bind(('', int(port)))
    print("Socket bound to ", port)
    s.listen(5)
    # Modify to add more players
    players = []
    data = []
    i = 1
    while len(connections) < 2:
        c, addr = s.accept()   
        connections.append(c)
        data_str = c.recv(28).decode()
        data.append(data_str)
        print(str(addr)+": " + data_str)
        #username isn't being sent to server anymore rn so I'm just replacing with numbers
        p = Player("player" + str(i))
        p.connection = c
        players.append(p)
        i+=1
        
    #game_data = data1 + "######" + data2
    players[0].connection.sendall(bytes(data[1], 'utf-8'))
    players[1].connection.sendall(bytes(data[0], 'utf-8'))

    '''
    while(1):
        for player in players:
            data = player.connection.recv(28).decode()
            print(data)
            if True:
                score_string = ""
                player.mod_score(data)
                for i in range(len(players)):
                    if len(players) > 1:
                        score_string += str(players[i].score) + " "
                    else:
                        score_string += str(players[i].score) + " " + "200 "
                player.connection.sendall(bytes(score_string, 'utf-8'))
    '''



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
