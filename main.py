import simplepbr

from direct.gui.OnscreenImage import *
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase

from pandac.PandaModules import *

#ConfigVariableBool("fullscreen", 0).setValue(1)

load_prc_file("myConfig.prc")


class Demo(ShowBase):

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
        self.swaptextures()
        self.setskybox()
        self.setfog()
        self.createGUI()

        self.loadingscreen(False)

        properties = WindowProperties()

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

    def createGUI(self):
        image = OnscreenImage(
            parent=base.a2dBottomCenter,
            image='Assets/Hud/3.png',
            pos=(0, 0, 0.4),
            scale=(1, 1, 0.4),
            hpr=(0, 0, 0)
        )
        image.setTransparency(TransparencyAttrib.MAlpha)

    def loadModels(self):
        self.characters = loader.loadModel("Assets/Characters/1/scene.gltf")
        self.characters.reparentTo(render)
        self.characters.setScale(1, 1, 1)
        self.characters.setPos(-2, 3, 0)
        self.characters.setHpr(475, 0, 0)

        # my_actor = Actor("Assets/Characters/1/scene.gltf")
        # anim_names = my_actor.get_anim_names()
        # my_actor.reparentTo(render)
        # my_actor.play(anim_names)

        # my_actor = Actor("Assets/Characters/1/scene.gltf")
        # anim_names = my_actor.get_anim_names()
        # my_actor.reparentTo(render)
        # my_actor.play(anim_names)

        self.enviroment = loader.loadModel("Assets/Enviroment/City/scene.gltf")
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
        self.skybox = loader.loadModel("Assets/Enviroment/City/skybox/scene.gltf")
        self.skybox.setScale(2000)
        self.skybox.reparentTo(render)
        self.skybox.setShaderOff()
        self.skybox.setBin('background', 0)
        self.skybox.setDepthWrite(1)
        self.skybox.setLightOff(0)

    def swaptextures(self):
        ts = TextureStage("1")
        ts.setTexcoordName("0")
        self.characters.setTexture(ts, self.loader.loadTexture("Assets/Characters/1/textures/1.png"))

test = Demo()
test.run()