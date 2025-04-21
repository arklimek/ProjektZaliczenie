import simplepbr
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, GeoMipTerrain, PointLight, TextureStage, VBase4


class MyApp(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)
    simplepbr.init()  # commenting this out to disable

    terrain = GeoMipTerrain('terrain')
    terrain.setHeightfield('heightmap.png')
    root = terrain.getRoot()
    root.setScale(10, 10, 10)
    root.setPos(-100, 0, -10)
    root.setTexScale(TextureStage.getDefault(), 16)
    root.setTexture(loader.loadTexture('grass.jpg'))
    root.reparentTo(render)
    terrain.update()

    model = loader.loadModel('lion.gltf')
    model.setScale(0.5, 0.5, 0.5)
    model.setPos(0, 5, -1)
    model.reparentTo(render)

    alight = AmbientLight('alight')
    alight.setColor(VBase4(0.3, 0.3, 0.3, 1.0))
    alnp = render.attachNewNode(alight)
    render.setLight(alnp)

    plight = PointLight('plight')
    plnp = render.attachNewNode(plight)
    render.setLight(plnp)


app = MyApp()
app.run()
