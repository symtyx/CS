##########################################################################################
# Created by Mostafa Atmar

'''
A game where there are two players competing to earn points. 
Each player has two choices; cooperate or steal. Cooperating gives both players 
+2 points, stealing can get you +3 but the other person loses -1. If both steal,
both players earn nothing. Both player actions are pre-determined and fall
under 5 categories: previous, friend, cheater, grudger, detective. Every one
of these types of players have their own distinctive play styles outlined in the pdf.

'''
##########################################################################################

class Move:
    def __init__(self, cooperate=True):
        self.cooperate = cooperate
    def __str__(self):
        if self.cooperate == True:
            return "." #if cooperates, returns '.'
        if self.cooperate == False:
            return "x" #if cheats, returns 'x'
    def __repr__(self):
        return "Move(%s)" % (self.cooperate) #choice is made here
    def __eq__(self, other):
        if self.cooperate == other.cooperate:
            return True
    def change(self): #toggles between cooperate or cheat
        if self.cooperate == True: 
            self.cooperate = False
        elif self.cooperate == False:
            self.cooperate = True
    def copy(self): 
        return Move(self.cooperate) #new Move object made w/action
        
class PlayerException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg #message returned here
    def __repr__(self):
        return "PlayerException('{}')".format(self.msg) #writes exception frame

class Player:
    def __init__(self, style, points=0, history=None):
        self.style = style
        self.points = points
        self.history = history
        if self.history == None:
            self.history = [] #gives empty list for no history
        legal = ["previous","friend","cheater","grudger","detective"]
        if self.style not in legal: #list of styles defined and checked here
            raise PlayerException("no style \'%s\'." %self.style) 
        #exception raised if not in list
    def __str__(self):
        holder = '' #appends text
        for i in range(len(self.history)):
            holder+= Move.__str__(self.history[i]) #each move is placed in holder
        return "%s(%s)" %(self.style, self.points) + holder #combines all
    def __repr__(self):
        return "Player('{}', {}, {})".format(self.style, self.points,self.history)
    def reset_history(self):
        self.history = [] #new history
    def reset(self):
        self.history = [] #new history and points
        self.points = 0
    def update_points(self,amount):
        self.points += amount #points updated by amount
    def ever_betrayed(self):
        holder = '' #holds text
        for i in range(len(self.history)): #goes through history
            holder+= Move.__str__(self.history[i]) 
        if "x" in holder: #checks for betrayal occurence
            return True
        else:
            return False
    def record_opponent_move(self, move):
        self.history.append(move) #appends move at end of list
    def copy_with_style(self):
        return Player(self.style, 0, []) #new Player object with default values
    def choose_move(self):
        if self.style == "friend": #always cooperates
            return Move(True)
        if self.style == "cheater": #always cheats
            return Move(False)
        if self.style == "previous": #first move is cooperate
            if len(self.history) == 0:
                return Move(True)
            return self.history[-1] #rest is last move in list
        if self.style == "detective":
            if len(self.history) == 0:
                return Move(True)
            if len(self.history) == 1:
                return Move(False)
            if len(self.history) == 2:
                return Move(True)
            if len(self.history) == 3: #moves 1-4 predetermined
                return Move(True)    
            if len(self.history) > 3: #after first 4
                if self.ever_betrayed() == True: #if cheated before...
                    return self.history[-1] #reciprocate last move
                else:
                    return Move(False) #otherwise keep cheating
        if self.style == "grudger":
            if self.ever_betrayed() == True: #if betrayed...
                return Move(False) #tear em apart
            return Move(True) #otherwise cooperate

def turn_payouts(move_a, move_b):
    if move_a == Move(True) and move_b == Move(False): 
        return (-1,3) #if a cheats
    if move_a == Move(False) and move_b == Move(True):
        return (3,-1) #if b cheats
    if move_a == Move(False) and move_b == Move(False):
        return (0,0) #if both cheat
    if move_a == Move(True) and move_b == Move(True): 
        return (2,2) #if both cooperate
def build_players(initials):
    built = [] #final list
    legal_styles = ["p","f","c","g","d"] #possible styles
    for i in initials:
        if i == "p": #looks at each letter
            x = Player("previous", 0, []) #makes corresponding object
            built.append(x) #appends to list
        if i == "f":
            x = Player("friend", 0, [])
            built.append(x)
        if i == "c":
            x = Player("cheater", 0, [])
            built.append(x)
        if i == "g":
            x = Player("grudger", 0, [])
            built.append(x)
        if i == "d":
            x = Player("detective", 0, [])
            built.append(x)
        if i not in legal_styles: #if letter is not a style, exception raised
            raise PlayerException("no style with initial \'%s\'." %i) 
    return built
def composition(players):
    amount = {} 
    temp = []
    for i in players: #pulls style from each object
        temp.append(i.style) #appends to list
    for i in temp: 
        if i in amount.keys(): #if entry exists
            amount[i] += 1 #increment
        else:
            amount[i] = 1 #otherwise initialize at 1
    return amount
def run_turn(player_a, player_b):
    if id(player_a) == id(player_b): #exception for identical id
        raise PlayerException("players must be distinct.")
    
    player_a.points -= 1 #deduct 1 token
    player_b.points -= 1

    player_a.choose_move() #move chosen from choose_move
    player_b.choose_move()

    player_a.record_opponent_move(player_b.choose_move())
    player_b.record_opponent_move(player_a.choose_move())
    #action recorded in each others histories
    
    pay = turn_payouts(player_a.history[-1],player_b.history[-1]) 
    #last move in history is determined and pay is calculated

    player_a.update_points(pay[1]) #player a rewarded from player b's move
    player_b.update_points(pay[0]) #vice versa
def run_game(player_a, player_b, num_turns=5):
    player_a.reset_history() #histories reset
    player_b.reset_history()
    
    for i in range(num_turns):
        try:
            if id(player_a) == id(player_b): #exception for identical id
                raise PlayerException("players must be distinct.") #exception raised
            run_turn(player_a,player_b) #run if no error
        except: #if exception raised
            break #end function

