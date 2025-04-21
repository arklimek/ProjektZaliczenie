from direct.showbase.ShowBase import ShowBase
from panda3d.core import PointLight  # Import klasy PointLight


class Demo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.loadModels()

    def loadModels(self):
        self.characters = loader.loadModel("Assets/Characters/characters.gltf")
        self.characters.reparentTo(render)

        self.enviroment = loader.loadModel("Assets/Enviroment/scene.gltf")
        self.enviroment.reparentTo(render)

        point_light = PointLight("point_light")
        point_light.setColor((1000, 1000, 1000, 1))  # Intensywność i kolor (biały)
        point_light.setAttenuation((0, 0, 1))  # Tłumienie kwadratowe dla PBR

        # Umieszczenie światła w scenie
        light_np = render.attachNewNode(point_light)
        light_np.setPos(0, 0, 0)  # Pozycja (0, 0, 0)


test = Demo()
test.run()