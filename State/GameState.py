import pygame, sys
sys.path.append('..')
import Game
from Control.Button import *
from Manager.EntityManager import *

class GameSate:
    level = 1
    def __init__(self, game: Game):
        self.game = game
        self.bg = pygame.image.load('resource/img/Background/Background2.png').convert()
        self.Surface = pygame.Surface(Globals.display.get_size())
        self.score = 0
        self.time = 0
        self.speed = 0

    def __del__(self):
        pass

    def Update(self):
        pass

    def Draw(self):
        pass

class MenuSate(GameSate):
    def __init__(self, game: Game):
        super().__init__(game)
        self.playBtn = Button('resource/img/Button/Play Button.png', pygame.Rect(176.00, 110.00, 120, 40))
        self.quitBtn = Button('resource/img/Button/Quit Button.png', pygame.Rect(176.00, 160.00, 120, 40))

        self.buttons = [
            self.playBtn,
            self.quitBtn
        ]

    def Update(self):
        for btn in self.buttons:
            btn.Update()

        if self.playBtn.isClick:
            self.game.ChangeState(StorySate(self.game))
            # self.game.ChangeState(RunningState(self.game, self.level))

        if self.quitBtn.isClick:
            Globals.running = False
        
    def Draw(self):
        Globals.Surface.blit(pygame.transform.scale(self.bg, Globals.Surface.get_size()), (0, 0))
        for btn in self.buttons:
            btn.Draw()

class StorySate(GameSate):
    def __init__(self, game: Game):
        super().__init__(game)
        self.story_pic = pygame.image.load('resource/img/Background/story_pic.jpg').convert()

    def Update(self):
        Globals.ShowText = True
        Globals.Text.fill((0, 0, 0, 0))

        if InputManager.CurrentKey[pygame.K_SPACE] and not InputManager.PreviousKey[pygame.K_SPACE]:
            self.game.ChangeState(RunningState(self.game, self.level))
        
    def Draw(self):
        Globals.Text.blit(pygame.transform.scale(self.story_pic, Globals.Text.get_size()), (0, 0))

class RunningState(GameSate):
    def __init__(self, game: Game, level):
        super().__init__(game)
        self.enityManager = EntityManager(level)
        pygame.mixer.music.load("resource/Music/bg_music.ogg")
        pygame.mixer.music.play(-1, 0.0, 3000)
        # pygame.mouse.set_visible(False)

    def __del__(self):
        return super().__del__()

    def Update(self):
        if InputManager.CurrentKey[pygame.K_ESCAPE] and not InputManager.PreviousKey[pygame.K_ESCAPE]:
            self.game.SaveState()
            pygame.mixer.music.fadeout(1000)
            pygame.mouse.set_visible(True)
            self.game.ChangeState(StopSate(self.game)) 

        if Globals.IsLevelEnd:
            Globals.IsLevelEnd = False
            pygame.mixer.music.stop()
            pygame.mouse.set_visible(True)
            SoundManager.PlaySound("WinGame")
            if self.level+1 <= 3:
                self.game.ChangeState(ChangeLevelState(self.game))
            self.level = 1
            self.game.ChangeState(GameWin(self.game))
        elif Globals.GameOver:
            Globals.GameOver = False
            pygame.mixer.music.stop()
            pygame.mouse.set_visible(True)
            SoundManager.PlaySound("LoseGame")
            self.game.ChangeState(GameOver(self.game))
        else:
            self.enityManager.Updated()

    def Draw(self):
        self.enityManager.Draw()

class StopSate(GameSate):
    def __init__(self, game: Game):
        super().__init__(game)
        self.resumeBtn = Button('resource/img/Button/Resume Button.png', pygame.Rect(176.00, 32.00, 120, 40))
        self.newGameBtn = Button('resource/img/Button/New game Button.png', pygame.Rect(176.00, 96.00, 120, 40))
        self.quitBtn = Button('resource/img/Button/Quit Button.png', pygame.Rect(176.00, 160.00, 120, 40))

        self.buttons = [
            self.resumeBtn,
            self.newGameBtn,
            self.quitBtn
        ]

    def Update(self):
        for btn in self.buttons:
            btn.Update()

        if self.resumeBtn.isClick or InputManager.CurrentKey[pygame.K_ESCAPE] and not InputManager.PreviousKey[pygame.K_ESCAPE]:
            pygame.mixer.music.play(-1, 0.0, 1000)
            pygame.mouse.set_visible(False)
            self.game.ChangeState(self.game.PreviousState) 

        if self.newGameBtn.isClick:
            # GameSate.level = 1
            self.game.ChangeState(RunningState(self.game, self.level))

        if self.quitBtn.isClick:
            Globals.running = False

    def Draw(self):
        Globals.Surface.blit(pygame.transform.scale(self.bg, Globals.Surface.get_size()), (0, 0)) 
        for btn in self.buttons:
            btn.Draw()

