import pygame
import random
import math
pygame.init()



class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw_button(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class DrawingInformation:
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREEN = 0,255,0
    RED=255,0,0
    BACKGROUND_COLOR=WHITE

    GRADIENTS =[
        (128,128,128),
        (160,160,160),
        (192,192,192)
    ]

    SIDE_PAD=100
    TOP_PAD=150

    def __init__(self,width,height,lst):
        self.width=width
        self.height=height

        self.window=pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self,lst):
        self.lst=lst
        self.max_val=max(lst)
        self.min_val=min(lst)

        self.block_width= round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = round((self.height - self.TOP_PAD) / (self.max_val - self.min_val))        
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info,buttons):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    draw_list(draw_info)
    for button in buttons:
        button.draw_button(draw_info.window)
    pygame.display.update()

def draw_list(draw_info):
    lst = draw_info.lst

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        # Calculate the height based on the value
        block_height = (val - draw_info.min_val) * draw_info.block_height

        # Ensure the block is not drawn off-screen
        y = draw_info.height - block_height
        
        color = draw_info.GRADIENTS[i % 3]
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, block_height))



def generate_starting_list(n,min_val,max_val):
    lst=[]
    for _ in range(n):
        val=random.randint(min_val,max_val)
        lst.append(val)
    return lst



def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawingInformation(800, 600, lst)


    sort_img = pygame.image.load('./images/sort-button-png-hi.png').convert_alpha()
    reset_img = pygame.image.load('./images/reset.png').convert_alpha()
    ascend_img = pygame.image.load('./images/ascend.png').convert_alpha()
    descend_img = pygame.image.load('./images/descend.png').convert_alpha()
    sort_img = pygame.transform.scale(sort_img, (75, 75))
    reset_img = pygame.transform.scale(reset_img, (75, 75))
    ascend_img = pygame.transform.scale(ascend_img, (75, 75))
    descend_img = pygame.transform.scale(descend_img, (75, 75))
#add images for all sorting methods

    #Create buttons
    sort_button = Button(25, 75, sort_img)  # Align at top-left
    reset_button = Button(100, 75, reset_img)  # Adjusted x position for alignment
    ascend_button = Button(175, 75, ascend_img)  # Adjusted x position for alignment
    descend_button = Button(250, 75, descend_img)  # Adjusted x position for alignment

    buttons = [sort_button, reset_button, ascend_button, descend_button]

    sorting = False
    ascending = True

    while run:
        clock.tick(60)  # 60 FPS

        draw(draw_info, buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Hit the red X
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if reset_button.is_clicked(pos):
                    lst = generate_starting_list(n, min_val, max_val)
                    draw_info.set_list(lst)
                    sorting = False
                elif sort_button.is_clicked(pos) and not sorting:
                    sorting = True
                elif ascend_button.is_clicked(pos) and not sorting:
                    ascending = True
                elif descend_button.is_clicked(pos) and not sorting:
                    ascending = False

    pygame.quit()

    pygame.quit()

if __name__ == '__main__':
    main()