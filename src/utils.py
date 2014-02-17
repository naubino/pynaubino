import random, pymunk
from pymunk import Vec2d



from collections import namedtuple
ColorRGB1   = namedtuple("ColorRGB1", "r g b")
ColorRGB255 = namedtuple("ColorRGB255", "r g b")

def color_rgb255(color):
    if isinstance(color, ColorRGB255):
        return color
    if isinstance(color, ColorRGB1):
        return ColorRGB255(*[int(x * 255) for x in color])
    raise TypeError("must be a Color* type, not "+str(type(color)))

def color_rgb1(color):
    if isinstance(color, ColorRGB1):
        return color
    if isinstance(color, ColorRGB255):
        return ColorRGB255(*[x / 255.0 for x in color])
    raise TypeError("must be a Color* type, not "+str(type(color)))

def color_hex(color):
    return ("{:02x}"*3).format(*color_rgb255(color))

def random_vec(x, y):
    return Vec2d(
        random.uniform(-x, x),
        random.uniform(-y, y))

def are_colors_alike(a, b):
    a, b = [color_rgb1(x) for x in [a,b]]
    return all([(max(a[i], b[i]) - min(a[i], b[i])) < 0.25
        for i in xrange(3)])

def random_byte():
    return random.randint(0, 255)

def random_not_white():
    r = random.uniform(0, 1)
    white = ColorRGB1(1, 1, 1)
    while True:
        color = ColorRGB1(r(), r(), r())
        if not are_colors_alike(color, white):
            return color

def toVec2d(v):
    if isinstance(v, Vec2d): return v
    else: return Vec2d(v.x(), v.y())

class Pos(object):
    @property
    def pos(self): return self.get_pos()
    @pos.setter
    def pos(self, pos): self.set_pos(pos)

    def __init__(self, x):
        from PyQt4.QtGui import QGraphicsItem
        if   isinstance(x, pymunk.Body):
            self.get_pos = lambda: x.position
            self.set_pos = lambda pos: setattr(x, u"position", pos)
        elif isinstance(x, QGraphicsItem):
            def get_pos():
                pos = x.pos()
                return Vec2d(pos.x(), pos.y())
            self.get_pos = get_pos
            def set_pos(pos):
                x.setPos(pos.x, pos.y)
            self.set_pos = set_pos
        else:
            raise TypeError(type(x))



class SaveParent(object):

    def __init__(self, *nodes):
        self.nodes = list(nodes)

    def __enter__(self):
        self.nodes = list(self.__save())
        for node, _, _ in self.nodes:
            node.unlink()

    def __save(self):
        for node in self.nodes:
            parent = node.parent
            if parent:
                index = parent.indexOf(node)
                yield (node, parent, index)
            else:
                yield (node, None, None)

    def __exit__(self, ex_type, ex_value, traceback):
        for node, parent, index in sorted(self.nodes, key = lambda x: x[2]):
            if node.parent:
                node.unlink()
            if parent:
                parent.insertChild(node, index)



import libavg as avg
def screenshot(node):
    if isinstance(node, avg.ImageNode):
        return avg.Bitmap(node.getBitmap())
    with SaveParent(node):
        return drawOffscreen(node.size, lambda parent:
            parent.appendChild(node))

def screenshotImageNode(node):
    img = avg.ImageNode()
    img.setBitmap(screenshot(node))
    return img

def drawOffscreen(size, what, unlink=True):
    canvas = avg.player.createCanvas(
        # XXX buggy on some platforms https://www.libavg.de/site/issues/467
        #mipmap = True,
        multisamplesamples = 8,
        autorender  = False,
        size        = size)
    root = canvas.getRootNode()
    what(root)
    canvas.render()
    bitmap = canvas.screenshot()
    while unlink and root.getNumChildren():
        root.removeChild(0)
    avg.player.deleteCanvas(canvas.getID())
    return bitmap
