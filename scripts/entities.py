import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

    def rect(self): # returns the rectangle of the entity
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)): # updates the entity's position and checks for collisions

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1]) # calculate movement for this frame
        # note we combine movement (an argument) with velocity (an attribute) to allow for both player input and other forces, e.g. gravity

        self.pos[0] += frame_movement[0] # horizontal movement
        entity_rect = self.rect() # get the rectangle of the entity

        for rect in tilemap.physics_rects_around(self.pos):

            if entity_rect.colliderect(rect): # check for collision

                # stop the rectangle from moving and set collision flag
                if frame_movement[0] > 0: 
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                    
                self.pos[0] = entity_rect.x # lock the entity to the rectangle

        self.pos[1] += frame_movement[1] # vertical movement
        entity_rect = self.rect() # get the rectangle of the entity

        for rect in tilemap.physics_rects_around(self.pos):

            if entity_rect.colliderect(rect): # check for collision

                # stop the rectangle from moving and set collision flag
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True

                self.pos[1] = entity_rect.y # lock the entity to the rectangle

        self.velocity[1] = min(5, self.velocity[1] + 0.1) # apply gravity

        if self.collisions['down'] or self.collisions['up']: # reset vertical velocity
            self.velocity[1] = 0
            self.collisions['down'] = False
            self.collisions['up'] = False

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1])) # render the entity to the given surface

