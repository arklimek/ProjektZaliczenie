import os
import simplepbr
from direct.gui.DirectGui import *
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *

#ConfigVariableBool("fullscreen", 0).setValue(1)

load_prc_file("myConfig.prc")

index_character_folder = 1
index_character = 1
index_enviroment = 1

class Demo(ShowBase):
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

                self.loadingText = OnscreenText("DEMO", 2, fg=(1, 1, 1, 1), pos=(0, 0), align=TextNode.ACenter,
                                                scale=.7, mayChange=1)

            for a in range(4):
                self.graphicsEngine.renderFrame()

        else:
            if hasattr(self, 'loadingScreenNode'):
                self.loadingScreenNode.removeNode()
                self.loadingText.removeNode()

                del self.loadingScreenNode
                del self.loadingText

    def __init__(self):
        ShowBase.__init__(self)
        self.loadingscreen(True)

        self.loadModels()
        self.createlight()
        self.cameracontrol()
        self.setskybox()
        self.setfog()
        self.createGUI()

        self.loadingscreen(False)

        simplepbr.init(
            use_normal_maps=True,
            enable_fog=True,
            enable_shadows=True,
            max_lights=2
        )

    def cameracontrol(self):
        self.camLens.set_fov(90)
        self.cam.set_hpr(0, 0, 0)
        self.cam.set_pos(0., -2., 2)

    def loadModels(self):
        global index_character, index_enviroment, index_character_folder

        self.characters = loader.loadModel(f"Assets/Characters/{index_character_folder}/{index_character}.gltf")
        self.characters.reparentTo(render)
        self.characters.setScale(1, 1, 1)
        self.characters.setPos(-2, 3, 0)
        self.characters.setHpr(475, 0, 0)

        self.enviroment = loader.loadModel(f"Assets/Enviroment/{index_enviroment}/scene.gltf")
        self.enviroment.reparentTo(render)

    def createlight(self):
        self.ambient = AmbientLight('ambient')
        self.ambient.setColor(VBase4(0.05, 0.07, 0.05, 1.0))
        self.ambient = render.attachNewNode(self.ambient)
        render.setLight(self.ambient)

        self.point = PointLight('point')
        self.point.setPoint(VBase3(0, 0, 0))

        self.point.setAttenuation(100)
        self.point.setMaxDistance(100)

        self.point.setColor(VBase4(1, 1.5, 1, 0))
        self.point = render.attachNewNode(self.point)
        render.setLight(self.point)

    def setfog(self):
        fog = Fog("fog")
        fog.set_mode(Fog.MExponentialSquared)
        fog.set_color(0.05, 0.06, 0.05)
        fog.set_exp_density(0.09)
        render.set_fog(fog)

    def setskybox(self):
        self.skybox = loader.loadModel("Assets/Enviroment/1/skybox/scene.gltf")
        self.skybox.setScale(2000)
        self.skybox.reparentTo(render)
        self.skybox.setShaderOff()
        self.skybox.setBin('background', 0)
        self.skybox.setDepthWrite(1)
        self.skybox.setLightOff(0)

    def swapcharacter(self, direction=1):
        global index_character

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
        self.characters.setPos(-2, 3, 0)
        self.characters.setHpr(475, 0, 0)

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
        global index_character_folder, index_character

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
        self.characters.setPos(-2, 3, 0)
        self.characters.setHpr(475, 0, 0)


    def createGUI(self):

        image = OnscreenImage(
            parent=self.a2dBottomCenter,
            image='Assets/Hud/3.png',
            pos=(0, 0, 0.4),
            scale=(1, 1, 0.4),
            hpr=(0, 0, 0)
        )

        image.setTransparency(TransparencyAttrib.MAlpha)

        self.typ_postaci_prev = DirectButton(
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            text=("<< TYP POSTACI"),
            text0_font=loader.loadFont('Assets/Hud/Roboto.ttf'),
            scale=0.05,
            command=lambda: self.swapcharacterfolder(-1),
            pos=(-0.5, 0, -0.9)
        )

        self.typ_postaci_next = DirectButton(
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            text=">> TYP POSTACI",
            scale=0.05,
            command=lambda: self.swapcharacterfolder(1),
            pos=(0.5, 0, -0.9)
        )
        self.poprzednia_postac = DirectButton(
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            text="<< POSTAĆ",
            scale=0.05,
            command=lambda: self.swapcharacter(-1),
            pos=(-0.3, 0, -0.9)
        )

        self.kolejna_postac = DirectButton(
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            text=">> POSTAĆ",
            scale=0.05,
            command=lambda: self.swapcharacter(1),
            pos=(0.3, 0, -0.9)
        )

        self.poprzednia_mapa = DirectButton(
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            text="<< MAPA",
            scale=0.05,
            command=lambda: self.swapenviroment(-1),
            pos=(-0.1, 0, -0.8)
        )

        self.kolejna_mapa = DirectButton(
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            text=">> MAPA",
            scale=0.05,
            command=lambda: self.swapenviroment(1),
            pos=(0.1, 0, -0.8)
        )


test = Demo()
test.run()