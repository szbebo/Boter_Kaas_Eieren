# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 13:44:19 2020

@author: bebo
"""
#import libraries
import sys
import PySimpleGUI as sg # for GUI 
import numpy as np #for array operations

sg.theme('DarkRed1') #set color theme for the windows
c_pushed=sg.theme_background_color() #set colour for used squares on the board

#define classes 

class Player(object):
    def __init__(self, name='', moves=None, if_win=False, size=3):  
        self.name = name
        self.size=size 
        self.moves = moves or np.zeros((size,size),dtype=int)
        self.if_win = if_win 
        
    #make a move    
    def move(self, board, pos):
        if board[pos]!=0:
            sg.popup_timed('Try another move', no_titlebar=True)
          
        else:
            self.moves[pos]=1
        return self.moves
    
    #check if wins
    def check_win(self):
        rows=np.sum(self.moves, axis=1)
        columns=np.sum(self.moves, axis=0)
        diagonal=np.sum(np.diagonal(self.moves))
        antidiagonal=np.sum(np.diagonal(np.fliplr(self.moves)))
        score=np.concatenate([rows,columns])
        score=np.append(score, diagonal)
        score=np.append(score, antidiagonal)
        # print('score',score) #debug
        # print('rows:', rows, 'columns: ', columns, 'diagonal:', diagonal, 'antidiagonal:', antidiagonal) #debug
        if self.size in score :
            self.if_win=True
            sg.popup_timed(self.name + ' wins the game!' ,no_titlebar=True)
        return self.if_win   
               
class Board(object):
    def __init__(self, is_full=False ,grid=None, size=3):
        self.is_full=is_full
        self.size=size
        self.grid=grid or np.zeros((size,size),dtype=int)
    
#update the status of the game    
    def update_board(self, moves_O, moves_X):
        self.grid=np.zeros((self.size,self.size),dtype=int)
        self.grid=self.grid + moves_O + moves_X
        return self.grid
    
#check is the board is full    
    def check_full(self):
        moves_count=np.sum(self.grid)
        grid_size=self.size**2
        if moves_count==grid_size:
            self.is_full=True
        return self.is_full

#layout 1 for settings
layout1 = [[sg.Text('Welcome to the game!', font='Helvetica 30', pad=(20,20))],
          [sg.Text(size=(12,1),  key='-OUTPUT-O', font='Helvetica 30',justification='center',pad=(20,20)), 
                   sg.Text('O : X',  font='Helvetica 30',  pad=(20,20)),
                   sg.Text(size=(12,1),key='-OUTPUT-X', font='Helvetica 30',justification='center',pad=(20,20))],
          
          [sg.Input(key='-IN-O',border_width=0, pad=(10,10))],
          [sg.Text('Name of Player O')], 
          
          [sg.Input(key='-IN-X', border_width=0, pad=(10,10))],
          [sg.Text('Name of Player X')], 
          [sg.Slider((3,8), orientation='h', size=(40, 20), border_width=0, key='size')],
          [sg.Text('Board size',)],
         
          [sg.Button('OK', border_width=0,pad=(10,10)), 
           sg.Button('Start new game', border_width=0, pad=(10,10)), 
           sg.Button('Exit', border_width=0, pad=(10,10))]]

win1 = sg.Window('Settings', layout1,element_justification='c', font='Helvetica 16', keep_on_top=True, no_titlebar=True)

win2_active = False #window 2 for game play

while True:
    ev1, vals1 = win1.read()
    if ev1 == 'OK':
        win1['-OUTPUT-O'].update(vals1['-IN-O'])
        win1['-OUTPUT-X'].update(vals1['-IN-X'])
        #print(O.name, X.name, B.size)
         
    if ev1 == sg.WIN_CLOSED or ev1 == 'Exit':
        win1.close()
        break

    if not win2_active and ev1 == 'Start new game':
        win2_active = True
        win1.Hide() 
        # create board and player instances for new game
        B=Board(size=int(vals1['size']))
        O=Player(name=vals1['-IN-O'], size=int(vals1['size']))
        X=Player(name=vals1['-IN-X'], size=int(vals1['size']))
          
        layout2 = [[sg.Button(' ', size=(3,1), font='Helvetica 40', key=(i,j), pad=(1,1),border_width=0) for j in range(B.size)] for i in range(B.size)]

        win2 = sg.Window('Boter, Kaas, Eieren', layout2, layout1,element_justification='c')
        
    if win2_active:        
        state= 'O' #initial state O: O starts the game
        sg.popup_timed('Player', str(O.name),' (O) makes the first move')
        # #check instance statuses
        # print(O.name,O.moves,O.if_win) #debug
        # print( X.name,X.moves, X.if_win) #debug
        
        while True:
            ev2, vals2 = win2.read()  
                      
            if ev2 in (sg.WIN_CLOSED, 'Exit'):
                win2_active  = False
                break
            
            if state == 'O': #O makes a move
                O.move(B.grid, ev2)                                          
                B.update_board(O.moves, X.moves) #update board
                
                #board=B.grid #debug
                # print(O.name,O.moves,O.if_win) #debug
                # print( X.name,X.moves, X.if_win) #debug
                # print('board:' , B.grid, B.is_full)  #debug 
                win2[ev2].update('O',button_color=(c_pushed,'white'))
                
                O.check_win()
                B.check_full()                
                # print (state) #debug
                # print(ev2) #debug
                if B.is_full== True:
                    sg.popup_timed('Game over, no possibe moves.')
                    state='end'
                elif O.if_win== False:
                    state='X'
                elif O.if_win== True:
                    state='end'
                    
            elif state == 'X': #X makes a move
                X.move(B.grid, ev2)            
                B.update_board(O.moves, X.moves) 
                
                # print('board:', B.grid, 'is the board full?',B.is_full)   #debug
                
                win2[ev2].update('X', button_color=(c_pushed,'white')) #change button colour and text
                X.check_win() #evaluate palyer moves
                B.check_full()  #evaluate board state
                
                # print ('state', state) #debug
                # print('pos', ev2) #debug
                if B.is_full== True:
                    sg.popup_timed('Game over, no possibe moves.')
                    state='end'
                elif X.if_win== False:
                    state='O'
                elif X.if_win==True:
                    state='end'
                               
        win2.close()
        win1.UnHide()
sys.exit(0)
    


