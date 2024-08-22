import pygame

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
        return self.selected_option
