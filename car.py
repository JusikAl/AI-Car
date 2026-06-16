import math
import pygame


def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center
    )
    win.blit(rotated_image, new_rect.topleft)


class Car:
    def __init__(
        self,
        max_velocity,
        rotation_velocity,
        img,
        start_pos,
        track_border_mask,
        width,
        height
    ):
        self.max_velocity = max_velocity
        self.velocity = 0
        self.rotation_velocity = rotation_velocity
        self.angle = 0

        self.img = img
        self.x, self.y = start_pos

        self.acceleration = 0.1
        self.alive = True

        self.sensors_angle = [-60, -30, 0, 30, 60]

        self.track_border_mask = track_border_mask
        self.width = width
        self.height = height
        
        self.distance_traveled = 0
        self.fitness = 0

    def rotate(self, left=False, right=False):
        if self.velocity == 0:
            return

        if left:
            self.angle += self.rotation_velocity
        elif right:
            self.angle -= self.rotation_velocity

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.velocity = min(
            self.velocity + self.acceleration,
            self.max_velocity
        )
        self.move()

    # def move_backward(self):
    #     self.velocity = max(
    #         self.velocity - self.acceleration,
    #         -self.max_velocity / 2
    #     )
    #     self.move()

    def move(self):
        radians = math.radians(self.angle)

        vertical = math.cos(radians) * self.velocity
        horizontal = math.sin(radians) * self.velocity

        self.x -= horizontal
        self.y -= vertical
        
        distance = abs(self.velocity)
        self.distance_traveled += distance
        self.fitness = self.distance_traveled

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)

        offset = (int(self.x - x), int(self.y - y))

        return mask.overlap(car_mask, offset)

    def get_sensor_distance(self, angle, max_length=200):
        sensor_angle = math.radians(self.angle + angle)

        start_x = self.x + self.img.get_width() // 2
        start_y = self.y + self.img.get_height() // 2

        for distance in range(max_length):
            x = int(start_x - math.sin(sensor_angle) * distance)
            y = int(start_y - math.cos(sensor_angle) * distance)

            if x < 0 or x >= self.width:
                return distance

            if y < 0 or y >= self.height:
                return distance
            if self.track_border_mask.get_at((x, y)):
                return distance

        return max_length

    def get_sensor_data(self):
        data = []

        for angle in self.sensors_angle:
            data.append(self.get_sensor_distance(angle))

        return data

    def draw_sensors(self, win):
        start_x = self.x + self.img.get_width() // 2
        start_y = self.y + self.img.get_height() // 2

        for angle in self.sensors_angle:
            distance = self.get_sensor_distance(angle)

            sensor_angle = math.radians(self.angle + angle)

            end_x = start_x - math.sin(sensor_angle) * distance
            end_y = start_y - math.cos(sensor_angle) * distance

            pygame.draw.line(
                win,
                (0, 255, 0),
                (start_x, start_y),
                (end_x, end_y),
                2,
            )

            pygame.draw.circle(
                win,
                (255, 0, 0),
                (int(end_x), int(end_y)),
                4,
            )


class PlayerCar(Car):
    def reduce_speed(self):
        self.velocity = max(
            self.velocity - self.acceleration / 2,
            0,
        )

        self.move()

    def destroy(self):
        self.alive = False