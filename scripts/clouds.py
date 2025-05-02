import random

class Cloud:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth


    def update(self):
        self.pos[0] += self.speed


    def render(self, surf, offset=(0, 0)):
        # render the cloud to the given surface, using the offset to make it appear in the right place
        render_pos = (self.pos[0] - offset[0] * self.depth, \
                      self.pos[1] - offset[1] * self.depth)
        # wrap the cloud around the screen
        surf.blit(self.img, (render_pos[0] % (surf.get_width() + self.img.get_width()) - self.img.get_width(), \
                             render_pos[1] % (surf.get_height() + self.img.get_height()) - self.img.get_height()))

class Clouds:
    def __init__(self, cloud_images, count=16):
        self.clouds = []

        for i in range(count): # create [count] new clouds with a random position, image, speed and depth
            new_cloud = Cloud((random.random() * 99999, random.random() * 99999), \
                                random.choice(cloud_images), \
                                    random.random() * 0.05 + 0.05, \
                                        random.random() * 0.6 + 0.2)
            self.clouds.append(new_cloud)

        self.clouds.sort(key=lambda x: x.depth) # sort clouds by depth, so we can render them in order

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surf, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surf, offset) # render the cloud to the given surface