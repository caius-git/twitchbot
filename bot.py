import cfg
import socket
import time
import re
import random
import threading
import datetime
import fileinput
import sys

s = socket.socket()


def connect():
    s.connect((cfg.HOST, cfg.PORT))
    s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(cfg.USER).encode("utf-8"))
    s.send("JOIN {}\r\n".format(cfg.CHANNEL).encode("utf-8"))


# if __name__ == "__main__":
#     main()

connect()


while True:
    try:
        new_username = ""
        lotto_counter = 0

        CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

        # s = socket.socket()
        # s.connect((cfg.HOST, cfg.PORT))
        # s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
        # s.send("NICK {}\r\n".format(cfg.USER).encode("utf-8"))
        # s.send("JOIN {}\r\n".format(cfg.CHANNEL).encode("utf-8"))


        def chat(sock, msg):
            temp_message = ("PRIVMSG " + cfg.CHANNEL + " :" + msg + "\r\n")
            sock.send(temp_message.encode("UTF-8"))
            print("Sent: " + msg)
            time.sleep(1 / cfg.RATE)

        def lotto_count_reset():
            global lotto_counter
            lotto_counter = 0

        def lotto_count():
            lottocounterfile = open("lottocounter.md", "r+")
            if lottocounterfile.mode == "r+":
                lotto_counter_contents = lottocounterfile.read()
                if new_username in lotto_counter_contents:
                    index = lotto_counter_contents.index(new_username)
                    lottocounterfile.seek(index)
                    line = lotto_counter_contents[index:]
                    i = line.split("\n")[0]
                    word = i.split()[-1]
                    your_number = word
                    new_number = int(your_number) + 1
                    lotto_counter_contents = lotto_counter_contents.replace(new_username + " " + your_number, new_username + " " + str(new_number))
                    lottocounterfile.seek(0)
                    lottocounterfile.truncate(0)
                    lottocounterfile.write(lotto_counter_contents)
                    lottocounterfile.close()
                    return str(new_number)
                else:
                    lottocounterfile.write(username + " 1 " + "\n")
                    lottocounterfile.close()
                    return str(1)


        def ban(sock, user):
            chat(sock, ".ban {}".format(user))

        def lotto_no_timeout():
            global lotto_counter
            global timer
            lotto_counter += 1
            timer = threading.Timer(30, lotto_count_reset)
            timer.start()

        def dick_size():
            if str(new_username) == "capu_streams":
                random_number = (random.randint(20, 30))
            elif str(new_username) == "leiziboi":
                random_number = (random.randint(1, 10))
            else:
                random_number = (random.randint(1, 30))
            emote = ""
            if random_number >= 25:
                emote = "TriHard"
            elif random_number < 25 and random_number >= 20:
                emote = "gachiGASM"
            elif random_number < 20 and random_number >= 15:
                emote = "PogChamp"
            elif random_number < 15 and random_number >= 10:
                emote = "LuL"
            elif random_number < 10 and random_number >= 5:
                emote = "FeelsBadMan"
            elif random_number < 5:
                emote = "FeelsBadMan :gun:"
            msg_to_chat = "@" + new_username + " Your dick is " + str(random_number) + " cm long " + emote
            chat(s, msg_to_chat)


        def lotto_roll():
            new_number = lotto_count()
            random_number = (random.randint(1, 7509579))
            if random_number == 1:
                current_time = datetime.datetime.now()
                chat(s, "@" + new_username + " You won the lottery PogChamp" + " Total attempts: " + new_number)
                lottofile = open("C:/Users/CJ/PycharmProjects/twitchbot/lottowinners.md", "a+")
                lottofile.write(username + " has won the lottery! This happened " + str(current_time) + ".\r\n")
                lottofile.close()
            else:
                if lotto_counter >= 1:
                    chat(s, "@" + new_username + " You didn't win the lottery FeelsBadMan " + " You have tried " + new_number + " times.")
                    timer.cancel()
                    lotto_no_timeout()
                else:
                    chat(s, "@" + new_username + " You didn't win the lottery FeelsBadMan" + " You have tried " + new_number + " times.")
                    lotto_no_timeout()

        def timeout(sock, user, secs=600):
            chat(sock, ".timeout {}".format(user, secs))


        def random_fact():
            new_fact = random.choice(cfg.LIST_OF_FACTS)
            chat(s, "@" + new_username + " " + new_fact)


        def contact():
            chat(s, "@" + new_username + " Tweet at @capubotz for more ideas/suggestions! (or bugs)")


        def cm_to_inches(cm):
            inches = cm / 2.54
            chat(s, str(cm) + " centimeters is " + str("%.2f" % inches) + " inches KKona")


        def inches_to_cm(inches):
            cm = inches / 0.393700787
            chat(s, str(inches) + " inches is " + str("%.2f" % cm) + " centimeters")



        while True:
            response = s.recv(1024).decode("utf-8")
            if response == "PING :tmi:twitch.tv\r\n":
                s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            else:
                username = re.search(r"\w+", response).group(0)
                message = CHAT_MSG.sub("", response)
                message_split = message.split()

                if "speaktomebot" in message_split[0].lower():
                    chat(s, "this is the bot talking, yo")

                if "howlongismystick" in message_split[0].lower():
                    new_username = new_username + username
                    dick_size()

                if "donald trump" in message.lower():
                    new_username = new_username + username
                    chat(s, "@" + new_username + " HELL YEAH BROTHER KKona")
                elif "fake news" in message.lower():
                    chat(s, "@" + username + " HELL YEAH BROTHER KKona")
                elif "freedom" in message.lower():
                    chat(s, "@" + username + " HELL YEAH BROTHER KKona")

                if "!lotto" in message_split[0].lower() and "help" not in message:
                    new_username = new_username + username
                    lotto_roll()

                if "!lottohelp" in message_split[0].lower():
                    new_username = new_username + username
                    chat(s, "@" + new_username + " Your chances of winning the lottery are 1 in 7,509,579. You might have to spend a"
                             " little time with this command if you want to win.")
                    new_username = ""

                if "!randomfact" in message_split[0].lower():
                    new_username = new_username + username
                    random_fact()

                if "!contact" in message_split[0].lower():
                    new_username = new_username + username
                    contact()

                if "!cmtoinches" in message_split[0].lower():
                    new_username = new_username + username
                    if len(message_split) >= 2:
                        cm = message_split[1]
                        if cm.isdigit() is True and len(str(cm)) < 15:
                            cm_to_inches(int(cm))
                        elif len(str(cm)) >= 15:
                            chat(s, "@" + new_username + " That number is too big!")
                        else:
                            chat(s, "@" + new_username + " That's not a number!")

                    else:
                        chat(s, "@" + new_username + " Please input a number")

                if "!inchestocm" in message_split[0].lower():
                    new_username = new_username + username
                    if len(message_split) >= 2:
                        inches = message_split[1]

                        if inches.isdigit() is True and len(str(inches)) < 15:
                            inches_to_cm(int(inches))
                        elif len(str(inches)) >= 15:
                            chat(s, "@" + new_username + " That number is too big!")
                        else:
                            chat(s, "@" + new_username + " That's not a number!")

                    else:
                        chat(s, "@" + new_username + " Please input a number")

                if "!totallyrandomshit" in message_split[0].lower():
                    chat(s, "@capu_streams hey there :)")

                if "!capucommands" in message_split[0].lower():
                    chat(s, "@" + username + " https://github.com/caius-git/twitchbot/blob/master/commands.md")

                print(username + ": " + message)
                new_username = ""
    except Exception:
        print("[+] Error. Restarting...")
        # main()
        connect()
        pass
