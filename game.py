import turtle
import random

#----Set Up----
wn = turtle.Screen()

rhythm_presser = []

button_property = {'Left': [(-100, 200), 'red', 180, []], 'Down': [(-25, 200), 'orange', -90, []], 'Up': [(50, 200), 'blue', 90, []], 'Right': [(125, 200), 'green', 0, []]} #Store (cord, color, heading, trtl_list)

timer = 30 #For Timer
counter_interval = 1000  
timer_up = False

scores = -1

timer_font = ("Arial", 20, "normal")

wn.bgpic('Activity 1.2.5\\startBackground.gif') #Create the start screen
play_image = "Activity 1.2.5\\play.gif"
wn.addshape(play_image)
wn.tracer(False)
start_button = turtle.Turtle()
start_button.speed(0)
start_button.pu()
start_button.sety(start_button.ycor()-100)
start_button.shapesize(5)
start_button.shape(play_image)
wn.tracer(True)
wn.update()

#----Functions----
def button_create(direction, cord): #Create the different buttons
    wn.tracer(False)
    button_trtl = turtle.Turtle()
    if len(rhythm_presser) < 4: #Store the four button trtl at the bottom
        rhythm_presser.append(button_trtl)
    else:
        button_property[direction][3].append(button_trtl) #Store the turtle to a list for falling button
    button_trtl.turtlesize(3)
    button_trtl.pu()
    button_trtl.speed(0)
    button_trtl.shape('triangle')
    button_trtl.color(button_property[direction][1])
    button_trtl.setheading(button_property[direction][2])
    button_trtl.goto(cord)
    wn.tracer(True)
    wn.update()
    
def screen(): #Create the four button at the bottom
    start = -100
    for direction in button_property.keys():
        button_create(direction, (start, -200))
        start +=75

def button_fall(button): #Make button fall
    global timer
    global button_trtl
    button_trtl = button_property[button][3][0]
    button_trtl.speed(speed)
    button_trtl.sety(-200)
    if len(button_property[button][3]) > 0: #If the button is not clicked then we deduct the time
        button_trtl.sety(-225)
        button_trtl.hideturtle()
        button_property[button][3].pop(0)
        timer -=1

def random_button(): #Generate a random button
    buttons = random.choice(list(button_property.keys()))
    button_create(buttons, button_property[buttons][0])
    button_fall(buttons)

def collisions(): #Detect if the turtle is within 40 pixel on the buttons at the bottom
    if -200 < button_trtl.ycor() < -160:
        return True
    else:
        return False

def pressed(button): #Check if the user timed their clicked correctly 
    global timer
    buton_list = button_property[button][3]
    if len(buton_list) > 0 and collisions(): #Detect if the button the user is correct and is timed correctly
        buton_list.pop(0)
        timer +=1
        score()
    else: #Otherwise subtract the time
        timer -=1

def countdown(): #Timer
    global timer, timer_up
    counter.clear()
    if timer <= 0:
        counter.write("Time's Up", align= 'center', font=timer_font)
        timer_up = True
    else:
        counter.write(f'Time left: {timer}s',  align= 'center', font=timer_font)
        timer -= 1
        counter.getscreen().ontimer(countdown, counter_interval) 

def score(): #Write score
    global scores
    scores +=1
    score_write.clear()
    score_write.write(f'Score: {scores}', align='center', font=timer_font)

def diff_trtl_screen(*arg): #Create the difficulty selection screen
    wn.clear()
    global diff_trtl
    wn.tracer(False)
    diff_trtl = turtle.Turtle()
    diff_trtl.speed(0)
    diff_trtl.pu()
    diff_trtl.sety(150)
    diff_trtl.write('Choose Your difficulty', align='center', font=('Arial', 50, 'bold'))
    diff_trtl.sety(diff_trtl.ycor()-75)
    diff_trtl.write('Use Up and Down to Choose difficulty\n      Press Enter to Select difficulty', align='center', font=('Arial', 15, 'bold'))
    diff_trtl.sety(diff_trtl.ycor()-100)
    global diff
    diff = {'Baby Mode': -5,'Normal': -55, 'Gamer Mode':-105} #Store as the difficulty cord
    for difficulties in diff.keys():
        diff_trtl.write(difficulties, align='center', font=('Arial', 25))
        diff_trtl.sety(diff_trtl.ycor()-50)
    diff_trtl.goto(125, diff['Normal'])
    diff_trtl.seth(180)
    diff_trtl.turtlesize(3)
    wn.tracer(True)
    wn.update()
    for selection in ['Up', 'Down']: #Choosing difficulty inputs
        wn.onkeypress(lambda x=selection: select(x), selection)
    wn.onkeypress(start_game, 'Return')
    wn.listen()
    
def select(key): #Set how fast the button fall base on difficulty
    if key == 'Up':
        if diff_trtl.ycor() < -5:
            diff_trtl.sety(diff_trtl.ycor()+50)
        else:
            diff_trtl.sety(-105)
    else:
        if diff_trtl.ycor() > -105:
            diff_trtl.sety(diff_trtl.ycor()-50)
        else:
            diff_trtl.sety(-5)
            
def start_game(): #Create the actual game
    global speed, score_write, counter
    speed = 2*list(diff.values()).index(diff_trtl.ycor())+1
    wn.clear()
    wn.bgpic('Activity 1.2.5\\gameBackground.gif')
    wn.tracer(False)
    counter = turtle.Turtle()
    counter.speed(0)
    counter.hideturtle()
    counter.pencolor('yellow')
    counter.penup()
    counter.goto(200,200)
    score_write = counter.clone()
    score_write.sety(score_write.ycor() - 50)
    screen()
    score()
    wn.tracer(True)
    wn.update()
    wn.ontimer(countdown, counter_interval) 
    for input in button_property.keys(): #User Button Input
        wn.onkeypress(lambda x =input:pressed(x), input)
    wn.listen()
    while not timer_up: #Generate random button if not time up
        random_button()

#----Game----
start_button.onclick(diff_trtl_screen)
wn.mainloop()