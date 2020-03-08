# -*- coding: utf-8 -*-
import curses
from random import randrange,choice
from collections import defaultdict

actions = ['Up','Left','Down','Right','Restart','Exit']
letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']
actions_dict = dict(zip(letter_codes,actions * 2))

def get_user_action(keyboard):
    char = 'N'
    while char not in actions_dict:
        char = keyboard.getch()
    return actions_dict[char]

def tranpose(field):
    return [list(row) for row in zip(*field)]

def invert(field):
    return [row[::-1] for row in field]

class GameField(object):
    def __init__(self,height=4,width=4,win=2048):
        self.height = height
        self.width = width
        self.win_value = win
        self.score = 0
        self.highscore = 0
        self.reset()

    def reset(self):
        # 更新分数
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0      
        # 初始化游戏开始界面
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()
        self.spawn()

    def is_win(self):
        return any(any(i >= self.win_value for i in row) for row in self.field)
    
    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in actions)
        
    def move(self,direction):
        def move_row_left(row):
            def tighten(row):
                '''将零散的非零单元集中'''
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row
                
            def merge(row):
                '''对临近元素合并'''
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2 * row[i])
                        self.score += 2 * row[i]
                        pair = False
                    else:
                        if i+1 < len(row) and row[i] == row[i+1]:
                            pair = True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row
            # 先将零散的元素集中，然后将相邻的相等元素合并，
            # 合并时会插入零元素，所以合并完后要再次集中。
            return tighten(merge(tighten(row)))
        
        moves = {}
        moves['Left']  = lambda field:[move_row_left(row) for row in field]
        moves['Right'] = lambda field:invert(moves['Left'](invert(field)))
        moves['Up']    = lambda field:tranpose(moves['Left'](tranpose(field)))
        moves['Down']  = lambda field:tranpose(moves['Right'](tranpose(field)))
        
        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False
        
    def spawn(self):
        # 从100中取一个随机数，如果随机数大于89，new_element=4,否则=2
        new_element = 4 if randrange(100)>89 else 2
        #print(new_element)
        # 得到一个随机空白位置的元组坐标
        (i,j) = choice([(i,j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        #print((i,j))
        self.field[i][j] = new_element
        
    def move_is_possible(self,direction):
        def row_is_left_movable(row):
            def change(i):
                if row[i] == 0 and row[i+1] != 0:
                    return True
                if row[i] !=0 and row[i+1] == row[i]:
                    return True
                return False
            return any(change(i) for i in range(len(row) - 1))
        
        check={}
        check['Left']  = lambda field: any(row_is_left_movable(row) for row in field)
        check['Right'] = lambda field: check['Left'](invert(field))
        check['Up']    = lambda field: check['Left'](tranpose(field))
        check['Down']  = lambda field: check['Right'](tranpose(field))
        
        if direction in check:
            return check[direction](self.field)
        else:
            return False
            
    def draw(self,screen):
        help_str1    = '(W)Up (S)Down (A)Left (D)Right'
        help_str2    = '    (R)Restart (Q)Exit'
        gameover_str = '        GAME OVER!'
        win_str      = '        YOU WIN!'
        
        def cast(string):
            screen.addstr(string + '\n')
            
        def draw_hori_separator():
            line = '+' + ('+------' * self.width + '+')[1:]
            cast(line)
            
        def draw_row(row):
            cast(''.join('|{:^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')
            
        screen.clear()
        cast('SCORE: ' + str(self.score))
        if 0 != self.highscore:
            cast('HIGHSCORE: ' + str(self.highscore))
            
        for row in self.field:
            draw_hori_separator()
            draw_row(row)
        draw_hori_separator()
        
        if self.is_win():
            cast(win_str)
        else:
            if self.is_gameover():
                cast(gameover_str)
            else:
                cast(help_str1)
        cast(help_str2)

def main(stdscr):

    def init():
        '''初始化游戏棋盘'''
        game_field.reset()
        return 'Game'
        
    def not_game(state):
        game_field.draw(stdscr)

        action = get_user_action(stdscr)
        
        responses = defaultdict(lambda:state)  
        responses['Restart'],responses['Exit'] = 'Init','Exit'   
        return responses[action]
        
    def game():
        game_field.draw(stdscr)
        
        action = get_user_action(stdscr)
        
        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action):
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'    
        return 'Game'
            
    state_actions = {
            'Init':init,
            'Win':lambda:not_game('Win'),           #原地循环，直到Q\R被按下，跳出循环
            'Gameover':lambda:not_game('Gameover'), #同理
            'Game':game                             #原地循环，直到游戏结束，或者Q\R被按下
    }

    curses.use_default_colors()    
    game_field = GameField(win=2048)
    state = 'Init'
    while state != 'Exit':
        state = state_actions[state]()

curses.wrapper(main)