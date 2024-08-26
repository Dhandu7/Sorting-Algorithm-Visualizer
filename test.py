import pygame
import random
import math
import time
pygame.init()
class DescriptionMenu:
    def __init__(self, x, y, font, bg_color,text_color):
        self.x = x
        self.y = y
        self.font = font
        self.bg_color = bg_color
        self.text = ""  # Initialize with an empty string
        self.text_color = text_color
        self.update_size()  # Set initial size

    def update_text(self, new_text):
        """Updates the text and adjusts the size accordingly."""
        self.text = new_text
        self.update_size()

    def update_size(self):
        """Updates the size of the menu based on the text length."""
        lines = self.text.split('\n')
        if lines:  # Ensure lines is not empty
            max_width = max(self.font.size(line)[0] for line in lines)
            total_height = sum(self.font.size(line)[1] for line in lines)
            self.width = max_width + 20  # Add padding
            self.height = total_height + 20  # Add padding
        else:
            # Default size if there is no text
            self.width = 200
            self.height = 50

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        """Draws the menu on the given window."""
        pygame.draw.rect(window, self.bg_color, self.rect)
        lines = self.text.split('\n')
        y_offset = self.rect.y + 10
        for line in lines:
            text_surface = self.font.render(line, True, self.text_color)
            window.blit(text_surface, (self.rect.x + 10, y_offset))
            y_offset += self.font.get_height()

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
        self.code=['O(n\u00b2)','O(nlogn)',]
        self.complexity = {
            "Bubble Sort": self.code[0],
            "Selection Sort": self.code[0],
            "Insertion Sort": self.code[0],  
            "Merge Sort": self.code[1],        
            "Quick Sort": self.code[1] 
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

    def handle_event(self, event, reset_execution_time_callback):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            elif self.active:
                for i, option_rect in enumerate(self.option_rects):
                    if option_rect.collidepoint(event.pos):
                        self.selected_option = self.options[i]
                        self.active = False
                        reset_execution_time_callback()  # Reset the execution time
                        break
                else:
                    self.active = False


    def get_selected_option(self):
        return self.sorting_functions.get(self.selected_option)
    
    def get_algorithm_name(self):
        return self.selected_option
    
    def get_complexity(self):
        return self.complexity.get(self.selected_option, ["No complexity available"])


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
    GREEN = 50, 205, 50
    RED = 220, 20, 60
    BLUE = 50, 50, 150
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('arial', 20)
    LARGE_FONT = pygame.font.SysFont('arial', 30)
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

def draw(draw_info, buttons, dropdown, sort_name, complexity, ascending, execution_time, description_visible, description_menu):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    title = draw_info.LARGE_FONT.render(f"{sort_name} - {'Ascending' if ascending else 'Descending'} | {complexity}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))
    execution = draw_info.FONT.render(f"{sort_name} executed in {execution_time if execution_time != 0 else '_'} seconds", 1, draw_info.BLACK)
    draw_info.window.blit(execution, (draw_info.width / 2 - execution.get_width() / 2, 45))

    draw_list(draw_info)

    for button in buttons:
        button.draw_button(draw_info.window)

    dropdown.draw(draw_info.window)

    if description_visible:
        description_menu.draw(draw_info.window)  # Only draw the description if it's visible

    pygame.display.update()  # Update the display after all drawing is done


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

def bubble_sort(draw_info,ascending=True):
    lst=draw_info.lst

    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1=lst[j]
            num2=lst[j+1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j],lst[j+1] = lst[j+1],lst[j]
                draw_list(draw_info,{j:draw_info.GREEN,j+1:draw_info.RED},True)
                yield True #saves current state
    return lst

def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst
    if is_sorted(lst, ascending):
        return

    for i in range(len(lst)):
        min_index = i

        for j in range(i + 1, len(lst)):
            draw_list(draw_info, {i: draw_info.BLUE, j: draw_info.RED, min_index: draw_info.GREEN}, True)
            yield True  

            if (lst[j] < lst[min_index] and ascending) or (lst[j] > lst[min_index] and not ascending):
                min_index = j

        # Swap the found minimum/maximum element with the first element
        if min_index != i:
            lst[i], lst[min_index] = lst[min_index], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, min_index: draw_info.RED}, True)
            yield True  

    return lst


def insertion_sort(draw_info,ascending=True):
    lst=draw_info.lst
    for i in range(1,len(lst)):
        current=lst[i]

        while True:
            ascending_sort= i >0 and lst[i-1] > current and ascending
            descending_sort= i >0 and lst[i-1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i-1]
            i-=1
            lst[i]=current
            draw_list(draw_info,{i-1:draw_info.GREEN, i: draw_info.RED}, True)
            yield True
    return lst

