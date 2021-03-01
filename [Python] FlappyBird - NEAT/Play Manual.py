
"""This class is for playing flappy bird manually without artifiial Intelligence"""
from Parameters import *
from Arena import *
from Bird import *
from Vector import *

class main:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.initiate()
        self.updateArena()

    def initiate(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()

    def gameOver(self):
        if self.bird.birdPosition[1] > self.arena.groundPosition[1]:
            self.runing = False

        dominant = str(self.arena.pipeDominant)
        self.pipePosition = eval("self.arena.upperPositionPipe"+dominant)

        topPosition = self.pipeHeight + self.pipePosition[1]
        bottomPosition = topPosition + self.arena.deltaPipe


        if self.bird.birdPosition[1] + self.bird.birdStay.get_height() <= topPosition and self.pipePosition[0] <= self.bird.birdPosition[0] + self.bird.birdStay.get_width():
            self.runing = False
        if self.bird.birdPosition[1] +  self.bird.birdStay.get_height() >= bottomPosition and self.pipePosition[0] <= self.bird.birdPosition[0]+ self.bird.birdStay.get_width()  :
            self.runing = False



    def updateArena(self):
        self.vector = Vector
        self.arena = Arena()
        self.pipeHeight = self.arena.upperPipe1.get_height()
        self.pipeWidth = self.arena.upperPipe1.get_width()

        self.bird = Bird()
        self.runing = True

        while self.runing == True:
            self.clock.tick(30)



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.jump(event.key)

            self.arena.moveImage()
            #Draw Arena
            self.arena.drawBackground(self.surface)
            self.arena.drawPipe(self.surface)
            self.arena.drawBase(self.surface)
            self.arena.drawScore(self.surface)

            #Draw Bird
            self.bird.drawBIrd(self.surface)
            self.bird.movement()

            self.gameOver()
            horizontalDistance, verticalDistance = self.vector.distance(self.bird.birdPosition, self.pipePosition, self.pipeHeight)

            self.screen.blit(self.surface, (0, 0))

            # pygame.display.flip()
            pygame.display.update()


if __name__ == '__main__':
    main()