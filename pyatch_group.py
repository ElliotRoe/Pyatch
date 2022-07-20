import pygame
from sprite import Sprite


# This class is for pyatch sprites ONLY
# NOTE: This class has somewhat of a misleading name. This is not used to store a group of sprites that visually
# represents a sprite's pen path. This functions as a regular group but it also adds the

class PyatchGroup(pygame.sprite.Group):

    def __init__(self, *sprites):
        pygame.sprite.Group.__init__(self)
        self.add(*sprites)

    def draw(self, surface):
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        for sprite in self.sprites():
            old_rect = self.spritedict[sprite]
            sprite.image.set_colorkey(sprite.key_color)
            # print(pygame.surfarray.array3d(sprite.image.convert_alpha())[0, 0])
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
            if sprite.has_say():
                surface_blit(sprite.say_bubble, (sprite.rect.x + sprite.rect.width, sprite.rect.y))
        return dirty
