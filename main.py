import os
import sys
import simplepbr
from direct.gui.DirectGui import *
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from panda3d.core import VBase4, NodePath

# CONFIG
# ConfigVariableBool("fullscreen", 0).setValue(1)
load_prc_file("myConfig.prc")

#ZMIENNE
index_character_folder = 1
index_character = 1
index_enviroment = 1
rotate_character = 0


class Demo(ShowBase):

    #PRE
    def checkfile(directory, filename):
        full_path = os.path.join(directory, filename)

        if not os.path.isdir(directory):
            print(f"Directory {directory} doesn't exist")
            return False

        if os.path.isfile(full_path):
            print(f"Found {filename} in {directory}")
            return True
        else:
            print(f"File {filename} not found")
            return False

    def loadingscreen(self, state):
        if state:
            if not hasattr(self, 'loadingScreenNode'):
                quad = CardMaker("loading_screen")
                quad.setFrameFullscreenQuad()

                self.loadingScreenNode = self.render2d.attachNewNode(quad.generate())
                self.loadingScreenNode.setTexture(loader.loadTexture('Assets/Hud/2.jpg'))

                self.loadingText = OnscreenText("Arkadiusz Klimek\nAntoni Knapczyk\n\nAGH 2025",
                                                2,
                                                fg=(1, 1, 1, 1),
                                                pos=(0, 0),
                                                align=TextNode.ACenter,
                                                scale=0.1)

            for a in range(4):
                self.graphicsEngine.renderFrame()

        else:
            if hasattr(self, 'loadingScreenNode'):
                self.loadingScreenNode.removeNode()
                self.loadingText.removeNode()

                del self.loadingScreenNode
                del self.loadingText

    def cameralocation(self):
        self.disableMouse()

        self.camLens.set_fov(75)
        self.cam.set_hpr(0, -10, 0)
        self.cam.set_pos(-0.5, -0.7, 1.5)

        self.lastMouseX = 0
        self.accept("mouse1", self.startMouseTask)
        self.accept("mouse1-up", self.stopMouseTask)

    #INIT
    def __init__(self):
        ShowBase.__init__(self)
        self.loadingscreen(True)
        self.loadModels()
        self.createlight()
        self.cameralocation()
        self.setskybox()
        self.setfog()
        self.createGUI()
        self.loadingscreen(False)
        self.fog_enabled = True

        simplepbr.init(
            use_normal_maps=True,
            enable_fog=True,
            enable_shadows=True,
            max_lights=1,
        )

        self.myMusic = self.loader.loadSfx('Assets/Audio/1.mp3')
        self.ambient = self.loader.loadSfx('Assets/Audio/ambient.mp3')
        self.ambient.play()

    #MYSZ
    def startMouseTask(self):
        self.taskMgr.add(self.mouseTask, "mouseTask")

    def stopMouseTask(self):
        self.taskMgr.remove("mouseTask")

    def mouseTask(self, task):
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()
            mouseX = mpos.getX()

            deltaX = mouseX - self.lastMouseX

            currentH = self.camera.getH()
            self.camera.setH(currentH - deltaX * 80)

            self.lastMouseX = mouseX

        return task.cont

    #SLIDER POSTACI
    def characterrotate(self):
        global rotate_character
        self.characters.setHpr(rotate_character, 0, 0)

    def slider(self):
        global rotate_character
        rotate_character = self.slider['value']
        self.characterrotate()

    #LIGHT
    def createlight(self):
        self.ambient = AmbientLight('ambient')

        self.ambient.setColor(VBase4(0.05, 0.07, 0.05, 1.0))
        self.ambient = render.attachNewNode(self.ambient)
        render.setLight(self.ambient)
        render.setShaderAuto()

    def setfog(self):
        fog = Fog("fog")
        fog.set_mode(Fog.MExponentialSquared)
        fog.set_color(0.05, 0.06, 0.05)
        fog.set_exp_density(0.07)
        render.set_fog(fog)
        render.setShaderAuto()
        self.fog_node = fog

    def setskybox(self):
        self.skybox = loader.loadModel("Assets/Enviroment/1/skybox/scene1.gltf")
        self.skybox.setScale(1000)
        self.skybox.reparentTo(render)
        self.skybox.setShaderOff()
        self.skybox.setBin('background', 0)
        self.skybox.setDepthWrite(1)
        self.skybox.setLightOff(1)

    # LOADERY
    def loadModels(self):
        global index_character, index_enviroment, index_character_folder

        self.characters = loader.loadModel(f"Assets/Characters/{index_character_folder}/{index_character}.gltf")
        self.characters.reparentTo(render)
        self.characters.setScale(1, 1, 1)
        self.characters.setPos(0, 2, 0)
        self.characters.setHpr(0, 0, 0)

        self.enviroment = loader.loadModel(f"Assets/Enviroment/{index_enviroment}/scene.gltf")
        self.enviroment.reparentTo(render)

    def swapcharacter(self, direction=1):
        global index_character, rotate_character

        max_models = 50
        folder = index_character_folder

        for _ in range(max_models):
            index_character += direction

            if index_character < 1:
                index_character = max_models
            if index_character > max_models:
                index_character = 1

            path = f"Assets/Characters/{folder}/{index_character}.gltf"
            if os.path.exists(path):
                break
        else:
            return

        if hasattr(self, 'characters') and self.characters:
            self.characters.removeNode()

        self.characters = loader.loadModel(path)
        self.characters.reparentTo(render)
        self.characters.setScale(1, 1, 1)
        self.characters.setPos(0, 2, 0)
        self.characters.setHpr(rotate_character, 0, 0)

    def swapenviroment(self, direction=1):
        global index_enviroment

        max_envs = 50

        for _ in range(max_envs):
            index_enviroment += direction

            if index_enviroment < 1:
                index_enviroment = max_envs
            if index_enviroment > max_envs:
                index_enviroment = 1

            path = f"Assets/Enviroment/{index_enviroment}/scene.gltf"
            if os.path.exists(path):
                break
        else:
            return

        if hasattr(self, 'enviroment') and self.enviroment:
            self.enviroment.removeNode()


        self.enviroment = loader.loadModel(path)
        self.enviroment.reparentTo(render)

    def swapcharacterfolder(self, direction=1):
        global index_character_folder, index_character, rotate_character

        max_folders = 50

        for _ in range(max_folders):
            index_character_folder += direction

            if index_character_folder < 1:
                index_character_folder = max_folders
            if index_character_folder > max_folders:
                index_character_folder = 1

            index_character = 1
            path = f"Assets/Characters/{index_character_folder}/{index_character}.gltf"

            if os.path.exists(path):
                break
        else:
            return

        if hasattr(self, 'characters') and self.characters:
            self.characters.removeNode()


        self.characters = loader.loadModel(path)
        self.characters.reparentTo(render)
        self.characters.setScale(1, 1, 1)
        self.characters.setPos(0, 2, 0)
        self.characters.setHpr(rotate_character, 0, 0)

    #MISC
    def audioplay(self):
        if self.myMusic.status() == AudioSound.PLAYING:
            self.myMusic.stop()
        else:
            self.myMusic.setVolume(0.5)
            self.myMusic.play()

    def toggleFog(self):
        if self.fog_enabled:
            render.clearFog()
        else:
            render.set_fog(self.fog_node)
        self.fog_enabled = not self.fog_enabled

    def createGUI(self):
        self.text_character = OnscreenText(text="CHARACTER", pos=(0.435, -0.2), scale=0.1, fg=(1, 0, 0, 1),
                                           align=TextNode.ACenter, parent=self.a2dTopLeft)

        self.text_preset = OnscreenText(text="PRESET", pos=(0.45, -0.5), fg=(1, 1, 1, 1), align=TextNode.ACenter,
                                        parent=self.a2dTopLeft)
        self.poprzedni_typ_postaci = DirectButton(
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            scale=0.03,
            command=lambda: self.swapcharacterfolder(-1),
            pos=(0.25, 0, -0.48),
            image="Assets/Hud/left.png",
            parent=self.a2dTopLeft
        )

        self.kolejny_typ_postaci = DirectButton(
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            scale=0.03,
            command=lambda: self.swapcharacterfolder(1),
            pos=(0.65, 0, -0.48),
            image="Assets/Hud/right.png",
            parent=self.a2dTopLeft
        )

        self.text_skin = OnscreenText(text="SKIN", pos=(0.45, -1), fg=(1, 1, 1, 1), align=TextNode.ACenter,
                                      parent=self.a2dTopLeft)
        self.poprzednia_postac = DirectButton(
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            scale=0.03,
            command=lambda: self.swapcharacter(-1),
            pos=(0.25, 0, -0.98),
            image="Assets/Hud/left.png",
            parent=self.a2dTopLeft
        )

        self.kolejna_postac = DirectButton(
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            scale=0.03,
            command=lambda: self.swapcharacter(1),
            pos=(0.65, 0, -0.98),
            image="Assets/Hud/right.png",
            parent=self.a2dTopLeft
        )

        self.text_background = OnscreenText(text="BACKGROUND", pos=(-0.45, -0.15), scale=0, fg=(0, 1, 0, 1),
                                            align=TextNode.ACenter, parent=self.a2dTopRight)
        self.poprzednia_mapa = DirectButton(
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            scale=0.03,
            command=lambda: self.swapenviroment(-1),
            pos=(-0.72, 0, -0.13),
            image="Assets/Hud/left.png",
            parent=self.a2dTopRight
        )

        self.kolejna_mapa = DirectButton(
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            scale=0.03,
            command=lambda: self.swapenviroment(1),
            pos=(-0.18, 0, -0.13),
            image="Assets/Hud/right.png",
            parent=self.a2dTopRight
        )

        self.exit = DirectButton(
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            text=("EXIT"),
            scale=0.05,
            command=lambda: sys.exit(),
            pos=(-0.2, 0, 0.1),
            parent=self.a2dBottomRight
        )
        self.audio = DirectButton(
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            scale=0.035,
            command=self.audioplay,
            pos=(0.1, 0, 0.1),
            image="Assets/Audio/play.png",
            parent=self.a2dBottomLeft
        )

        self.fog = DirectButton(
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            scale=0.035,
            command=self.toggleFog,
            pos=(0.25, 0, 0.1),
            image="Assets/Hud/fog.png",
            parent=self.a2dBottomLeft
        )

        self.slider = DirectSlider(
            range=(0, 720),
            value=rotate_character,
            pageSize=1,
            command=self.slider,
            pos=(0, 0, 0.1),
            scale=0.3,
            parent=self.a2dBottomCenter,
            thumb_frameColor=(1, 1, 1, 0.25),
            frameColor=(1, 1, 1, 0.15),
            text_fg=(0, 1, 0, 1)
        )

        myFrame = DirectFrame(frameColor=(0, 0, 0, 0.35), frameSize=(-10, -0.5, -10, 10), pos=(1.4, 0, 0),
                              parent=self.a2dLeftCenter)

        self.poprzednia_mapa.setTransparency(TransparencyAttrib.MAlpha)
        self.kolejna_mapa.setTransparency(TransparencyAttrib.MAlpha)
        self.poprzednia_postac.setTransparency(TransparencyAttrib.MAlpha)
        self.kolejna_postac.setTransparency(TransparencyAttrib.MAlpha)
        self.poprzedni_typ_postaci.setTransparency(TransparencyAttrib.MAlpha)
        self.kolejny_typ_postaci.setTransparency(TransparencyAttrib.MAlpha)
        self.audio.setTransparency(TransparencyAttrib.MAlpha)
        self.fog.setTransparency(TransparencyAttrib.MAlpha)


app = Demo()
app.run()