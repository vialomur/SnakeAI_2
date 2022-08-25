from agent import *
from snake import *

rectangle = pygame.Rect(x_pos, y_pos, width, height)
x_push = 0
y_push = 0
move = 0

fpsClock = pygame.time.Clock()
FPS = 120
food_alive = False
food = None
max_score = 1

if __name__ == '__main__':
    surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    srodowisko = f'{rectangle.x} {rectangle.y} {0} {0}'
    my_agent = Agent()

    for game in range(5_000):
        run = True
        rectangle = pygame.Rect(x_pos, y_pos, width, height)
        score = 1
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if not food_alive:
                food = make_food()
                food_alive = True

            my_agent.x = rectangle.x
            my_agent.y = rectangle.y
            action = my_agent.predict([food.x, food.y],game)
            did_collide = False
            did_lose = False
            if action == 0:
                move = LEFT
                x_push = -60
            if action == 1:
                move = UP
                y_push = -60
            if action == 2:
                move = RIGHT
                x_push = 60
            if action == 3:
                move = DOWN
                y_push = 60

            if check_borders(rectangle, x_push, y_push, move) == -1:
                did_lose = True
                run = False
                x_push = 0
                y_push = 0

            if rectangle.colliderect(food):
                food_alive = False
                score += 1
                did_collide = True

            my_agent.x = rectangle.x
            my_agent.y = rectangle.y
            my_agent.learn(did_lose, did_collide, action, [food.x, food.y],game)

            surface.fill((255, 255, 255))
            name_font = pygame.font.SysFont('arial', 50)
            score_txt = name_font.render(str(score), True, (255, 0, 255))
            game_txt = name_font.render(str(game), True, (255, 0, 255))
            surface.blit(game_txt, (60, 20))
            surface.blit(score_txt, (810, 20))
            make_rect(surface, rectangle)
            pygame.draw.rect(surface, (0, 255, 0), food)
            fpsClock.tick(FPS)
            if max_score < score:
                max_score = score
                with open("values.txt", 'w') as fp:
                    fp.write(str(my_agent.weights))

            pygame.display.update()
            # print(did_lose, end=' ')
            # print(my_agent.weights)
            # print("Actions:",my_agent.actions)
            # print(action)
            # check_position(my_agent.srodowisko, my_agent.stan)
            # print("Randint ",random.randint(0,3))

print("Max score:", max_score)
