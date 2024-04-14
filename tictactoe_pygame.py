import pygame, math, os
from pygame.locals import *
from pygame.mixer import *
from tkinter import messagebox

file_path= os.path.dirname(__file__)
pygame.init()
pygame.mixer.init()

SCREEN_SIZE= (1000,600)
screen= pygame.display.set_mode(SCREEN_SIZE)

fps= 60
mark_size= 90
board_size= 500
w=5

clicker_size= board_size/3-5
positions_filled= [0 for i in range(9)]


pygame.display.set_caption("TIC-TAC-TOE")
icon= pygame.image.load(f"{file_path}/logo_tictactoe.png")
pygame.display.set_icon(icon)
settings= pygame.image.load(f"{file_path}/settings.png")
settings= pygame.transform.scale(settings, (60,60))
back= pygame.image.load(f"{file_path}/back.png")
back= pygame.transform.scale(back, (60,60))

start_background= pygame.image.load(f"{file_path}/start_background.jpg")
game_background= pygame.image.load(f"{file_path}/game_background.jpg")

board= pygame.image.load(f"{file_path}/board.png")
board= pygame.transform.scale(board, (board_size, board_size))
X= pygame.image.load(f"{file_path}/my_x.png")
X= pygame.transform.scale(X, (mark_size,mark_size))
O= pygame.image.load(f"{file_path}/my_o.png")
O= pygame.transform.scale(O, (mark_size,mark_size))
red_strike= pygame.image.load(f"{file_path}/red_line.png").convert_alpha()
blue_strike= pygame.image.load(f"{file_path}/blue_line.png").convert_alpha()
strikes= (red_strike, blue_strike)
HOR, VER, DIA1, DIA2= [],[],[],[]

for i in range(2):
    HOR.append(pygame.transform.scale(strikes[i], (board_size, mark_size/6)))
    VER.append(pygame.transform.rotate(HOR[i], 90))
    DIA1.append(pygame.transform.rotate(pygame.transform.scale(HOR[i], (board_size*(2**(1/2)), mark_size/6)), 45))
    DIA2.append(pygame.transform.rotate(DIA1[i], 90))

LINES= [HOR, VER, (DIA1, DIA2)]

musics= [f"{file_path}/start_background.mp3", f"{file_path}/game_background.mp3"]

red_sound= pygame.mixer.Sound(f"{file_path}/red.mp3")
blue_sound= pygame.mixer.Sound(f"{file_path}/blue.mp3")
win_sound= pygame.mixer.Sound(f"{file_path}/win.mp3")
draw_sound= pygame.mixer.Sound(f"{file_path}/draw.mp3")
button_sound= pygame.mixer.Sound(f"{file_path}/button.mp3")
sounds= (red_sound, blue_sound, win_sound, draw_sound, button_sound)

mark= (X,O)
state= 1 #0=>win, 1=>playing, 2=>draw
count= 0
victory= False
checked, check_pos, winner= None,None,None
window= 0
song_loaded= False
game_volume= 50
container_width= 400; container_height= 200; controller_width= container_width- 100; controller_height= 20; loaded= (game_volume/100)*controller_width
set_drag= False



screen_width, screen_height, positions, board_pos_x, board_pos_y, victory_pos_hor, victory_pos_ver, victory_pos_dia, LINE_POS, clicker_pos, clicker, name_text, start_text, button, setting_button, back_button, container, volume_text, volume_controller, volume_gas= [None for i in range(20)]


