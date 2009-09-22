import pyglet.window
import pyglet.image


class IsoRenderer(object):
    """ Renders a 3D view of a map
    """
    cam_rx, cam_ry, cam_rz = 45, 0, 0
    cam_x, cam_y, cam_z = 0, 0, -1000
    w, h = 640, 480
    far = 10000
    fov = 60

    def __init__(self):
        self.load_map()
        self.create_window()
        self.setup_gl_params()

    def create_window(self):
        self.window = pyglet.window.Window(fullscreen=False, resizable=True)
        self.window.width=1280
        self.window.height=800
        self.window.on_resize=self.resize_view

    def setup_gl_params(self):
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        pyglet.gl.glDepthFunc(pyglet.gl.GL_LEQUAL)
        pyglet.gl.glEnable(pyglet.gl.GL_LINE_SMOOTH)
        pyglet.gl.glHint(pyglet.gl.GL_LINE_SMOOTH_HINT, pyglet.gl.GL_DONT_CARE)

    def load_map(self):
        """ takes a PIL image.
        """
        map_img = pyglet.image.load('img.gif')
        self.map_tex = map_img.get_texture()

    def draw_map(self):
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(-512, 0, 512)
        pyglet.gl.glRotatef(-90, 1.0, 0.0, 0.0)
        self.map_tex.blit(0, 0, 0, 1024, 1024)
        pyglet.gl.glPopMatrix()
        pyglet.gl.glColor4f(1.0, 0.0, 0.0, 1)
        pyglet.gl.glLineWidth(1.5);
        pyglet.gl.glBegin(pyglet.gl.GL_LINE_LOOP)
        pyglet.gl.glVertex3f(512, 0, 512)
        pyglet.gl.glVertex3f(-512, 0, 512)
        pyglet.gl.glVertex3f(-512, 0, -512)
        pyglet.gl.glVertex3f(512, 0, -512)
        pyglet.gl.glEnd()
        pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1)

    def render(self):
        self.window.dispatch_events()
        pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT | pyglet.gl.GL_DEPTH_BUFFER_BIT)
        self.apply_camera()
        self.draw_map()
        self.window.flip()

    def apply_camera(self):
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glTranslatef(self.cam_x, self.cam_y, self.cam_z)
        pyglet.gl.glRotatef(self.cam_rx,1,0,0)
        pyglet.gl.glRotatef(self.cam_ry,0,1,0)
        pyglet.gl.glRotatef(self.cam_rz,0,0,1)


    def resize_view(self, width, height):
        self.w,self.h=width,height
        pyglet.gl.glViewport(0, 0, width, height)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.gluPerspective(self.fov, float(self.w)/self.h, 0.1, self.far)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)