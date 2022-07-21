import random
import numpy as np
import time


def gamePlay():
    #Choose language
    polski = input("Czy grasz po Polsku? ")
    if (polski.lower()=="tak"):
        polski = True
    else:
        polski = False
        
    board = np.full((9, 9), ' ')
    
    
    yourShips = [2,2,2,3,3,4]
    if (polski):
        randomPlacement = input("Czy chcesz by twoje statki były losowo rozstawione za Ciebie? ")
        if (randomPlacement.lower()=="tak"):
            randomPlacement = True
        else:
            randomPlacement = False
    else:
        randomPlacement = input("Would you like your ships to be placed randomly for you? ")
        if (randomPlacement.lower()=="yes"):
            randomPlacement = True
        else:
            randomPlacement = False
    
    if (randomPlacement):
        while (yourShips):
            ship = yourShips.pop()
            #Keep randomly placing this ship until it's placed
            placed = False
            while (not placed):
                hv = random.choice(('h','v'))
                pn = random.randint(0,8)
                pl = random.randint(0,8)
                placed = placeRoboShip(board, ship, hv, pn, pl) #Creating this function creates so much repeated code, but it's easier than creating "if robo" for each input and - make the input optional = initialise it to null?

        if (polski):
            print("\tTwoja plansza: ")
        else:
            print("\tYour board: ")
        printBoard(board)
    else: 
        if (polski):
            print("\tTwoja plansza: ")
        else:
            print("\tYour board: ")
        while (yourShips):
            printBoard(board)
            ship = yourShips.pop()
            if (polski):
                print("Ustaw statek o długości:", ship, "Wybierz czy ustawić go poziomo czy pionowo i wpisz lewy górny róg w którym ma się zacząć statek")
            else:
                print("Place ship of length:", ship, "Select whether to place it horizontally or vertically and select the top left corner of where your ship should go")

            placeShip(board,ship, polski)
        
        
    #Set up robo board
    roboBoard = np.full((9, 9), ' ')
    
    #Create roboBoard
    roboShips = [2,2,2,3,3,4]
    while (roboShips):
        ship = roboShips.pop()
        #Keep randomly placing this ship until it's placed
        placed = False
        while (not placed):
            hv = random.choice(('h','v'))
            pn = random.randint(0,8)
            pl = random.randint(0,8)
            placed = placeRoboShip(roboBoard, ship, hv, pn, pl) #Creating this function creates so much repeated code, but it's easier than creating "if robo" for each input and - make the input optional = initialise it to null?
        
    #While not win:
    turn = 0
    pre = time.perf_counter()
    while ('■' in board and '■' in roboBoard):
        #Player's turn
        if (turn%2==0):
            shoot(roboBoard, polski)
        
        #Robo's turn
        else:
            roboShoot(board, turn, polski)
            
        turn +=1

    post = time.perf_counter()
    m, s = divmod(post-pre, 60)
    print("The game lasted ", turn, f"turns and",m, f"minutes {s:0.2f} seconds")

    if (polski):
        again = input("Czy chcesz zagrać ponownie?")

    else:
        again = input("Do you want to play again?")
        
    if (again.lower()=="tak" or again.lower()=="yes"):
        gamePlay()
    else:
        return
    
#default is False = you can't see the ships
def printBoard(board, hideShips=False):  
    letters = "  "
    for l in range (len(board[0])):
        letters += chr(65+l) + ' '
    print(letters)
    n = int(0)
    for line in board:
        linetp = str(n) + "|"
        n +=1
        for i in range (len(line)):
            if (hideShips):
                if (line[i]=='■'):
                    linetp += ' ' + "|"
                else: 
                    if line[i] =='.':
                        linetp += ' ' +"|"
                    else:
                        linetp += line[i]+"|"
            else: 
                if line[i] =='.':
                    linetp += ' ' +"|"
                else:
                    linetp += line[i]+"|"
            
        print(linetp)
