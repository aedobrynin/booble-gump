from platforms_handler import PlatformsHandler
from monsters_handler import MonstersHandler


class EntitiesHandler:
    def __init__(self, world_boundings, p_images_dir, p_sounds_dir,
                 m_images_dir, m_sounds_dir):
        self.platforms_handler = \
            PlatformsHandler(world_boundings, p_images_dir, p_sounds_dir)
        self.monsters_handler = \
            MonstersHandler(world_boundings, m_images_dir, m_sounds_dir)

    @property
    def platforms(self):
        return self.platforms_handler

    @property
    def monsters(self):
        return self.monsters_handler

    def make_harder(self):
        self.platforms_handler.make_harder()
        self.monsters_handler.make_harder()

    def update(self, scroll_value, fps):
        self.platforms_handler.update(scroll_value, fps)
        self.monsters_handler.update(scroll_value, fps)

    def draw(self, surface):
        self.platforms_handler.draw(surface)
        self.monsters_handler.draw(surface)
