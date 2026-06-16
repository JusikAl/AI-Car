import pygame
from neural_network import NeuralNetwork
from car import PlayerCar
    

def scale_image(img, factor):
    size = (
        round(img.get_width() * factor),
        round(img.get_height() * factor),
    )

    return pygame.transform.scale(img, size)


pygame.init()

GRASS = scale_image(
    pygame.image.load("imgs/grass.jpg"),
    2.5,
)

TRACK = scale_image(
    pygame.image.load("imgs/track.png"),
    0.9,
)

TRACK_BORDER = scale_image(
    pygame.image.load("imgs/track-border.png"),
    0.9,
)

TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

RED_CAR = scale_image(
    pygame.image.load("imgs/red-car.png"),
    0.55,
)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Car")

FPS = 60


def draw(win, images, cars):
    
    for img, pos in images:
        win.blit(img, pos)

    for car in cars:
        if car.alive:
            car.draw(win)
            car.draw_sensors(win)

    pygame.display.update()


def move_ai(car):
    sensor_data = [x / 200 for x in car.get_sensor_data()]
    outputs = car.brain.predict(sensor_data)

    turn = outputs[0]

    car.move_forward() 

    if turn > 0:
        car.rotate(left=True)
    else:
        car.rotate(right=True)


clock = pygame.time.Clock()

run = True

images = [
    (GRASS, (0, 0)),
    (TRACK, (0, 0)),
]

cars = []

for i in range(100):
    car = PlayerCar(
        max_velocity=4,
        rotation_velocity=4,
        img=RED_CAR,
        start_pos=(180, 200),
        track_border_mask=TRACK_BORDER_MASK,
        width=WIDTH,
        height=HEIGHT,
    )
    
    car.brain = NeuralNetwork()
    
    cars.append(car)

while run:
    clock.tick(FPS)

    draw(screen, images, cars)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for car in cars:
        if car.alive:
            move_ai(car)

            if car.collide(TRACK_BORDER_MASK):
                car.destroy()

    if all(not car.alive for car in cars):
        best_cars = sorted(
            cars,
            key=lambda car: car.fitness,
            reverse=True
        )

        print("Best fitness:", best_cars[0].fitness)

        run = False

pygame.quit()