#x = hit
#■ = ship (only visible on my board)
#  = empty (sea or hidden ship) - also shows up over '.' on both boards
#- = miss 
#. = ship is next to this square - used to keep player from placing ships next to each other and to mark when a ship's sunken
        #Not visible to the player, only as background mechanic

def placeShip(board, ship, polski):
    shipLine = False
    while (not shipLine): #Keep asking until a correct placement is found
        #ship = int(input("Ship size: "))
        if (polski):
            hv = input("poziomo (h)/pionowo (v): ")
            while (not (hv=='h' or hv=='v')):
                hv = input("Kliknij h aby ustawić statek poziomo lub v by postawić go pionowo: ")            

            place = input("Wybierz górny lewy róg położenia statku (n.p. 1A): ")
            #Check input is valid:
            while (not (len(place)==2 and place[0].isdigit() and place[1].isalpha())):
                place = input("Proszę użyć poprawnego formatu (n.p. 1A): ")
        else:
            hv = input("horizontal (h)/vertical (v): ")
            #Check input is valid:
            while (not (hv=='h' or hv=='v')):
                hv = input("Type h for horizontal and v for vertical placement: ")            

            place = input("Top left corner of ship placement (e.g. 1A): ")
            #Check input is valid:
            while (not (len(place)==2 and place[0].isdigit() and place[1].isalpha())):
                place = input("Please use the correct format (e.g. 1A): ")
            
        pn = int(place[0])
        pl = lToN(place[1].capitalize())
        

        #intendedShipLine:
        tempLine=[]
        try:
            if (hv=='h'):
                for i in range (ship):
                    tempLine = (board[pn,:])[pl:pl+ship]
                
                    
            elif (hv =='v'):
                for i in range (ship):
                    tempLine = (board[:,pl])[pn:pn+ship]
        except IndexError:
            if (polski):
                print("Wychodzi poza planszę, wybierz inną pozycję!")
            else:
                print("Goes out of the board! Try a different position!")

            
        
        if(all([x==' ' for x in tempLine]) and len(tempLine)==ship): #If all those spaces are free, put the boat there
            shipSquares = []
            #horizontal placement
            if (hv=='h'):
                for i in range (ship):
                    board[pn,pl+i] = '■'
                    shipSquares.append((pn,pl+i))
            #vertical placement:
            else:
                for i in range (ship):
                    board[pn+i,pl] = '■'
                    shipSquares.append((pn+i,pl))
                    
            squares = list(map(surroundingPositions, list(ship[0] for ship in shipSquares),list(ship[1] for ship in shipSquares)))            
            #Flatten squares: 
            squares = [x for xs in squares for x in xs]
            
            for square in squares:
                if (board[square[0],square[1]]==' '):
                    board[square[0],square[1]] = '.' #Mark that a ship is nearby
                    
            shipLine=True
        else:
            if (polski):
                print("To miejsce nie jest wolne, lub dotyka innego statku. Wybierz inne miejsce.")
            else:
                print("That space is not empty or touches another ship or goes off the board, try again")



#Small helper functions

def lToN(l): #returns number of letter board position
    return ord(l)-65

def surroundingSquares(board, pn,pl): #returns list of elements in surrounding squares
    positions = surroundingPositions(pn,pl)
    squares = []
    for pos in positions:
        squares.append(board[pos[0],pos[1]])
    return squares
    
def surroundingPositions(pn,pl):
    #returns positions of surrounding squares
    positions = []
    for i in range(-1,2):
        for j in range(-1,2):
            if (pn+i>=0 and pl+j>=0 and pn+i<9 and pl+j<9):
                positions.append((pn+i,pl+j))
    positions.remove((pn,pl))
    return positions

