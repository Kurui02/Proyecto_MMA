import pygame

class SpriteSheet:
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Error cargando el spritesheet {filename}: {e}")
            self.sheet = None

    def get_image(self, x, y, width, height, scale_factor):
        if not self.sheet:
            return pygame.Surface((width, height))

        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        
        if scale_factor != 1.0:
            image = pygame.transform.scale(image, (int(width * scale_factor), int(height * scale_factor)))
            
        return image

    def load_strip(self, num_frames, scale_factor=1.0):
        animation_list = []
        if self.sheet:
            total_width = self.sheet.get_width()
            frame_height = self.sheet.get_height()
            frame_width = total_width // num_frames 

            for i in range(num_frames):
                frame = self.get_image(i * frame_width, 0, frame_width, frame_height, scale_factor)
                animation_list.append(frame)
                
        return animation_list