#!/usr/bin/env python
import sys

from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from panda3d.core import loadPrcFileData, WindowProperties, AmbientLight, PointLight, TextNode, \
    LPoint3, LVector3


def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft)


def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1, 1, 1, 1), scale=.08,
                        parent=base.a2dBottomRight, align=TextNode.ARight,
                        pos=(-0.1, 0.09), shadow=(0, 0, 0, 1))


class BumpMapDemo(ShowBase):
    def __init__(self):
        loadPrcFileData("", "parallax-mapping-samples 3\nparallax-mapping-scale 0.1")
        ShowBase.__init__(self)

        if not self.win.getGsg().getSupportsBasicShaders():
            addTitle("Bump Mapping: Video driver does not support shaders.")
            return

        # Instructions
        self.title = addTitle("Panda3D: Tutorial - Bump Mapping")
        self.inst1 = addInstructions(0.06, "Press ESC to exit")
        self.inst2 = addInstructions(0.12, "Move mouse to rotate camera")
        self.inst3 = addInstructions(0.18, "W: Move forwards")
        self.inst4 = addInstructions(0.24, "S: Move backwards")
        self.inst5 = addInstructions(0.30, "A: Move left")
        self.inst6 = addInstructions(0.36, "D: Move right")
        self.inst7 = addInstructions(0.42, "Enter: Turn bump maps Off")

        # Load the room model
        self.room = loader.loadModel("models/abstractroom")
        self.room.reparentTo(render)

        # Mouse and camera setup
        self.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        self.win.requestProperties(props)
        self.camLens.setFov(110)

        # Camera focus and movement state
        self.focus = LVector3(55, -55, 20)
        self.heading = 180
        self.pitch = 0
        self.last = 0
        self.movement = {'forward': False, 'backward': False, 'left': False, 'right': False}

        # Task and key bindings
        taskMgr.add(self.controlCamera, "camera-task")
        self.accept("escape", sys.exit)
        self.accept("enter", self.toggleShader)
        self.accept("j", self.rotateLight, [-1])
        self.accept("k", self.rotateLight, [1])
        self.accept("arrow_left", self.rotateCam, [-1])
        self.accept("arrow_right", self.rotateCam, [1])

        # Movement keys
        self.accept("w", self.setMovement, ['forward', True])
        self.accept("w-up", self.setMovement, ['forward', False])
        self.accept("s", self.setMovement, ['backward', True])
        self.accept("s-up", self.setMovement, ['backward', False])
        self.accept("a", self.setMovement, ['left', True])
        self.accept("a-up", self.setMovement, ['left', False])
        self.accept("d", self.setMovement, ['right', True])
        self.accept("d-up", self.setMovement, ['right', False])

        # Lighting setup
        self.lightpivot = render.attachNewNode("lightpivot")
        self.lightpivot.setPos(0, 0, 25)
        self.lightpivot.hprInterval(10, LPoint3(360, 0, 0)).loop()
        plight = PointLight('plight')
        plight.setColor((1, 1, 1, 1))
        plight.setAttenuation(LVector3(0.7, 0.05, 0))
        plnp = self.lightpivot.attachNewNode(plight)
        plnp.setPos(45, 0, 0)
        self.room.setLight(plnp)

        alight = AmbientLight('alight')
        alight.setColor((0.2, 0.2, 0.2, 1))
        alnp = render.attachNewNode(alight)
        self.room.setLight(alnp)

        sphere = loader.loadModel("models/icosphere")
        sphere.reparentTo(plnp)
        self.room.setShaderAuto()
        self.shaderenable = 1

    def setMovement(self, direction, value):
        self.movement[direction] = value

    def rotateLight(self, offset):
        self.lightpivot.setH(self.lightpivot.getH() + offset * 20)

    def rotateCam(self, offset):
        self.heading -= offset * 10

    def toggleShader(self):
        self.inst7.destroy()
        if self.shaderenable:
            self.inst7 = addInstructions(0.42, "Enter: Turn bump maps On")
            self.shaderenable = 0
            self.room.setShaderOff()
        else:
            self.inst7 = addInstructions(0.42, "Enter: Turn bump maps Off")
            self.shaderenable = 1
            self.room.setShaderAuto()

    def controlCamera(self, task):
        md = self.win.getPointer(0)
        x, y = md.getX(), md.getY()
        if self.win.movePointer(0, 100, 100):
            self.heading -= (x - 100) * 0.2
            self.pitch -= (y - 100) * 0.2
        self.pitch = max(min(self.pitch, 45), -45)
        self.camera.setHpr(self.heading, self.pitch, 0)

        elapsed = task.time - self.last if self.last != 0 else 0
        dir = self.camera.getMat().getRow3(1)
        right = self.camera.getMat().getRow3(0)
        move = LVector3(0, 0, 0)

        if self.movement['forward']: move += dir
        if self.movement['backward']: move -= dir
        if self.movement['left']: move -= right
        if self.movement['right']: move += right

        if move.length() > 0:
            move.normalize()
            self.focus += move * elapsed * 30

        self.camera.setPos(self.focus - dir * 5)
        self.focus.set(
            max(min(self.focus.x, 59), -59),
            max(min(self.focus.y, 59), -59),
            max(min(self.focus.z, 45), 5)
        )
        self.last = task.time
        return Task.cont


demo = BumpMapDemo()
demo.run()