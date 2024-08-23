import pygame
import random
import math
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
            "Selection Sort": selection_sort,
            "Insertion Sort": insertion_sort,  
            "Merge Sort": merge_sort,          
            "Quick Sort": quick_sort 
        }
        self.code=[['def bubble_sort(arr):\nfor n in range(len(arr) - 1, 0, -1):\nswapped = False\nfor i in range(n):\nif arr[i] > arr[i + 1]:\nswapped = True\narr[i], arr[i + 1] = arr[i + 1], arr[i]\nif not swapped:\nreturn'],['def bubble_sort(arr):\nfor n in range(len(arr) - 1, 0, -1):\nswapped = False\nfor i in range(n):\nif arr[i] > arr[i + 1]:\nswapped = True\narr[i], arr[i + 1] = arr[i + 1], arr[i]\nif not swapped:\nreturn'],['def bubble_sort(arr):\nfor n in range(len(arr) - 1, 0, -1):\nswapped = False\nfor i in range(n):\nif arr[i] > arr[i + 1]:\nswapped = True\narr[i], arr[i + 1] = arr[i + 1], arr[i]\nif not swapped:\nreturn'],['def bubble_sort(arr):\nfor n in range(len(arr) - 1, 0, -1):\nswapped = False\nfor i in range(n):\nif arr[i] > arr[i + 1]:\nswapped = True\narr[i], arr[i + 1] = arr[i + 1], arr[i]\nif not swapped:\nreturn'],['def bubble_sort(arr):\nfor n in range(len(arr) - 1, 0, -1):\nswapped = False\nfor i in range(n):\nif arr[i] > arr[i + 1]:\nswapped = True\narr[i], arr[i + 1] = arr[i + 1], arr[i]\nif not swapped:\nreturn']]
        self.descriptions = {
            "Bubble Sort": self.code[0],
            "Selection Sort": self.code[1],
            "Insertion Sort": self.code[2],  
            "Merge Sort": self.code[3],          
            "Quick Sort": self.code[4] 
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
        return self.sorting_functions.get(self.selected_option)
    
    def get_algorithm_name(self):
        return self.selected_option

    def get_description(self):
        return self.descriptions.get(self.selected_option, ["No description available"])


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

    FONT = pygame.font.SysFont('arial', 30)
    LARGE_FONT = pygame.font.SysFont('arial', 40)
    SMALL_FONT = pygame.font.SysFont('arial',10)
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

        self.window = pygame.display.set_mode((width, height),pygame.RESIZABLE)
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
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

def draw(draw_info, buttons, dropdown, sort_name, ascending, description_text=None):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    title = draw_info.LARGE_FONT.render(f"{sort_name} - {'Ascending' if ascending else 'Descending'}",1,draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    draw_list(draw_info)

    for button in buttons:
        button.draw_button(draw_info.window)

    dropdown.draw(draw_info.window)

    if description_text:
        font = draw_info.SMALL_FONT
        text_y = 10  # Start drawing the description from the top-left of the screen
        text_x = 10  # Slight padding from the left edge

        for line in description_text:
            description_surface = font.render(line, True, draw_info.BLACK)
            draw_info.window.blit(description_surface, (text_x, text_y))
            text_y += description_surface.get_height() + 5  # Add some spacing between lines

    pygame.display.update()
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    title = draw_info.LARGE_FONT.render(f"{sort_name} - {'Ascending' if ascending else 'Descending'}",1,draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    draw_list(draw_info)

    for button in buttons:
        button.draw_button(draw_info.window)

    dropdown.draw(draw_info.window)

    if description_text:
        font = pygame.font.SysFont('arial', 20)
        text_y = 500  # Adjust this value as needed
        for line in description_text:
            description_surface = font.render(line, True, draw_info.BLACK)
            draw_info.window.blit(description_surface, (50, text_y))  # Adjust X and Y coordinates as needed
            text_y += description_surface.get_height() + 5  # Add some spacing between lines

    pygame.display.update()

def draw_list(draw_info,color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect=(draw_info.SIDE_PAD//2,draw_info.TOP_PAD,
                    draw_info.width-draw_info.SIDE_PAD,draw_info.height-draw_info.TOP_PAD)

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

def is_sorted(lst, ascending=True):
    n = len(lst)
    if ascending:
        return all(lst[i] <= lst[i + 1] for i in range(n - 1))
    else:
        return all(lst[i] >= lst[i + 1] for i in range(n - 1))
    
def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True
    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i: draw_info.GREEN, i - 1: draw_info.RED}, True)
            yield True
    return lst

def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst)):
        min_idx = i

        for j in range(i + 1, len(lst)):
            if (lst[j] < lst[min_idx] and ascending) or (lst[j] > lst[min_idx] and not ascending):
                min_idx = j

        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, min_idx: draw_info.RED}, True)
        yield True

    return lst

