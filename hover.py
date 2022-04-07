class Option:
    def __init__(self, text, pos, screen, font):
        self.hovered = False
        self.text = text
        self.pos = pos
        self.display = screen   # screen: pygaem.display
        self.font = font
        self.set_label_box()
            
    def draw(self):
        self.set_label()
        self.display.blit(self.label, self.label_box)

    def set_label(self):   # font;pygame.font.Font
        self.label = self.font.render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.hovered:
            return (255, 255, 255)
        else:
            return (100, 100, 100)
        
    def set_label_box(self):
        self.set_label()
        self.label_box = self.label.get_rect()
        self.label_box.center = self.pos

    def get_coordinate(self):
        return self.label_box.topleft + self.label_box.bottomright
        