def create_screen():
    global start_background, game_background, screen_width, screen_height, positions, board_pos_x, board_pos_y, victory_pos_hor, victory_pos_ver, victory_pos_dia, LINE_POS, clicker_pos, clicker, name_text, start_text, button, settings, setting_button, back_button, game_volume, container_width, container_height, controller_width, controller_height, loaded, container, volume_text, volume_controller, volume_gas

    screen_width, screen_height = screen.get_size()
    start_background= pygame.transform.scale(start_background, screen.get_size())
    game_background= pygame.transform.scale(game_background, screen.get_size())
    board_pos_x= (screen_width-board_size)/2
    board_pos_y= (screen_height-board_size)/2

    positions = [(board_pos_x + (i%3)*(board_size/3) + ((board_size/3)-mark_size)/3 + 15, board_pos_y + (i//3)*(board_size/3) + ((board_size/3)-mark_size)/3 + 15) for i in range(9)]


    victory_pos_hor = [(board_pos_x, board_pos_y + (board_size/3 - mark_size) + i*(board_size/3)) for i in range(3)]
    victory_pos_ver = [(board_pos_x + (board_size/3 - mark_size) + i*(board_size/3), board_pos_y) for i in range(3)]
    victory_pos_dia = (board_pos_x, board_pos_y)

    LINE_POS= [victory_pos_hor, victory_pos_ver, victory_pos_dia]

    clicker_pos= [(board_pos_x+(i%3)*board_size/3+4, board_pos_y+(i//3)*board_size/3+4) for i in range(9)]
    
    clicker= [pygame.Rect(clicker_pos[i][0], clicker_pos[i][1], clicker_size, clicker_size) for i in range(9)]

    name_font= pygame.font.SysFont('comicsans', icon.get_width()//6, True)
    font= pygame.font.SysFont('roman', icon.get_width()//6)
    name_text= name_font.render("TIC-TAC-TOE", True, (250,255,150))
    start_text= font.render("PLAY", True, (250,255,250), (0,0,0))
    button= pygame.Rect((screen_width-start_text.get_width())/2-2*w,screen_height-start_text.get_height()-w, start_text.get_width()+4*w, start_text.get_height()+w)
    setting_button= pygame.Rect((0,0), settings.get_size())
    back_button= pygame.Rect((0,0), back.get_size())

    loaded= (game_volume/100)*controller_width
    container= pygame.Rect((screen.get_width()- container_width)/2, (screen.get_height()- container_height)/2, container_width, container_height)
    set_font= pygame.font.SysFont("algerian", 50)
    volume_text= set_font.render("VOLUME", True, (0,0,0))
    volume_controller= pygame.Rect(container.x+(container.width- controller_width)/2, container.y+ volume_text.get_height()+controller_height, controller_width, controller_height)
    volume_gas= pygame.Rect(container.x+(container.width- controller_width)/2, container.y+ volume_text.get_height()+controller_height, loaded, controller_height)


def swap_players():
    global player
    player= (player+1)%2


def match():
    global state, checked, check_pos, winner, victory, song_loaded


    hor= [(0+i*3,1+i*3,2+i*3) for i in range(3)]
    ver= [(0+i,3+i,6+i) for i in range(3)]
    dia= [(2,4,6), (0,4,8)]
    arr= [hor, ver, dia]
    X_O_list= [[],[]]

    for i in range(9):
        if positions_filled[i]==X:
            X_O_list[0].append(i)
        elif positions_filled[i]==O:
            X_O_list[1].append(i)
    
    for check in arr:
        for i in range(len(check)):
            for j in range(2):
                if check[i][0] in X_O_list[j] and check[i][1] in X_O_list[j] and check[i][2] in X_O_list[j]:
                    checked= arr.index(check); check_pos= i; winner= j; state= 0; victory=True
                    song_loaded= False
                    return


def add_text():
    screen.blit(name_text, (((screen_width-name_text.get_width())/2, 0)))
    screen.blit(start_text, ((screen_width-start_text.get_width())/2,screen_height-start_text.get_height()))
    pygame.draw.rect(screen, (0,255,0), button, w)


def create_settings():
    global screen, game_volume, container_width, container_height, controller_width, controller_height, loaded, container, volume_text, volume_controller, volume_gas, set_drag

    screen.fill((12,12,12))
    screen.blit(back, (0,0))
    pygame.draw.rect(screen, (202,203,230), container)
    pygame.draw.rect(screen, (0,0,200), volume_controller, 2)
    pygame.draw.rect(screen, (0,0,200), volume_gas)
    screen.blit(volume_text, (container.x+(container.width- volume_text.get_width())/2, container.y+ volume_text.get_height()/2))
    font= pygame.font.SysFont('arial', 20)
    help_text1= font.render("1. Press f to switch between fullscreen", True, (0,0,0))
    help_text2= font.render("2. Press q to quit the game", True, (0,0,0))
    screen.blit(help_text1, ((screen_width-help_text1.get_width())/2, container.y+ volume_text.get_height()+ help_text1.get_height()*3))
    screen.blit(help_text2, ((screen_width-help_text1.get_width())/2, container.y+ volume_text.get_height()+ help_text1.get_height()*3+ help_text2.get_height()))

def player_status():
    global player, replay_button
    
    screen.blit(back, (0,0))
    about_font= pygame.font.SysFont("algerian", 30)
    about_text1= about_font.render("PLAYER 1: X", True, (255,255,255), (0,0,0))
    about_text2= about_font.render("PLAYER 2: O", True, (255,255,255), (0,0,0))
    screen.blit(about_text1, (screen_width-about_text1.get_width()*1.5, about_text1.get_height()))
    screen.blit(about_text2, (screen_width-about_text1.get_width()*1.5, about_text1.get_height()*3))
    status_font= pygame.font.SysFont("arial", 30)
    replay_text= about_font.render("Replay", True, (200,200,200), (0,0,0))
    if screen.get_size()== SCREEN_SIZE:
        replay_pos_y= screen_height- replay_text.get_height()
    else:
        replay_pos_y= screen_height-replay_text.get_height()*3

    replay_button= pygame.Rect((screen_width-replay_text.get_width())/2, replay_pos_y, replay_text.get_width(), replay_text.get_height())

    if state==1:
        status= f"Player {player+1}'s Turn"
    elif state==0:
        status= f"Hurray.. Player {winner+1} WON"
        pygame.draw.rect(screen, (0,0,0), replay_button)
        screen.blit(replay_text, (replay_button.x, replay_button.y))
    else:
        status= "Oh.. Ouh.. It's a DRAW"
        pygame.draw.rect(screen, (0,0,0), replay_button)
        screen.blit(replay_text, (replay_button.x, replay_button.y))

    status_text= status_font.render(status, True, (255,155,155), (10,10,10))
    screen.blit(status_text, ((screen_width-status_text.get_width())/2, 0))



def main():
    global player, count, state, winner, checked,check_pos, victory, screen_width, screen_height, board_pos_x, board_pos_y, positions, victory_pos_hor, victory_pos_ver, victory_pos_dia, LINE_POS, clicker_pos, clicker, name_text, start_text, button, song_loaded
    screen.blit(game_background, (0,0))

    screen.blit(board, (board_pos_x, board_pos_y))
    player_status()
    
    if state==1 and count==9:
        state=2
        song_loaded= False
    for i in range(9):
        if positions_filled[i]:
            screen.blit(positions_filled[i], positions[i])
    
    
        if victory:
            pygame.mixer.music.pause()
            pygame.mixer.Sound.play(win_sound)
            victory= False
        try:
            if checked<2:
                screen.blit(LINES[checked][winner], LINE_POS[checked][check_pos])
            else:
                screen.blit(LINES[checked][check_pos][winner], LINE_POS[checked])
        except:
            pass


def start_game():
    global player, count, state, winner, checked,check_pos, victory, window, song_loaded, screen, game_volume, setting_button, set_drag, back_button, replay_button
    player= 0

    clock= pygame.time.Clock()
    clock.tick(fps)


    run=True
    while run:
        mouse_pos= pygame.mouse.get_pos()
        screen.fill((0,0,0))
        create_screen()

        if not song_loaded:
            if window==1:
                if state==1:
                    pygame.mixer.music.load(musics[1])
                elif state==2:
                    pygame.mixer.music.pause()
                    pygame.mixer.Sound.play(draw_sound)
                    pygame.time.delay(math.ceil(pygame.mixer.Sound.get_length(draw_sound))*1000)
                    pygame.mixer.music.load(musics[0])
                else:
                    pygame.time.delay(math.ceil(pygame.mixer.Sound.get_length(win_sound))*1000)
                    pygame.mixer.music.load(musics[0])
            else:
                pygame.mixer.music.load(musics[0])
            song_loaded= True
            pygame.mixer.music.set_volume(game_volume/100)
            for i in range(len(sounds)):
                pygame.mixer.Sound.set_volume(sounds[i], game_volume/100)
            pygame.mixer.music.play(-1)


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(math.ceil(pygame.mixer.Sound.get_length(button_sound))*100)
                run= False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_q:
                    if messagebox.askyesno('TIC-TAC-TOE', "Do you really want to quit?"):
                        run= False
                elif event.key == pygame.K_f:
                    if screen.get_size() == SCREEN_SIZE:
                        screen= pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    else:
                        screen= pygame.display.set_mode(SCREEN_SIZE)

            
            if window in (0,1):
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if window==1:
                        if state==1:
                            for i in range(9):
                                if clicker[i].collidepoint(mouse_pos) and not positions_filled[i]:
                                    pygame.mixer.Sound.play(sounds[player])
                                    positions_filled[i]= mark[player]
                                    count+=1
                                    swap_players()
                                    match()
                        
                        else:
                            if replay_button.collidepoint(mouse_pos):
                                for i in range(9):
                                    positions_filled[i]= 0
                                state= 1
                                song_loaded= False
                                player= 0
                                count= 0
                                checked, check_pos, winner= None, None, None

                    elif window==0:
                        if button.collidepoint(mouse_pos):
                            pygame.mixer.Sound.play(button_sound)
                            window=1; song_loaded= False
                        elif setting_button.collidepoint(mouse_pos):
                            pygame.mixer.Sound.play(button_sound)
                            window=2
                
            elif window==2:
                if event.type== MOUSEBUTTONDOWN:
                    if volume_controller.collidepoint(mouse_pos):
                        set_drag= True
                        start_vol= mouse_pos[0]

                    elif back_button.collidepoint(mouse_pos):
                        pygame.mixer.Sound.play(button_sound)
                        window=0
                
                if event.type== MOUSEMOTION and set_drag:
                    if game_volume>=0 and game_volume<=100:
                        game_volume+= ((mouse_pos[0]-start_vol)/controller_width)*100
                    elif game_volume<0:
                        game_volume=0
                    elif game_volume>100:
                        game_volume=100
                    start_vol= mouse_pos[0]
                    pygame.mixer.music.set_volume(game_volume/100)
                    for i in range(len(sounds)):
                        pygame.mixer.Sound.set_volume(sounds[i], game_volume/100)
                    
                
                if event.type== MOUSEBUTTONUP:
                    set_drag= False
            
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and window==1:
                if back_button.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(button_sound)
                    if not messagebox.askyesno("TIC-TAC-TOE", "Do you want to save the game?"):
                        for i in range(9):
                            positions_filled[i]= 0
                        player= 0
                        count= 0
                        checked, check_pos, winner= None, None, None
                    window=0
                    song_loaded=False

        if window==1:
            main()
        elif window==0:
            screen.blit(start_background, (0,0))
            screen.blit(icon, ((screen_width-icon.get_width())/2,(screen_height-icon.get_height())/2))
            screen.blit(settings, (0,0))

            add_text()

        elif window==2:
            create_screen()
            create_settings()


        pygame.display.update()
    pygame.quit()


if __name__=="__main__":
    start_game()