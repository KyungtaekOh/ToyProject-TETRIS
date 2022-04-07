from block import Block
from hover import Option
from server import Server
from client import Client
import pygame as pg
import threading
from multiprocessing import Process, Queue

class Game:
    def __init__(self):
        pg.init()
        pg.font.init()
        self.sysfont = 'dejavuserif'
        self.board_height = 1000    # board = screen
        self.board_width = 900
        self.hfield = 800           # field = tetris field
        self.wfield = 400
        self.rlt_field = (self.board_height-self.hfield)//2     # 100 row left top
        self.clt_field = (self.board_width-self.wfield)//5      # 100 col left top
        self.op_hfield = 400        # opponent field block_row = 10
        self.op_wfield = 200        # oppenent field block_row = 10
        self.max_r = 20             
        self.max_c = 10
        self.one_block = self.wfield//self.max_c
        self.block_exist = dict()
        self.my_score = 0
        self.num_of_players=1
        self.display = pg.display.set_mode((self.board_width, self.board_height))
        pg.display.set_caption("TETRIS GAME")

    def __draw_text(self, text, size=60, color=(255,255,255), row_offset=0, col_offset=0, fill=True):
        if fill:
            self.display.fill((0,0,0))
        font = pg.font.SysFont(self.sysfont, 30, bold=True)
        label = font.render(text, size, color)
        label_box = label.get_rect()
        label_box.center = ((self.board_width//2)+col_offset, (self.board_height//2)+row_offset)
        self.display.blit(label, label_box)


    def __draw_op(self, op_grid):      # Draw opponent screen
        """
        If number of players is 2,
            draw opponent's screen
        """
        sr = self.board_height//2 
        sc = self.wfield+(self.clt_field*2)

        font = pg.font.SysFont(self.sysfont, 30)
        label = font.render('Opponent', 1, (255,255,255))
        label_box = label.get_rect()
        label_box.center = (sc+100, sr-50)
        self.display.blit(label, label_box)

        for r in range(self.max_r):
            for c in range(self.max_c):
                pg.draw.rect(self.display, op_grid[r][c],
                                (sc+(c*20), sr+(r*20), 20, 20), 0)

        for r in range(self.max_r+1):     # horizontal lines
            pg.draw.line(self.display, (128,128,128), 
                                (sc, sr+(r*20)), 
                                (sc+self.op_wfield, sr+(r*20)))
        for c in range(self.max_c+1):     # vertical lines
            pg.draw.line(self.display, (128,128,128), 
                                (sc+(c*20), sr), 
                                (sc+(c*20), sr+self.op_hfield))


    def __draw_next_block(self, block:Block):
        """
        Draw next block on screen
        """
        sr = self.board_height//5
        sc = self.board_width*(2/3)
        
        font = pg.font.SysFont(self.sysfont, 30)
        label = font.render('Next Block', 1, (255,255,255))
        label_box = label.get_rect()
        label_box.center = (sc+100, sr-50)
        self.display.blit(label, label_box)
        
        coord = block.coord
        for r, c in coord:
            pg.draw.rect(self.display, block.color, (sc+(c*40), sr+(r*40), 40, 40), 0)


    def __draw_score(self):
        """
        TODO
        draw self.my_score
        """

        return 0

    def __draw_title(self, height=50):
        font = pg.font.SysFont(self.sysfont, 60)
        label = font.render('TETRIS', 1, (255,255,255))
        label_box = label.get_rect()
        label_box.center = (self.board_width//2, height)
        self.display.blit(label, label_box)

    def __draw_board(self):
        """
        Draw full of screen
        """
        self.display.fill((0,0,0))
        # Title Text
        self.__draw_title()
        
        sr = self.rlt_field
        sc = self.clt_field

        """
        Draw play screen using grid array
        """
        for r in range(self.max_r):
            for c in range(self.max_c):
                pg.draw.rect(self.display, self.grid[r][c], 
                                    (sc+(c*40), sr+(r*40), 40, 40), 0)

        """
        Draw grid 
            param: display, color, start_pos, end_pos, width=1
            pos: (x,y) == (c,r)    
        """
        for i, r in enumerate(range(self.max_r+1)):     # horizontal lines
            width = 5 if i==0 or i==self.max_r else 1
            pg.draw.line(self.display, (128,128,128), 
                                (sc, sr+(r*40)), 
                                (sc+self.wfield, sr+(r*40)), width)
        for i, c in enumerate(range(self.max_c+1)):     # vertical lines
            width = 5 if i==0 or i==self.max_c else 1
            pg.draw.line(self.display, (128,128,128), 
                                (sc+(c*40), sr), 
                                (sc+(c*40), sr+self.hfield), width)


    def __update_grid(self):
        """
        Update the grid's elements
        """
        self.grid = [[(0,0,0) for c in range(self.max_c)] for r in range(self.max_r)]
        for r in range(self.max_r):
            for c in range(self.max_c):
                if (c,r) in self.block_exist:
                    self.grid[r][c] = self.block_exist[(c,r)]


    def __get_block(self):
        """
        Make new block object
        """
        new_block = Block()
        return new_block

    def __clear_rows(self):
        """
        TODO
        1. clear line   ->  del line?
        2. shift every other row above down
        """
        target = []
        for ridx in reversed(range(self.max_r)):        # line clear
            if self.grid[ridx].count((0,0,0)) == 0:
                target.append(ridx)
                for cidx in range(self.max_c):
                    del self.block_exist[(cidx, ridx)]
        
        if target:                                      # row down
            for (col, row) in list(self.block_exist.keys()):
                count = 0
                for lidx in target:
                    if row < lidx:
                        count += 1
                if count:
                    nr, nc = row + count, col
                    self.block_exist[(nc,nr)] = self.block_exist.pop((col,row))
        return len(target)

    def __block_validation(self, block:Block):
        """
        Validate the block's coordinate
        """
        possible_coord = sum([[(c,r) for c in range(self.max_c) if self.grid[r][c]==(0,0,0)] for r in range(self.max_r)], [])
        for r, c in block.coord:
            nr = block.row + r
            nc = block.col + c
            if ((nc, nr) not in possible_coord) and nr > -1:
                return False
        return True

    def __check_end(self):
        for coord in self.block_exist:
            if coord[1] < 1:
                return True
        return False

    def __game_start(self):
        """
        Game Start
        """
        curr_block = self.__get_block()
        next_block = self.__get_block()
        self.clock = pg.time.Clock()
        self.my_score = 0
        fall_time = 0
        fall_speed = 0.4
        is_bottom = False
        game_run = True

        block_sr = -(max(curr_block.coord, key=lambda k:k[0])[0] + 2)
        block_sc = (self.max_c//2) - 1
        curr_block.set_rowcol(block_sr, block_sc)
        while game_run:
            self.__update_grid()
            fall_time += self.clock.get_rawtime()
            self.clock.tick()

            # Falling 
            if fall_time/1000 >= fall_speed:
                fall_time = 0
                curr_block.row += 1
                if not self.__block_validation(curr_block):
                    curr_block.row -= 1
                    is_bottom = True

            # Keyboard Event
            for event in pg.event.get():
                if event.type == pg.KEYDOWN: # when push any keyboard
                    if event.key == pg.K_UP:       # UP - rotate
                        curr_block.rotation()
                        if not self.__block_validation(curr_block):
                            curr_block.rotation(-1)
                    elif event.key == pg.K_DOWN:     # DOWN
                        curr_block.row += 1
                        if not self.__block_validation(curr_block):
                            curr_block.row -= 1
                    elif event.key == pg.K_RIGHT:    # RIGHT
                        curr_block.col += 1
                        if not self.__block_validation(curr_block):
                            curr_block.col -= 1
                    elif event.key == pg.K_LEFT:     # LEFT
                        curr_block.col -= 1
                        if not self.__block_validation(curr_block):
                            curr_block.col += 1
                    elif event.key == pg.K_SPACE:    # SPACE - DOWN Immediately
                        while True:
                            curr_block.row += 1
                            if not self.__block_validation(curr_block):
                                curr_block.row -= 1
                                break
            
            # Add piece to the grid
            for r, c in curr_block.coord:
                nr = curr_block.row + r
                nc = curr_block.col + c
                if nr > -1:
                    self.grid[nr][nc] = curr_block.color

            # When the block reached bottom
            if is_bottom:
                for r, c in curr_block.coord:
                    nr = curr_block.row + r
                    nc = curr_block.col + c
                    self.block_exist[(nc,nr)] = curr_block.color
                curr_block = next_block
                next_block = self.__get_block()
                curr_block.set_rowcol(block_sr, block_sc)
                is_bottom = False
                if self.__clear_rows():
                    self.my_score += 100

            self.__draw_board()
            self.__draw_next_block(next_block)
            if self.num_of_players==2:
                self.network.send(self.grid)
                rdata = self.network.receive()
                if type(rdata)==list:
                    self.__draw_op(rdata)
                elif rdata == "end":
                    self.__draw_text("You Win!!")
                    break
            
            if self.__check_end():
                game_run = False
                if self.num_of_players==2:
                    self.network.send("end")
                    self.__draw_text("You Lose... TnT")
            pg.display.update()
        
        if self.num_of_players==1:
            self.__draw_text("You Lose... TnT")
        pg.display.update()
        self.__init__()
        pg.time.delay(3000)
    

    def __draw_options(self, opt_text):
        mfont = pg.font.SysFont(self.sysfont, 60)
        c_row, c_col = (self.board_height//2, self.board_width//2)
        options = [Option(opt_text[0], (c_col, c_row-100), self.display, mfont), 
                   Option(opt_text[1], (c_col, c_row), self.display, mfont),
                   Option(opt_text[2], (c_col, c_row+100), self.display, mfont)]
        click = 0
        options_coord = [opt.get_coordinate() for opt in options]
        while not click:
            pg.event.pump()
            self.display.fill((0,0,0))
            self.__draw_title(c_row//2)
            for option in options:
                if option.label_box.collidepoint(pg.mouse.get_pos()):
                    option.hovered = True
                else:
                    option.hovered = False
                option.draw()

            event = pg.event.poll()
            if event.type == pg.QUIT:
                break
            elif event.type == pg.MOUSEBUTTONDOWN:
                col, row = event.pos
                for idx, (c1, r1, c2, r2) in enumerate(options_coord):
                    if c1<=col<=c2 and r1<=row<=r2:
                        click = idx+1
            pg.display.update()
        
        return click
    
    def __choice_type(self):
        type_text = ["1 Player", "2 Player", "Exit"]
        game_type = self.__draw_options(type_text)
        fontsize = 30
        if game_type==1:
            return 1
        elif game_type==2:
            room_text = ["Make a Room", "Enter a Room", "Exit"]
            room_type = self.__draw_options(room_text)
            
            ### Make a Room - Server user 
            if room_type==1:
                server_text = "Waiting for a connection"
                self.network = Server()
                self.__draw_text(server_text, row_offset=-fontsize)
                self.__draw_text("My IP address : "+self.network.get_ip(), row_offset=fontsize, fill=False)
                pg.display.update()
                self.network.connect()
                if self.network.is_connect():
                    return 2
                    
            ### Enter a Room - Client user
            elif room_type==2:
                client_text = "Enter Opponent IP address"
                user_input = "IP : "
                is_end = False
                num_text = 19
                pg.key.set_text_input_rect(pg.Rect(0,0,400,400))
                while not is_end:
                    for event in pg.event.get():
                        keys = pg.key.get_pressed()
                        for idx in range(len(keys)):
                            if keys[idx]==True:
                                if idx==13 or idx==27:      # Enter or ESC
                                    is_end = True
                                    break
                                elif idx==8 and len(user_input)>5:
                                    user_input = user_input[:-1]
                                    break
                                elif len(user_input) <= num_text and idx!=8:
                                    user_input += chr(idx)
                                pg.event.wait()
                    self.__draw_text(client_text, row_offset=-fontsize)
                    self.__draw_text(user_input, row_offset=fontsize, fill=False)
                    pg.display.update()
                self.network = Client(user_input[5:])
                self.network.connect()
                if self.network.is_connect():
                    return 2
                
                pg.time.delay(1000)
            else:
                pg.quit()
        else:
            pg.quit()


    def run(self):
        self.num_of_players = self.__choice_type()
        keydown = False
        while not keydown:
            self.__draw_text("Press any key to begin")
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    keydown = True
                elif event.type == pg.KEYDOWN:
                    if self.num_of_players==2:      # Multi play
                        self.network.send("start")
                        rdata = self.network.receive()
                        if rdata == "start":
                            self.__draw_text("GAME START!!")
                            pg.display.update
                            pg.time.delay(2000)
                            self.__game_start()
                    else:                           # Solo play
                        self.__game_start()
                    self.num_of_players = self.__choice_type()
        pg.quit()

if __name__=="__main__":
    game = Game()
    game.run()