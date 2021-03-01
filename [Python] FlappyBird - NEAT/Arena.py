## This is where all arena parameters made. Pipe, background, score, ground are settle up in this class
from Parameters import *

class Arena:
    def __init__(self):
        ##Font initialization
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 70)

        ## Set Initial Score
        self.score = 0

        ### Pipe dominant refer to which pipe is near the bird (in front of bird)
        self.pipeDominant = 1

        ### Loading Several Images
        self.background = pygame.transform.scale(pygame.image.load("assets/images/bg.png"), (SCREEN_WIDTH,SCREEN_HEIGHT))
        self.ground = pygame.transform.scale(pygame.image.load("assets/images/base.png"), (SCREEN_WIDTH+200,100))
        self.pipe = pygame.image.load("assets/images/pipe.png")

        ### Horizontal Distance of Pipe
        self.deltaPipe = 120

        ### Create 3 images pipe consist of bottom and top pipe
        self.bottomPipe1, self.upperPipe1, self.lowerPositionPipe1, self.upperPositionPipe1 = self.createPipe(position="Left")
        self.bottomPipe2, self.upperPipe2, self.lowerPositionPipe2, self.upperPositionPipe2 = self.createPipe(position="Right")
        self.bottomPipe3, self.upperPipe3, self.lowerPositionPipe3, self.upperPositionPipe3 = self.createPipe(position="Left")
        self.pipe3 = False

        ### Ground Position
        self.groundPosition = (0, SCREEN_HEIGHT - self.ground.get_height())
        self.groundPosition2 = (SCREEN_WIDTH + 200, SCREEN_HEIGHT - self.ground.get_height())


    def drawScore(self, screen):
        """

        :param screen: which screen score will be displayed
        :return:
        """
        text = self.myfont.render(str(self.score),False, (255,255,255))
        screen.blit(text, (SCREEN_WIDTH/2-30,100))

    def createPipe(self, position = "Left"):
        """

        :param position:
        Left: pipe ion position x =
        :return: position of image of bottom and upper pipe and their location (x,y)
        """
        height = np.random.randint(60,370,1)
        bottomPipe = pygame.transform.scale(self.pipe, (self.pipe.get_width(), 500))
        upperPipe = pygame.transform.rotate(self.pipe, 180)
        upperPipe = pygame.transform.scale(upperPipe, (self.pipe.get_width(), 500))

        if position == "Left":
            pipePositionLower = [SCREEN_WIDTH, SCREEN_HEIGHT-self.ground.get_height()-height]
            pipePositionUpper = [SCREEN_WIDTH, -500+SCREEN_HEIGHT - self.ground.get_height() - height - self.deltaPipe]
        elif position == "Right":
            pipePositionLower = [SCREEN_WIDTH + 180, SCREEN_HEIGHT - self.ground.get_height() - height]
            pipePositionUpper = [SCREEN_WIDTH + 180, -500 + SCREEN_HEIGHT - self.ground.get_height() - height - self.deltaPipe]
        else:
            pipePositionLower = [SCREEN_WIDTH + 350, SCREEN_HEIGHT - self.ground.get_height() - height]
            pipePositionUpper = [SCREEN_WIDTH + 350, -500 + SCREEN_HEIGHT - self.ground.get_height() - height - self.deltaPipe]

        return bottomPipe, upperPipe, pipePositionLower, pipePositionUpper

    def drawBackground(self, screen):
        """

        :param screen: Where the image will be drawn
        :return:
        """

        screen.blit(self.background, (0, 0))

    def drawBase(self, screen):
        """
        Where the bese will be drawn
        :param screen:
        :return:
        """
        screen.blit(self.ground, self.groundPosition)
        screen.blit(self.ground, self.groundPosition2)

    def moveImage(self):
        """
        setting up every image movement
        :return:
        """
        ###Ground
        self.groundPosition = (self.groundPosition[0] - velocity, SCREEN_HEIGHT-100)
        self.groundPosition2 = (self.groundPosition2[0] - velocity, SCREEN_HEIGHT - 100)

        if self.groundPosition[0] <= -SCREEN_WIDTH-200:
            self.groundPosition = (SCREEN_WIDTH+200, SCREEN_HEIGHT - 100)
        elif self.groundPosition2[0] <= -SCREEN_WIDTH-200:
            self.groundPosition2 = (SCREEN_WIDTH + 200, SCREEN_HEIGHT - 100)

        ###Pipe
        self.lowerPositionPipe1 = (self.lowerPositionPipe1[0] - velocity, self.lowerPositionPipe1[1])
        self.upperPositionPipe1 = (self.upperPositionPipe1[0] - velocity, self.upperPositionPipe1[1])
        self.lowerPositionPipe2 = (self.lowerPositionPipe2[0] - velocity, self.lowerPositionPipe2[1])
        self.upperPositionPipe2 = (self.upperPositionPipe2[0] - velocity, self.upperPositionPipe2[1])

        if self.pipe3:
            self.lowerPositionPipe3 = (self.lowerPositionPipe3[0] - velocity, self.lowerPositionPipe3[1])
            self.upperPositionPipe3 = (self.upperPositionPipe3[0] - velocity, self.upperPositionPipe3[1])

        ### Checking which pipe is in front
        if self.lowerPositionPipe1[0] == BirdPosition[0] - self.pipe.get_width():
            self.pipeDominant = 2
            self.score += 1
        elif self.lowerPositionPipe2[0] == BirdPosition[0] - self.pipe.get_width():
            self.pipeDominant = 3
            self.score += 1
        elif self.upperPositionPipe3[0] == BirdPosition[0] - self.pipe.get_width():
            self.pipeDominant = 1
            self.score += 1
        ### Changing pipe after 1 pipe leave map
        if self.lowerPositionPipe1[0] == 0:
            self.pipe3 = True
            self.bottomPipe3, self.upperPipe3, self.lowerPositionPipe3, self.upperPositionPipe3 = self.createPipe(
                position="Left")

        elif self.lowerPositionPipe2[0] == 0:
            self.bottomPipe1, self.upperPipe1, self.lowerPositionPipe1, self.upperPositionPipe1 = self.createPipe(
                position="Left")


        elif self.upperPositionPipe3[0] == 0:
            self.bottomPipe2, self.upperPipe2, self.lowerPositionPipe2, self.upperPositionPipe2 = self.createPipe(
                position="Left")

    def drawPipe(self, screen):
        """

        :param screen: Where the pipe is going to drawn
        :return:
        """

        ### Blit pipe into screen
        screen.blit(self.upperPipe1, self.upperPositionPipe1)
        screen.blit(self.bottomPipe1, self.lowerPositionPipe1)
        screen.blit(self.upperPipe2, self.upperPositionPipe2)
        screen.blit(self.bottomPipe2, self.lowerPositionPipe2)
        screen.blit(self.upperPipe3, self.upperPositionPipe3)
        screen.blit(self.bottomPipe3, self.lowerPositionPipe3)
