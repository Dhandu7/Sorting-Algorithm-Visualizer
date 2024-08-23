import pygame
import random
import math
pygame.init()

class DropdownMenu:
    def __init__(self, x, y, w, h, font, main_color, hover_color, options):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.font = font
        self.main_color = main_color
        self.hover_color = hover_color
        self.options = options
        self.rect = pygame.Rect(x, y, w, h)
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

    def draw(self, screen):
        pygame.draw.rect(screen, self.main_color, self.rect)
        text_surf = self.font.render(self.selected_option, True, (255, 255, 255))
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

        if self.active:
            for i, option in enumerate(self.options):
                color = self.hover_color if self.option_rects[i].collidepoint(pygame.mouse.get_pos()) else self.main_color
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

    def update_position(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.rect = pygame.Rect(x, y, w, h)
        self.option_rects = [pygame.Rect(x, y + (i + 1) * h, w, h) for i in range(len(self.options))]

    def get_selected_option(self):
        return self.sorting_functions.get(self.selected_option)
    
    def get_algorithm_name(self):
        return self.selected_option

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

    def update_position(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

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

    FONT = pygame.font.SysFont('arial', 20)
    LARGE_FONT = pygame.font.SysFont('arial', 40)
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
        self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
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

    def update_dimensions(self, width, height):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.set_list(self.lst)  # Update the list based on the new dimensions

def draw(draw_info, buttons, dropdown, sort_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    title = draw_info.LARGE_FONT.render(f"{sort_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    draw_list(draw_info)

    for button in buttons:
        button.draw_button(draw_info.window)

    dropdown.draw(draw_info.window)

    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD,
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)

        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

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
                yield True  # saves current state
    return lst

def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst
    if is_sorted(lst, ascending):
        return

    for i in range(len(lst)):
        min_idx = i
        for j in range(i + 1, len(lst)):
            if (lst[j] < lst[min_idx] and ascending) or (lst[j] > lst[min_idx] and not ascending):
                min_idx = j

        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, min_idx: draw_info.RED}, True)
        yield True  # save current state
    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    if is_sorted(lst, ascending):
        return

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
            yield True  # save current state
    return lst

def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def merge_sort_recursive(lst, ascending):
        if len(lst) <= 1:
            return lst

        mid = len(lst) // 2
        left_half = merge_sort_recursive(lst[:mid], ascending)
        right_half = merge_sort_recursive(lst[mid:], ascending)

        return merge(left_half, right_half, ascending)

    def merge(left, right, ascending):
        sorted_list = []
        while left and right:
            if (left[0] <= right[0] and ascending) or (left[0] >= right[0] and not ascending):
                sorted_list.append(left.pop(0))
            else:
                sorted_list.append(right.pop(0))

        sorted_list.extend(left if left else right)
        return sorted_list

    lst[:] = merge_sort_recursive(lst, ascending)
    draw_list(draw_info, clear_bg=True)
    yield True
    return lst

def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def quick_sort_recursive(lst, low, high, ascending):
        if low < high:
            pivot_index = partition(lst, low, high, ascending)
            quick_sort_recursive(lst, low, pivot_index - 1, ascending)
            quick_sort_recursive(lst, pivot_index + 1, high, ascending)

    def partition(lst, low, high, ascending):
        pivot = lst[high]
        i = low - 1
        for j in range(low, high):
            if (lst[j] < pivot and ascending) or (lst[j] > pivot and not ascending):
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
                draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
                yield True  # save current state
        lst[i + 1], lst[high] = lst[high], lst[i + 1]
        return i + 1

    quick_sort_recursive(lst, 0, len(lst) - 1, ascending)
    draw_list(draw_info, clear_bg=True)
    yield True
    return lst

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawingInformation(800, 600, lst)

    sorting = False
    ascending = True

    algorithm = bubble_sort
    algorithm_name = "Bubble Sort"
    algorithm_generator = None

    buttons = [
        Button(0, 75, draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Start", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR),
        Button(0, 75, draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Reset", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR),
        Button(0, 75, draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Ascending", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR),
        Button(0, 75, draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Descending", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR)
    ]

    dropdown = DropdownMenu(0, 75, 140, 35, draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR, ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"])

    # Initial positioning of buttons and dropdown
    button_positions, dropdown_x = draw_info.calculate_button_positions(len(buttons), dropdown.width)
    for button, pos in zip(buttons, button_positions):
        button.update_position(*pos, draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT)
    dropdown.update_position(dropdown_x, 75, dropdown.width, dropdown.height)

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.VIDEORESIZE:
                draw_info.update_dimensions(event.w, event.h)
                draw_info.set_list(lst)
                button_positions, dropdown_x = draw_info.calculate_button_positions(len(buttons), dropdown.width)
                for button, pos in zip(buttons, button_positions):
                    button.update_position(*pos, draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT)
                dropdown.update_position(dropdown_x, 75, dropdown.width, dropdown.height)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not sorting:
                    for i, button in enumerate(buttons):
                        if button.is_clicked(event.pos):
                            if i == 0:  # Start
                                sorting = True
                                algorithm_generator = algorithm(draw_info, ascending)
                            elif i == 1:  # Reset
                                lst = generate_starting_list(n, min_val, max_val)
                                draw_info.set_list(lst)
                                sorting = False
                            elif i == 2:  # Ascending
                                ascending = True
                            elif i == 3:  # Descending
                                ascending = False

                    dropdown.handle_event(event)
                    selected_algorithm = dropdown.get_selected_option()
                    if selected_algorithm:
                        algorithm = selected_algorithm
                        algorithm_name = dropdown.get_algorithm_name()

        if sorting:
            try:
                next(algorithm_generator)
            except StopIteration:
                sorting = False

        draw(draw_info, buttons, dropdown, algorithm_name, ascending)

    pygame.quit()

if __name__ == "__main__":
    main()
