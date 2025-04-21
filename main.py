import simplepbr
from direct.showbase.ShowBase import ShowBase


class Demo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.loadModels()

    def loadModels(self):
        simplepbr.init()

        self.characters = loader.loadModel("Assets/Characters/characters.gltf")
        self.characters.reparentTo(render)

        self.enviroment = loader.loadModel("Assets/Enviroment/scene.gltf")
        self.enviroment.reparentTo(render)


test = Demo()
test.run()
