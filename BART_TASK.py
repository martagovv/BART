#Python take home exam 2021
#Student: Marta Gómez Vargas
#Student number: s1044254
from psychopy import core, visual, event, data, gui, sound
import random
#The organization of my exam consists in three parts: (1)functions needed for the BART, (2)functions for writing up the data and (3)function for BART and running the complete program

#(1) Functions needed for the BART:
def instruction(win): #the instructions are displayed in an image (rules and control included), and the participant can press y when he/she is ready to start
    instructions = visual.ImageStim(win, image = 'instruction.jpg')
    instructions.draw()
    win.flip()
    event.waitKeys(keyList=['y'])
    
def presentballoon(win, size, money, money_total): #this function is used for presenting the balloon in each trial, the variables it has are the size (because it has to increase) and the money (because it is not constant)
    balloon = visual.ImageStim(win)
    balloon.size = size
    balloon.setImage("balloon.png")
    
    m1 = visual.TextStim(win = win, text = "In this trial you have "+str(money)+" €", pos = (0, 0.8), color = 'black', font = "arial nova light")
    m2 = visual.TextStim(win = win, text = "So far, you have collected: "+str(money_total)+" €", pos = (0, -0.8), color = 'black', font = "arial nova light")
    keyreminder1 = visual.TextStim(win = win, text = "pump = space", pos = (-0.7, 0.15), color = 'purple', font = "arial nova light")
    keyreminder2 = visual.TextStim(win = win, text = "collect money = t", pos = (-0.7, -0.15), color = 'purple', font = "arial nova light")

    balloon.draw()
    m1.draw(win)
    m2.draw(win)
    keyreminder1.draw(win)
    keyreminder2.draw(win)
    #thanks to the messages m1 and m2 the pp can see the money they are meaking per trial and in total
    win.flip()
    
def explosion(win): #each time the balloon explodes this function will display a message
    explosion = visual.TextStim(win, 'BUM :(', color = 'red', font = "arial nova light")
    explosion.draw()
    win.flip()
    core.wait(2)
    
def final_screen(win, money_total): #when the participant finish the task they will see this screen with the total money they made and they can click "esc" to exit the game
    m3 = visual.TextStim(win = win, text = "You have finished the task!", pos = (0, 0.3), color = 'black', font = "arial nova light")
    m4 = visual.TextStim(win = win, text = "In total, you earned: "+str(money_total)+" €", pos = (0, -0.1), color = 'black', font = "arial nova light")
    m5 = visual.TextStim(win = win, text = "PRESS e TO EXIT THE GAME", pos = (0, -0.4), color = 'grey', font = "arial nova light")
    m3.draw(win)
    m4.draw(win)
    m5.draw(win)
    win.flip()
    event.waitKeys(keyList=['e'])
    
#(2)Writing up the data
def demo(): #at the beggining a pop up will appear for the participant to enter their subject number, age, and gender. And it will be later save in an additional file (demographicsofBARTpps.txt)
    f = open('demographicsofBARTpps.txt', 'a')
    info = {'Subject number' : 000, 'Age' : 00, 'Gender' : ['Male', 'Female', 'Other']}
    popup = gui.DlgFromDict(dictionary=info, title='BART')
    if popup.OK:
        subject = info['Subject number']
        f.write("{}\t{}\t{}\n".format(subject, info['Age'], info['Gender']))
    else:
        subject = 000
    f.close()
    return subject

def write_data(data_in_file, file): #saving the data into a file called data.txt
    output = ""
    for d in data_in_file[:-1]:
        output += "{}\t".format(d)
    output += "{}\n".format(data_in_file[-1])
        
    a = open(file, 'a')
    a.write(output.format(data_in_file))
    a.close()
 
#(3)The BART function, which uses the previous functions and a loop for the trials, & running the complete program
def bart(subject):  
    
    columns_name = ['Subject number', 'Trial number', 'Number of pumps', 'Balloon explosion T/F', 'Money of the trial', 'Total money']
    write_data(columns_name, 'data.txt')
    
    win = visual.Window(fullscr=True, color=(0.8, 0.9, 1)) #this is the window where the game will take place, i gave it a light blue color and full screen.
    clock = core.Clock()
    keys = {'pump': 'space', 'take': 't', 'exit': 'e'} #the keys that the participant can use 
    instruction(win)
    
    #the 3 conditions are the probabilities that the balloon can explode:
    conditions = [1/128, 1/32, 1/8] 
    #they are rendomized using trialhandler, where I also specified that each one should be displayed 30 times (making 90 trials in total):
    trials = data.TrialHandler(conditions, 30) 

    money_total = 0 #this variable is the total amount of money that the participant accumulates, it is outside the loop because it does not need to be resetted per iteration
    responses = [0 for i in range(130)] #this variable is used for counting how many times the participant pumps the balloon
    
    for p in trials:
        size = 0.8 #original size of the balloon (inside the loop because it needs to be resetted per trial or iteration)
        money = 0 #this is the money the participant makes per trial (inside the loop because it needs to be resetted per trial or iteration)
        gameon = True #I use this boolean expression for staying in the same trial while the ballon does not explode. When it explodes or the participant decides to take the money, it is false, so the next trial starts
        while gameon:
            balloon_pops = random.choices([True, False], weights=[p, 1-p])[0] #this variable makes the balloon explode with the probability of the condition each trial belongs to
            presentballoon(win, size, money, money_total)
            clock.reset()
            respond = event.waitKeys(keyList=keys.values(), timeStamped=clock)
            response, latency = respond[0]

            #at this point, the participant gives a response, either pump or take the money
            if response == keys['pump']: #the participant decides to pump the balloon
                responses[trials.thisN] += 1 #everytime the participant pumps it is recorded here
                    
                if not balloon_pops: #the balloon did not explode with the probability 1-p
                    size += 0.02 #therefore its size increases in 0.2 units
                    money += 0.25 #and the money of that trial increases in 25 cents 
                    
                    if ((1/p)-1) > 1:
                        p = 1/((1/p)-1) #this makes the denominator of the probability of each condition to decrease one unit every time that the balloon does not explode
                    else:
                        p = 1 #this conditional expression is needed because p=1 does not neccesarily imply that the balloon explodes, therefore it iterates one more time and p would become 1/0, which is incorrect, causing the program to crash. So I stablish that if p = 1 it stays the same.
                    
                else: #the ballon exploded with probability p
                    gameon = False
                    plup = sound.Sound("plup.wav")
                    plup.play()
                    explosion(win)
                    money = 0 #participant loses the money
                
                
            if response == keys['take']: #the participant decides to collect the money
                gameon = False #this iteration or trial finishes and the next one will start
                money_total += money #the money of this trial goes to the total money sum
        
        # write data with the following order of columns: subject number, number of trial, last response before next trial, number of pumps, if the balloon exploded, money earned in that trial, total money accumulated
        #the demographic data is saved in an additional file called demographicsofBARTpps.txt
        data_in_file = [subject, trials.thisN, responses[trials.thisN], balloon_pops, money, money_total]
        write_data(data_in_file, 'data.txt')
    
    final_screen(win, money_total)
    win.close() #the task finishes

def run_bart():
    subject = demo()
    bart(subject)

run_bart()
