"""This class to testing training result
Just change Generation number but i only gibe the 132nd generation
"""
from Arena import *
from Bird import *
from Parameters import *
from Vector import *
from NeuralNetwork import *

class AutoGame:
    def __init__(self):
        self.neuralNetwork = NeuralNetwork(shape)
        self.loadNeuralNetwork()
        self.runGame()

    def loadNeuralNetwork(self):
        generation = 132

        path = "TrainingResult/"

        for i in range(10):
            name = glob(path+ "Training Gen"+str(generation)+"_parent-"+str(i)+"*")
            globals()["neuralNetwork"+str(i)] = np.load(name[0])
        print(name)
    def gameOver(self, bird, arena):
        runing = 1
        pipeHeight = arena.upperPipe1.get_height()

        if bird.birdPosition[1] > arena.groundPosition[1]:
            runing = 0

        dominant = str(arena.pipeDominant)
        pipePosition = eval("arena.upperPositionPipe" + dominant)

        topPosition = pipeHeight + pipePosition[1]
        bottomPosition = topPosition + arena.deltaPipe

        if bird.birdPosition[1] + bird.birdStay.get_height() <= topPosition and pipePosition[0] <= bird.birdPosition[
            0] + bird.birdStay.get_width():
            runing = 0
        if bird.birdPosition[1] + bird.birdStay.get_height() >= bottomPosition and pipePosition[0] <= bird.birdPosition[
            0] + bird.birdStay.get_width():
            runing = 0
        return runing, pipePosition

    def runGame(self):
        for i in range(10):
            globals()["bird"+str(i)] = Bird()
            globals()["bird"+str(i)+"Show"] = 1
            globals()["bird" + str(i)].birdPosition = (BirdPosition[0],np.random.randint(200,300))

        vector = Vector
        arena = Arena()
        pipeHeight = arena.upperPipe1.get_height()
        running = True

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        surface = pygame.Surface(screen.get_size())
        surface = surface.convert()
        clock = pygame.time.Clock()
        passing = [1]*10
        while running:
            clock.tick(30)
            arena.moveImage()
            arena.drawBackground(surface)
            arena.drawPipe(surface)
            arena.drawBase(surface)
            arena.drawScore(surface)

            sum = 0
            for i in range(10):
                if passing[i] == 1:
                    globals()["bird" + str(i) + "Show"], pipePosition = self.gameOver(eval("bird" + str(i)), arena)
                    eval("bird"+str(i)).drawBIrd(surface)
                    eval("bird" + str(i)).movement()
                    passing[i] = globals()["bird"+str(i)+"Show"]
                    horizontalDistance, verticalDistance = vector.distance(eval("bird"+str(i)).birdPosition, pipePosition, pipeHeight)
                    input = np.array([horizontalDistance, verticalDistance])
                    # Working with Neural Network
                    feedForward = self.neuralNetwork.feedForward(input, eval("neuralNetwork"+str(i))[0], eval("neuralNetwork"+str(i))[1])
                    eval("bird"+str(i)).neuralNetworkJump(feedForward)
                elif passing[i] == 0:
                    continue

            screen.blit(surface, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if np.sum(passing) == 0:
                break
if __name__ == '__main__':
    AutoGame()