class ChangeLevelState(GameSate):
    def __init__(self, game: Game):
        super().__init__(game)
        self.continuteBtn = Button('resource/img/Button/Continue Button.png', pygame.Rect(176.00, 112.00, 120, 40))
        self.newGameBtn = Button('resource/img/Button/New game Button.png', pygame.Rect(176.00, 160.00, 120, 40))
        self.quitBtn = Button('resource/img/Button/Quit Button.png', pygame.Rect(176.00, 208.00, 120, 40))
        self.speed = 0.01

        self.buttons = [
            self.continuteBtn,
            self.newGameBtn,
            self.quitBtn
        ]

    def Update(self):
        self.time += Globals.DeltaTime

        for btn in self.buttons:
            btn.Update()

        if self.time >= self.speed and self.score < Globals.score:
            SoundManager.PlaySound("coin")
            self.score+=5
            self.time=0
        
        self.text = Globals.text_font.render(f"Score: {self.score}", True, 'white')

        if self.continuteBtn.isClick:
            GameSate.level+=1
            print(GameSate.level)
            self.game.ChangeState(RunningState(self.game, GameSate.level)) 

        if self.newGameBtn.isClick:
            # GameSate.level = 1
            self.game.ChangeState(RunningState(self.game, self.level))

        if self.quitBtn.isClick:
            Globals.running = False

        Globals.ShowText = True
        Globals.Text.fill((0, 0, 0, 0))

    def Draw(self):
        Globals.Surface.blit(pygame.transform.scale(self.bg, Globals.Surface.get_size()), (0, 0))
        Globals.Text.blit(self.text, ((Globals.Text.get_width() - self.text.get_width())/2, 200))
        for btn in self.buttons:
            btn.Draw()

class GameWin(GameSate):
    def __init__(self, game: Game):
        super().__init__(game)
        self.playBtn = Button('resource/img/Button/New Game Button.png', pygame.Rect(176.00, 110.00, 120, 40))
        self.quitBtn = Button('resource/img/Button/Quit Button.png', pygame.Rect(176.00, 160.00, 120, 40))
        self.speed = 0.01
        self.buttons = [
            self.playBtn,
            self.quitBtn
        ]

    def Update(self):
        self.time += Globals.DeltaTime
        
        for btn in self.buttons:
            btn.Update()
        
        if self.time >= self.speed and self.score < Globals.score:
            SoundManager.PlaySound("coin")
            self.score+=5
            self.time=0

        self.text = Globals.text_font.render("You win!!", True, 'white')
        self.text_score = Globals.text_font.render(f"Score: {self.score}", True, 'white')


        if self.playBtn.isClick:
            self.game.ChangeState(RunningState(self.game, self.level))

        if self.quitBtn.isClick:
            Globals.running = False

        Globals.ShowText = True
        Globals.Text.fill((0, 0, 0, 0))
        
    def Draw(self):
        Globals.Surface.blit(pygame.transform.scale(self.bg, Globals.Surface.get_size()), (0, 0))
        Globals.Text.blit(self.text, ((Globals.Text.get_width() - self.text.get_width())/2, 120))
        Globals.Text.blit(self.text_score, ((Globals.Text.get_width() - self.text_score.get_width())/2, 200))
        for btn in self.buttons:
            btn.Draw()

class GameOver(GameSate):
    def __init__(self, game: Game):
        super().__init__(game)
        self.playBtn = Button('resource/img/Button/New Game Button.png', pygame.Rect(176.00, 110.00, 120, 40))
        self.quitBtn = Button('resource/img/Button/Quit Button.png', pygame.Rect(176.00, 160.00, 120, 40))
        self.speed = 0.01

        self.buttons = [
            self.playBtn,
            self.quitBtn
        ]

    def Update(self):
        self.time += Globals.DeltaTime

        for btn in self.buttons:
            btn.Update()

        if self.time >= self.speed and self.score < Globals.score:
            SoundManager.PlaySound("coin")
            self.score+=5
            self.time=0

        self.text = Globals.text_font.render("You Lose!!", True, 'white')
        self.text_score = Globals.text_font.render(f"Score: {self.score}", True, 'white')
        self.text_try = Globals.text_font.render("Try Again?", True, 'white')

        if self.playBtn.isClick:
            # self.level = 1
            self.game.ChangeState(RunningState(self.game, self.level))

        if self.quitBtn.isClick:
            Globals.running = False

        Globals.ShowText = True
        Globals.Text.fill((0, 0, 0, 0))
        
    def Draw(self):
        Globals.Surface.blit(pygame.transform.scale(self.bg, Globals.Surface.get_size()), (0, 0))
        Globals.Text.blit(self.text, ((Globals.Text.get_width() - self.text.get_width())/2, 110))
        Globals.Text.blit(self.text_score, ((Globals.Text.get_width() - self.text_score.get_width())/2, 200))
        Globals.Text.blit(self.text_try, ((Globals.Text.get_width() - self.text_try.get_width())/2, 290))
        for btn in self.buttons:
            btn.Draw()
        