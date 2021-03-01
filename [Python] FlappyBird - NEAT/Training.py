"""This class is used to train AI to play flappy Bird"""

from Arena import *
from Bird import *
from Parameters import *
from Vector import *
from NeuralNetwork import *


class TrainingBird:
    def __init__(self, populationSize, mutationRate, parentNumber, shape):
        self.queue = Queue()
        self.populationSize = populationSize
        self.mutationRate = mutationRate
        self.shape = shape
        self.parentNumber = parentNumber
        self.neuralNetowk = NeuralNetwork(self.shape)
        self.update()

    def update(self):
        self.createPopulation()
        self.populationFitness = self.calculateFitnessPopulation(self.population)
        generation = 0

        while generation < 300:
            print("\nGeneration: " + str(generation))
            self.selectParent()
            self.createChild()
            self.population = self.population + self.parents + self.children
            self.populationFitness = self.populationFitness + self.parentsFitness + self.childrenFitnesss

            # Soering
            popSorting = np.argsort(self.populationFitness)[-self.populationSize:]
            popSorting = popSorting[::-1]
            self.population = [self.population[x] for x in popSorting]
            self.populationFitness = [self.populationFitness[x] for x in popSorting]

            generation+=1
            for i in range(10):
                np.save("TrainingResult/Training Gen" + str(generation) + "_Parent-" + str(i) + "_" + str(self.populationFitness[i]) + ".npy",self.population[i])
            # self.runBird(self.population[0], display=True)
            print('\n top 6 Best Fitness: ' + str(self.populationFitness[0:6]))
            print('\n Lowest 6 Fitness: ' + str(self.populationFitness[-6:]))


    def createChild(self):
        """
        using 2 crossover method and only pick the best one to append as children
        children = list([children1],....,[childrenN])
        :return:
        """
        self.children = []
        self.childrenFitnesss = []
        parent = list(permutations(self.parents, 2))
        iteration = len(parent) if len(parent) < self.populationSize else self.populationSize
        np.random.shuffle(parent)
        maxChild = 0
        sys.stdout.write('\n')
        sys.stdout.flush()
        for i in range(iteration):
            sys.stdout.write('\r' + "Progress Children: " + str(100 * (i + 1) / self.populationSize) + "\t" +
                             "maximum Children Fitness: " + str(maxChild))
            sys.stdout.flush()
            parent1 = parent[i][0]
            parent2 = parent[i][1]
            child1, child2 = self.crossOver(parent1, parent2)
            child3, child4 = self.crossOver(self.mutation(parent1), self.mutation(parent2))
            popChild = [self.mutation(child1), self.mutation(child2), self.mutation(child3), self.mutation(child4)]
            fitChild = self.calculateFitnessPopulation(popChild)
            winner = popChild[np.argmax(fitChild)]
            self.children.append(winner)
            self.childrenFitnesss.append(max(fitChild))
            if max(fitChild) > maxChild:
                maxChild = max(fitChild)

    def crossOver(self, parent1, parent2):
        """Cross over type 2 is on;ly swipe neuron in a layer or making a sum of percentage*weight1 + percentage2*weight2
        where percentage1+percentage2 must equal to 1
        :return 2 new Individu
        """
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)

        # Weights Cross Over
        for index1 in range(len(child1[0])):
            for index2 in range(len(child1[0][index1])):
                lenIndex2 = len(parent1[0][index1][index2]) // 2
                child1[0][index1][index2][-lenIndex2:] = parent2[0][index1][index2][-lenIndex2:]
                child2[0][index1][index2][-lenIndex2:] = parent1[0][index1][index2][-lenIndex2:]

        # Biases Cross Over
        for index1 in range(len(child1[1])):
            value = np.random.rand(1)
            child1[1][index1] = value * parent1[1][index1] + (1-value) * parent2[1][index1]
            child2[1][index1] = (1-value) * parent1[1][index1] + value * parent2[1][index1]
        return child1, child2
    def mutation(self, individu):
        """
        Mutate Individu
        :param individu: list([Weights],[Biases])
        :return: mutated individu: list([Weights],[Biases])
        """
        mutated = np.array(copy.deepcopy(individu))

        # Weight Mutation
        weights = mutated[0]
        biases = mutated[1]

        # Weights mutation
        for index1, weights1 in enumerate(weights):
            for index2, weights2 in enumerate(weights1):
                for index3, weights3 in enumerate(weights2):
                    random = np.random.rand(1)
                    if random < self.mutationRate:
                        mutated[0][index1][index2][index3] = np.random.randn()
        for index1, bias1 in enumerate(biases):
            for index2, bias2 in enumerate(bias1):
                random = np.random.rand(1)
                if random < self.mutationRate:
                    mutated[1][index1][index2] = np.random.randn()
        return mutated

    def selectParent(self):
        sortingIndex = np.argsort(self.populationFitness)[-10:]
        self.parents = [self.population[i] for i in sortingIndex]
        self.parentsFitness = self.calculateFitnessPopulation(self.parents)


    def calculateFitnessPopulation(self, population):
        populationFitness = []

        for i in range(len(population)):
            fitness = self.calculateFitness(population[i])
            populationFitness.append(fitness)
        return populationFitness
    def calculateFitness(self, individu, display = False):

        score1 = self.runBird(individu, display)
        score2 = self.runBird(individu, display)
        score3 = self.runBird(individu, display)

        return np.mean([score1,score2,score3])
    def createPopulation(self):
        self.population = []
        for _ in range(self.populationSize):
            weight = self.neuralNetowk.createWeight()
            biases = self.neuralNetowk.createBiasses()
            self.population.append([weight, biases])
    def gameOver(self, bird, arena):
        runing = True
        pipeHeight = arena.upperPipe1.get_height()

        if bird.birdPosition[1] > arena.groundPosition[1]:
            runing = False

        dominant = str(arena.pipeDominant)
        pipePosition = eval("arena.upperPositionPipe"+dominant)

        topPosition = pipeHeight + pipePosition[1]
        bottomPosition = topPosition + arena.deltaPipe


        if bird.birdPosition[1] + bird.birdStay.get_height() <= topPosition and pipePosition[0] <= bird.birdPosition[0] + bird.birdStay.get_width():
            runing = False
        if bird.birdPosition[1] +  bird.birdStay.get_height() >= bottomPosition and pipePosition[0] <= bird.birdPosition[0]+ bird.birdStay.get_width():
            runing = False
        return runing, pipePosition

    def runBird(self, individu, display = False):
        vector = Vector
        arena = Arena()
        pipeHeight = arena.upperPipe1.get_height()

        bird = Bird()
        running = True
        age = 0

        if display:
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            surface = pygame.Surface(screen.get_size())
            surface = surface.convert()
            clock = pygame.time.Clock()

        while running:
           arena.moveImage()
           # Draw Arena
           if display:
               arena.drawBackground(surface)
               arena.drawPipe(surface)
               arena.drawBase(surface)
               arena.drawScore(surface)

               # Draw Bird
               bird.drawBIrd(surface)
           bird.movement()
           running, pipePosition = self.gameOver(bird, arena)

           # Working with vector
           horizontalDistance, verticalDistance = vector.distance(bird.birdPosition, pipePosition, pipeHeight)
           input = np.array([horizontalDistance, verticalDistance])

           #Working with Neural Network
           feedForward = self.neuralNetowk.feedForward(input, individu[0], individu[1])
           bird.neuralNetworkJump(feedForward)

           if display:
               clock.tick(30)
               screen.blit(surface, (0, 0))
               pygame.display.update()
               for event in pygame.event.get():
                   if event.type == pygame.QUIT:
                       running = False
                   elif event.type == pygame.KEYDOWN:
                       if event.key == pygame.K_SPACE:
                           bird.jump(event.key)
           age +=1
        return arena.score + age

if __name__ == '__main__':
    TrainingBird(POPULATINO_SIZE, MUTATION_RATE, PARENTNUMBER, shape)