def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def quick_sort_recursion(lst, start, end):
        if start >= end:
            return

        pivot = lst[end]
        pivot_idx = start

        for i in range(start, end):
            if (lst[i] < pivot and ascending) or (lst[i] > pivot and not ascending):
                lst[i], lst[pivot_idx] = lst[pivot_idx], lst[i]
                pivot_idx += 1

        lst[end], lst[pivot_idx] = lst[pivot_idx], lst[end]
        draw_list(draw_info, {pivot_idx: draw_info.GREEN}, True)
        yield True

        yield from quick_sort_recursion(lst, start, pivot_idx - 1)
        yield from quick_sort_recursion(lst, pivot_idx + 1, end)

    yield from quick_sort_recursion(lst, 0, len(lst) - 1)

    return lst

def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def merge_sort_recursion(lst, left, right):
        if right <= left:
            return

        mid = (left + right) // 2
        yield from merge_sort_recursion(lst, left, mid)
        yield from merge_sort_recursion(lst, mid + 1, right)
        yield from merge(lst, left, mid, right, ascending)

    def merge(lst, left, mid, right, ascending):
        merged = []
        left_idx, right_idx = left, mid + 1

        while left_idx <= mid and right_idx <= right:
            if (lst[left_idx] < lst[right_idx] and ascending) or (lst[left_idx] > lst[right_idx] and not ascending):
                merged.append(lst[left_idx])
                left_idx += 1
            else:
                merged.append(lst[right_idx])
                right_idx += 1

        while left_idx <= mid:
            merged.append(lst[left_idx])
            left_idx += 1

        while right_idx <= right:
            merged.append(lst[right_idx])
            right_idx += 1

        for i, sorted_val in enumerate(merged):
            lst[left + i] = sorted_val
            draw_list(draw_info, {left + i: draw_info.GREEN}, True)
            yield True

    yield from merge_sort_recursion(lst, 0, len(lst) - 1)
    return lst

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawingInformation(800, 600, lst)

    num_buttons = 5  # Updated number of buttons to include the Description button
    dropdown_width = 150

    button_positions, dropdown_x = draw_info.calculate_button_positions(num_buttons, dropdown_width)

    sort_button = Button(button_positions[0][0], button_positions[0][1], draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Sort", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR)
    reset_button = Button(button_positions[1][0], button_positions[1][1], draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Reset", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR)
    ascend_button = Button(button_positions[2][0], button_positions[2][1], draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Ascend", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR)
    descend_button = Button(button_positions[3][0], button_positions[3][1], draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Descend", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR)
    desc_button = Button(button_positions[4][0], button_positions[4][1], draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Description", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR)  # New Description button

    buttons = [sort_button, reset_button, ascend_button, descend_button, desc_button]

    dropdown = DropdownMenu(dropdown_x, 75, dropdown_width, draw_info.BUTTON_HEIGHT, draw_info.FONT, (50, 50, 150), (100, 100, 200), ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"])

    sorting = False
    ascending = True
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            sort_name = dropdown.get_algorithm_name()
            draw(draw_info, buttons, dropdown, sort_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.VIDEORESIZE:
                draw_info.width, draw_info.height = event.w, event.h
                draw_info.window = pygame.display.set_mode((draw_info.width, draw_info.height), pygame.RESIZABLE)
                draw_info.set_list(draw_info.lst)

                button_positions, dropdown_x = draw_info.calculate_button_positions(num_buttons, dropdown_width)

                # Update button positions
                sort_button.rect.topleft = button_positions[0]
                reset_button.rect.topleft = button_positions[1]
                ascend_button.rect.topleft = button_positions[2]
                descend_button.rect.topleft = button_positions[3]
                desc_button.rect.topleft = button_positions[4]

                # Update dropdown position
                dropdown.rect.topleft = (dropdown_x, 75)
                dropdown.option_rects = [pygame.Rect(dropdown_x, 75 + (i + 1) * dropdown.rect.height, dropdown.rect.width, dropdown.rect.height) for i in range(len(dropdown.options))]

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if reset_button.is_clicked(pos):
                    lst = generate_starting_list(n, min_val, max_val)
                    draw_info.set_list(lst)
                    sorting = False

                elif sort_button.is_clicked(pos) and not sorting:
                    sorting = True
                    selected_sort = dropdown.get_selected_option()
                    sorting_algorithm_generator = selected_sort(draw_info, ascending)

                elif ascend_button.is_clicked(pos) and not sorting:
                    ascending = True

                elif descend_button.is_clicked(pos) and not sorting:
                    ascending = False

                elif desc_button.is_clicked(pos):
                    selected_description = dropdown.get_description()
                    draw(draw_info, buttons, dropdown, sort_name, ascending, description_text=selected_description)
                    continue  # Skip the rest of the event loop to avoid clearing the description


            dropdown.handle_event(event)

    pygame.quit()

if __name__ == '__main__':
    main()