def placeRoboShip(board, ship, hv, pn, pl):
    #intendedShipLine:
    tempLine=[]
    try:
        if (hv=='h'):
            for i in range (ship):
                tempLine = (board[pn,:])[pl:pl+ship]


        elif (hv =='v'):
            for i in range (ship):
                tempLine = (board[:,pl])[pn:pn+ship]
    except IndexError:
        return False



    if(all([x==' ' for x in tempLine]) and len(tempLine)==ship): #If all those spaces are free, put the boat there
        shipSquares = []
        #horizontal placement
        if (hv=='h'):
            for i in range (ship):
                board[pn,pl+i] = '■'
                shipSquares.append((pn,pl+i))
        #vertical placement:
        else:
            for i in range (ship):
                board[pn+i,pl] = '■'
                shipSquares.append((pn+i,pl))

        squares = list(map(surroundingPositions, list(ship[0] for ship in shipSquares),list(ship[1] for ship in shipSquares)))            
        #Flatten squares: 
        squares = [x for xs in squares for x in xs]

        for square in squares:
            if (board[square[0],square[1]]==' '):
                board[square[0],square[1]] = '.' #Mark that a ship is nearby

        return True
    else:
        return False


def sunkenShip(board,pn,pl, polski):
    surrSquares = surroundingSquares(board, pn, pl)
    if ('■' in surrSquares):
        return False, None 
    
    
    finalxs = [(pn,pl)] #This is used to return list of xs if sunken
    xs = [(pn,pl)] #This is used as a stack to check all the xs in line
    
    while (xs):
        x = xs.pop(0)
        pos = surroundingPositions(x[0],x[1])
        sqrs = surroundingSquares(board, x[0],x[1])
        if ('■' in sqrs):
            return False, None
        else: 
            for p in pos: #Find the position of the xs (there will be at least the first one)
                if (board[p[0],p[1]]=='x'):
                    if (p not in finalxs): #The x hasn't been marked yet
                        xs.append(p)
                        finalxs.append(p)
    if (polski):
        print("Zatopiony!")
    else:
        print("It sank")
    return True, finalxs #If we get through the loop without finding a square, return xs

#Calculates the best spot to shoot on the board
def bestSpot(board):
    scoreBoard = np.full((9, 9), 1) 
    for i in range(9):
        for j in range(9):
            cell = board[i][j]
            if (cell=='-'):
                scoreBoard[i][j] = 0
            
            #Assign squares right next to xs high scores to continue hitting along a line
            if (cell=='x'):
                scoreBoard[i][j] = 0
                
                #Mark diagonals to 0 (because ships can't touch)
                if (i>0 and j>0):
                    scoreBoard[i-1][j-1] = 0
                if (i>0 and j<8):
                    scoreBoard[i-1][j+1] = 0
                if (i<8 and j>0):
                    scoreBoard[i+1][j-1] = 0
                if (i<8 and j<8):
                    scoreBoard[i+1][j+1] = 0
                    
                #Mark squares next to x as high - but NOT if they were marked as 0 already (and check they're on the board)
                if (i-1>=0):
                    if (scoreBoard[i-1][j]!=0):
                        scoreBoard[i-1][j] = 14
                if (i+1<=8):
                    if (scoreBoard[i+1][j]!=0):
                        scoreBoard[i+1][j] = 14
                if (j-1>=0):
                    if (scoreBoard[i][j-1]!=0):
                        scoreBoard[i][j-1] = 14
                if (j+1<=8):
                    if (scoreBoard[i][j+1]!=0):
                        scoreBoard[i][j+1] = 14
    
   
    for i in range(9):
        for j in range(9):
            #Don't change the score if it was initialised to 0
            if scoreBoard[i][j]==0:
                continue
                
            #Left (j-k) TODO - going off the board
            for k in range(1,4):
                if (j-k<0 or scoreBoard[i][j-k]==0):
                    break
                else:
                    scoreBoard[i][j] += 1
                  
            #Right
            for k in range(1,4):
                if (j+k>8 or scoreBoard[i][j+k]==0):
                    break
                else:
                    scoreBoard[i][j] += 1
            
            #Up
            for k in range(1,4):
                if (i-k<0 or scoreBoard[i-k][j]==0):
                    break
                else:
                    scoreBoard[i][j] += 1
            #Down        
            for k in range(1,4):
                if (i+k>8 or scoreBoard[i+k][j]==0):
                    break
                else:
                    scoreBoard[i][j] += 1
                
    return int((np.argmax(scoreBoard))/9),(np.argmax(scoreBoard))%9

