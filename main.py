import pygame
import random
pygame.init()

class DropdownMenu:
    def __init__(self, x, y, w, h, font, main_color, hover_color, options):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = main_color
        self.hover_color = hover_color
        self.options = options
        self.font = font
        self.selected_option = options[0]
        self.active = False
        self.option_rects = [pygame.Rect(x, y + (i + 1) * h, w, h) for i in range(len(options))]
        self.sorting_functions = {
            "Bubble Sort": bubble_sort,
            "Selection Sort": selection_sort,  # Ensure you define these sorting functions
            "Insertion Sort": insertion_sort,  # Define these functions
            "Merge Sort": merge_sort,          # Define these functions
            "Quick Sort": quick_sort 
        }

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.selected_option, True, (255, 255, 255))
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

        if self.active:
            for i, option in enumerate(self.options):
                color = self.hover_color if self.option_rects[i].collidepoint(pygame.mouse.get_pos()) else self.color
                pygame.draw.rect(screen, color, self.option_rects[i])
                text_surf = self.font.render(option, True, (255, 255, 255))
                screen.blit(text_surf, text_surf.get_rect(center=self.option_rects[i].center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            elif self.active:
                for i, option_rect in enumerate(self.option_rects):
                    if option_rect.collidepoint(event.pos):
                        self.selected_option = self.options[i]
                        self.active = False
                        break
                else:
                    self.active = False

    def get_selected_option(self):
        return self.sorting_functions.get(self.selected_option, bubble_sort)


class Button:
    def __init__(self, x, y, width, height, text, font, bg_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color

    def draw_button(self, window):
        pygame.draw.rect(window, self.bg_color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        window.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class DrawingInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BLUE = 50, 50, 150
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)
    SIDE_PAD = 100
    TOP_PAD = 150

    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 35
    BUTTON_FONT = FONT
    BUTTON_BG_COLOR = BLUE
    BUTTON_TEXT_COLOR = WHITE
    BUTTON_PADDING = 20  # Space between buttons

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = round((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

    def calculate_button_positions(self, num_buttons, dropdown_width):
        total_width = (num_buttons * self.BUTTON_WIDTH) + ((num_buttons - 1) * self.BUTTON_PADDING) + dropdown_width + self.BUTTON_PADDING
        start_x = (self.width - total_width) // 2
        button_positions = []

        for i in range(num_buttons):
            x = start_x + i * (self.BUTTON_WIDTH + self.BUTTON_PADDING)
            button_positions.append((x, 75))  # Assuming y = 75 for all buttons
        dropdown_x = start_x + num_buttons * (self.BUTTON_WIDTH + self.BUTTON_PADDING)
        return button_positions, dropdown_x

def draw(draw_info, buttons, dropdown):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    title = draw_info.LARGE_FONT.render("Sorting Algorithm Visualization Tool", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    draw_list(draw_info)

    for button in buttons:
        button.draw_button(draw_info.window)

    dropdown.draw(draw_info.window)

    pygame.display.update()

def draw_list(draw_info,color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect=(draw_info.SIDEPAD//2,draw_info.TOP_PAD,
                    draw_info.WIDTH-draw_info.SIDE_PAD,draw_info.height-draw_info.TOP_PAD)

        pygame.draw.rect(draw_info.window,draw_info.BACKGROUND_COLOR,clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        block_height = (val - draw_info.min_val) * draw_info.block_height
        y = draw_info.height - block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, block_height))

    if clear_bg:
        pygame.display.update()

def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst

def bubble_sort(draw_info,ascending=True):
    lst=draw_info.lst

    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1=lst[j]
            num2=lst[j+1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j],lst[j+1] = lst[j+1],lst[j]
                draw_list(draw_info,{j:draw_info.GREEN,j+1:draw_info.RED})
                yield True #saves current state
    return lst

next()

def selection_sort(draw_info,ascending=True):
    pass
def insertion_sort(draw_info,ascending=True):
    pass
def merge_sort(draw_info,ascending=True):
    pass
def quick_sort(draw_info,ascending=True):
    pass

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawingInformation(800, 600, lst)

    num_buttons = 4
    dropdown_width = 150

    button_positions, dropdown_x = draw_info.calculate_button_positions(num_buttons, dropdown_width)

    sort_button = Button(button_positions[0][0], button_positions[0][1], draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Sort", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR)
    reset_button = Button(button_positions[1][0], button_positions[1][1], draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Reset", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR)
    ascend_button = Button(button_positions[2][0], button_positions[2][1], draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Ascend", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR)
    descend_button = Button(button_positions[3][0], button_positions[3][1], draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Descend", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR)

    buttons = [sort_button, reset_button, ascend_button, descend_button]

    dropdown = DropdownMenu(dropdown_x, 75, dropdown_width, draw_info.BUTTON_HEIGHT, draw_info.FONT, (50, 50, 150), (100, 100, 200), ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"])

    sorting = False
    ascending = True

    selected_sort = dropdown.get_selected_option()
    sorting_algorithm_generator=None
    

    while run:
        clock.tick(60)

        draw(draw_info, buttons, dropdown)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if reset_button.is_clicked(pos):
                    lst = generate_starting_list(n, min_val, max_val)
                    draw_info.set_list(lst)
                    sorting = False

                elif sort_button.is_clicked(pos) and not sorting:
                    sorting = True
                    sorting_algorithm_generator=selected_sort(draw_info,ascending)
                    print(f"Selected Sorting Algorithm: {selected_sort}")

                elif ascend_button.is_clicked(pos) and not sorting:
                    ascending = True

                elif descend_button.is_clicked(pos) and not sorting:
                    ascending = False

            dropdown.handle_event(event)

    pygame.quit()

if __name__ == '__main__':
    main()