def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst

    # Check if the list is already sorted
    if is_sorted(lst, ascending):
        return

    def merge(left, right, start):
        merged = []
        i = j = 0
        left_len = len(left)
        right_len = len(right)

        while i < left_len and j < right_len:
            if (left[i] <= right[j] and ascending) or (left[i] >= right[j] and not ascending):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        while i < left_len:
            merged.append(left[i])
            i += 1

        while j < right_len:
            merged.append(right[j])
            j += 1

        for i in range(len(merged)):
            lst[start + i] = merged[i]
            draw_list(draw_info, {start + i: draw_info.GREEN}, True)
            yield True

    def merge_sort_recursive(start, end):
        if start < end:
            mid = (start + end) // 2
            yield from merge_sort_recursive(start, mid)
            yield from merge_sort_recursive(mid + 1, end)
            yield from merge(lst[start:mid+1], lst[mid+1:end+1], start)

    yield from merge_sort_recursive(0, len(lst) - 1)

def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst

    # Check if the list is already sorted
    if is_sorted(lst, ascending):
        return

    def partition(start, end):
        pivot = lst[end]
        low = start - 1

        for high in range(start, end):
            if (lst[high] < pivot and ascending) or (lst[high] > pivot and not ascending):
                low += 1
                lst[low], lst[high] = lst[high], lst[low]
                draw_list(draw_info, {low: draw_info.GREEN, high: draw_info.RED}, True)
                yield True

        lst[low + 1], lst[end] = lst[end], lst[low + 1]
        draw_list(draw_info, {low + 1: draw_info.GREEN, end: draw_info.RED}, True)
        yield True
        return low + 1

    def quick_sort_recursive(start, end):
        if start < end:
            p = yield from partition(start, end)
            yield from quick_sort_recursive(start, p - 1)
            yield from quick_sort_recursive(p + 1, end)

    yield from quick_sort_recursive(0, len(lst) - 1)
    return lst

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawingInformation(800, 600, lst)

    num_buttons = 5
    dropdown_width = 150

    button_positions, dropdown_x = draw_info.calculate_button_positions(num_buttons, dropdown_width)

    sort_button = Button(button_positions[0][0], button_positions[0][1], draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Sort", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR)
    reset_button = Button(button_positions[1][0], button_positions[1][1], draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Reset", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR)
    ascend_button = Button(button_positions[2][0], button_positions[2][1], draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Ascend", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR)
    descend_button = Button(button_positions[3][0], button_positions[3][1], draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Descend", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR)
    description_button = Button(button_positions[4][0], button_positions[4][1], draw_info.BUTTON_WIDTH, draw_info.BUTTON_HEIGHT, "Description", draw_info.BUTTON_FONT, draw_info.BUTTON_BG_COLOR, draw_info.BUTTON_TEXT_COLOR)

    buttons = [sort_button, reset_button, ascend_button, descend_button, description_button]

    dropdown = DropdownMenu(dropdown_x, 75, dropdown_width, draw_info.BUTTON_HEIGHT, draw_info.FONT, (50, 50, 150), (100, 100, 200), ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"])

    # Calculate the y position for the description menu
    max_button_y = max(pos[1] for pos in button_positions)
    description_menu_y = max_button_y + draw_info.BUTTON_HEIGHT + 10  # Adding a small margin

    # Initialize the DescriptionMenu
    description_menu = DescriptionMenu(10, description_menu_y, draw_info.FONT, draw_info.BLUE,draw_info.WHITE)  # Positioned below buttons

    sorting = False
    ascending = True
    sorting_algorithm_generator = None

    start_time = 0
    execution_time = 0
    show_description = False

    def reset_execution_time():
        nonlocal execution_time
        execution_time = 0

    def update_description():
        """Updates the description text based on the selected sorting algorithm."""
        selected_sort = dropdown.get_algorithm_name()
        complexity = dropdown.get_complexity()

        descriptions = {
            "Bubble Sort": (
                "Bubble Sort:\n"
                "def bubble_sort(arr):\n"
                "    n = len(arr)\n"
                "    for i in range(n):\n"
                "        for j in range(0, n-i-1):\n"
                "            if arr[j] > arr[j+1]:\n"
                "                arr[j], arr[j+1] = arr[j+1], arr[j]"
            ),
            "Selection Sort": (
                "Selection Sort:\n"
                "def selection_sort(arr):\n"
                "    n = len(arr)\n"
                "    for i in range(n):\n"
                "        min_idx = i\n"
                "        for j in range(i+1, n):\n"
                "            if arr[j] < arr[min_idx]:\n"
                "                min_idx = j\n"
                "        arr[i], arr[min_idx] = arr[min_idx], arr[i]"
            ),
            "Insertion Sort": (
                "Insertion Sort:\n"
                "def insertion_sort(arr):\n"
                "    for i in range(1, len(arr)):\n"
                "        key = arr[i]\n"
                "        j = i-1\n"
                "        while j >= 0 and key < arr[j]:\n"
                "            arr[j + 1] = arr[j]\n"
                "            j -= 1\n"
                "        arr[j + 1] = key"
            ),
            "Merge Sort": (
                "Merge Sort:\n"
                "def merge_sort(arr):\n"
                "    if len(arr) > 1:\n"
                "        mid = len(arr) // 2\n"
                "        L = arr[:mid]\n"
                "        R = arr[mid:]\n"
                "        merge_sort(L)\n"
                "        merge_sort(R)\n"
                "\n"
                "        i = j = k = 0\n"
                "        while i < len(L) and j < len(R):\n"
                "            if L[i] < R[j]:\n"
                "                arr[k] = L[i]\n"
                "                i += 1\n"
                "            else:\n"
                "                arr[k] = R[j]\n"
                "                j += 1\n"
                "            k += 1\n"
                "\n"
                "        while i < len(L):\n"
                "            arr[k] = L[i]\n"
                "            i += 1\n"
                "            k += 1\n"
                "\n"
                "        while j < len(R):\n"
                "            arr[k] = R[j]\n"
                "            j += 1\n"
                "            k += 1"
            ),
            "Quick Sort": (
                "Quick Sort:\n"
                "def quick_sort(arr):\n"
                "    def partition(low, high):\n"
                "        pivot = arr[high]\n"
                "        i = low - 1\n"
                "        for j in range(low, high):\n"
                "            if arr[j] < pivot:\n"
                "                i += 1\n"
                "                arr[i], arr[j] = arr[j], arr[i]\n"
                "        arr[i + 1], arr[high] = arr[high], arr[i + 1]\n"
                "        return i + 1\n"
                "\n"
                "    def quick_sort_recursive(low, high):\n"
                "        if low < high:\n"
                "            pi = partition(low, high)\n"
                "            quick_sort_recursive(low, pi - 1)\n"
                "            quick_sort_recursive(pi + 1, high)\n"
                "\n"
                "    quick_sort_recursive(0, len(arr) - 1)"
            )
        }



        description_menu.update_text(descriptions[selected_sort])

    update_description()  # Initialize with the first option

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
                end_time = time.time()  # Get the current time when sorting ends
                execution_time = round((end_time - start_time), 4)  # Calculate the elapsed time

        sort_name = dropdown.get_algorithm_name()
        complexity = dropdown.get_complexity()

        draw(draw_info, buttons, dropdown, sort_name, complexity, ascending, execution_time, show_description, description_menu)

        pygame.display.update()  # Update the display after all drawing is done

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.VIDEORESIZE:
                draw_info.width, draw_info.height = event.w, event.h
                draw_info.window = pygame.display.set_mode((draw_info.width, draw_info.height), pygame.RESIZABLE)
                draw_info.set_list(draw_info.lst)

                button_positions, dropdown_x = draw_info.calculate_button_positions(num_buttons, dropdown_width)

                sort_button.rect.topleft = button_positions[0]
                reset_button.rect.topleft = button_positions[1]
                ascend_button.rect.topleft = button_positions[2]
                descend_button.rect.topleft = button_positions[3]
                description_button.rect.topleft = button_positions[4]

                dropdown.rect.topleft = (dropdown_x, 75)
                dropdown.option_rects = [pygame.Rect(dropdown_x, 75 + (i + 1) * dropdown.rect.height, dropdown.rect.width, dropdown.rect.height) for i in range(len(dropdown.options))]

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if reset_button.is_clicked(pos):
                    lst = generate_starting_list(n, min_val, max_val)
                    draw_info.set_list(lst)
                    sorting = False
                    execution_time = 0

                elif sort_button.is_clicked(pos) and not sorting:
                    sorting = True
                    selected_sort = dropdown.get_selected_option()
                    execution_time = 0
                    start_time = time.time()  # Get the current time when sorting starts
                    sorting_algorithm_generator = selected_sort(draw_info, ascending)

                elif ascend_button.is_clicked(pos) and not sorting:
                    ascending = True

                elif descend_button.is_clicked(pos) and not sorting:
                    ascending = False

                elif description_button.is_clicked(pos) and not sorting:
                    show_description = not show_description  # Toggle the description menu visibility

            dropdown.handle_event(event, reset_execution_time)

            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                update_description()  # Update the description when the dropdown changes

    pygame.quit()

if __name__ == '__main__':
    main()
