import simplepbr
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, PointLight, VBase4, VBase3

class Demo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.loadModels()
        self.createlight()
        self.cameracontrol()
        self.setskybox()
        simplepbr.init()

    def cameracontrol(self):
        self.camLens.set_fov(90)
        self.cam.set_hpr(0, 0, 0)
        self.cam.set_pos(0., -2., 2)

    def loadModels(self):
        self.characters = loader.loadModel("Assets/Characters/scene.gltf")
        self.characters.setScale(1, 1, 1)
        self.characters.reparentTo(render)

        self.enviroment = loader.loadModel("Assets/Enviroment/City/scene.gltf")
        self.enviroment.reparentTo(render)

    def createlight(self):
        self.ambient = AmbientLight('ambient')
        self.ambient.setColor(VBase4(0.05, 0.07, 0.05, 1.0))
        self.ambient = render.attachNewNode(self.ambient)
        render.setLight(self.ambient)

        self.point = PointLight('point')
        self.point.setPoint(VBase3(0, 0, 0))

        self.point.setAttenuation(10)
        self.point.setMaxDistance(10)

        self.point.setColor(VBase4(1, 1.5, 1, 0))
        self.point = render.attachNewNode(self.point)
        render.setLight(self.point)

    def setskybox(self):
        self.skybox = loader.loadModel("Assets/Enviroment/City/skybox/scene.gltf")
        self.skybox.setScale(2000)
        self.skybox.reparentTo(render)
        self.skybox.setShaderOff()
        self.skybox.setBin('background', 0)
        self.skybox.setDepthWrite(0)
        self.skybox.setLightOff()
test = Demo()
test.run()