def shoot(board, polski):
    missed = False
    while (not missed):
        #Print board
        if (polski):
            print("\tPlansza przeciwnika: ")
        else:
            print("\tOpponent's board: ")    
        printBoard(board, True)
        #Get user input
        if (polski):
            shot = input("Gdzie chcesz strzelić? (n.p. 1A): ")
        else:
            shot = input("Where would you like to shoot (e.g. 1A): ")
        #Check input is valid:
        while (not (len(shot)==2 and shot[0].isdigit() and shot[1].isalpha())):
            if (polski):
                shot = input("Proszę użyć poprawnego formatu (n.p. 1A): ")
            else:
                shot = input("Please use the correct format (e.g. 1A): ")
        pn = int(shot[0])
        pl = lToN(shot[1].capitalize())

        #If hit:
        if (board[pn][pl]=='■'):
            board[pn][pl]='x'
            if (polski):
                print("Trafiłeś w statek!")
            else:
                print("You hit a ship!")

            #EndGame
            if (not '■' in board):
                if (polski):
                    print("Koniec gry! \nWygrałeś!")
                    print("Gratulacje, pokonałeś głupiego robota!")
                else:
                    print("Game over! \nYou won!")
                    print("Congratulations, you beat this dumb robot!")
                return
                
            sunken, xs = sunkenShip(board,pn,pl, polski)
            if (sunken): 
                #Mark all surrounding squares to show ship sank
                tempsurrSquares = []
                for x in xs:
                    tempsurrSquares.append(surroundingPositions(x[0],x[1]))

                temptemp = [x for xs in tempsurrSquares for x in xs]
                surrSquares = []
                surrSquares = list(set(temptemp))

                for square in surrSquares:
                    if (board[square[0],square[1]]!='x'):
                        board[square[0],square[1]] = '-'
        
        #If not hit, mark miss and end while loop
        else: 
            if (polski):
                print("Nie trafiłeś!")
            else:
                print("You missed!")
            board[pn][pl]='-' 
            missed = True
                           


def roboShoot(board, turn, polski):
    missed = False
        
    while (not missed):
        if (turn <6):
            pn = random.randint(0,8)
            pl = random.randint(0,8)
        else:
            pn, pl = bestSpot(board)
        if (polski):
            print("Robot strzela w:",str(pn)+chr(pl+65))
        else:      
            print("Robot hitting:",str(pn)+chr(pl+65))
        
        #If hit:
        if (board[pn][pl]=='■'):
            board[pn][pl]='x'
            if (polski):
                print("Trafił!")
            else: 
                print("Your ship was hit!")
            
            #EndGame
            if (not '■' in board):
                if (polski):
                    print("Koniec gry!\nPrzegrałeś!")
                else: 
                    print("Game over! \nYou lose!")
                return

            sunken, xs = sunkenShip(board,pn,pl, polski)
            if (sunken): 
                #Mark all surrounding squares
                tempsurrSquares = []
                for x in xs:
                    tempsurrSquares.append(surroundingPositions(x[0],x[1]))
                
                temptemp = [x for xs in tempsurrSquares for x in xs]
                surrSquares = []
                surrSquares = list(set(temptemp))
                
                for square in surrSquares:
                    if (board[square[0],square[1]]!='x'):
                        board[square[0],square[1]] = '-'
                        
        else: #If not hit, mark miss and end while loop
            if (polski):
                print("Nie trafił!")
            else: 
                print("Missed!")
            board[pn][pl]='-' 
            missed = True
    if (polski):
        print("\tTwoja plansza: ")
    else:
        print("\tYour board: ")
    printBoard(board)
                           


gamePlay()
