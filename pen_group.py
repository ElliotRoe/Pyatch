import pygame
from sprite import Sprite

# This class is for pyatch sprites ONLY

class PenGroup(pygame.sprite.Group):

    def __init__(self, pen_layer_group, *sprites):
        pygame.sprite.Group.__init__(self)
        self.add(*sprites)
        self.target_pen_group = pen_layer_group

    def draw(self, surface):
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        for sprite in self.sprites():
            if sprite.pen_state():
                self.target_pen_group.add(Sprite('data/penmark.png', x = (sprite.rect.x + sprite.rect.width/2), y = sprite.rect.y + sprite.rect.height/2, scale=sprite.pen_size()/4))
            old_rect = self.spritedict[sprite]
            new_rect = surface_blit(sprite.image, sprite.rect)
            if old_rect:
                if new_rect.colliderect(old_rect):
                    dirty_append(new_rect.union(old_rect))
                else:
                    dirty_append(new_rect)
                    dirty_append(old_rect)
            else:
                dirty_append(new_rect)
            self.spritedict[sprite] = new_rect
        return dirty
