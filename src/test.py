import pyglet
import pyglet.window
import pyglet.graphics

class gps_map:
    red_dots = pyglet.graphics.vertex_list(1,
        ('v2i', (10, 15)),
        ('c3B', (255, 0, 0))
    )
    
    def draw(self):
        self.red_dots.draw(pyglet.gl.GL_POINTS)
    
    def add_red_dot(self, x, y):
        """ Adds a dot to the list of red dots
        """
        size = self.red_dots.get_size()
        size = size + 1

        v2i = list(self.red_dots.vertices)
        c3b = list(self.red_dots.colors)

        v2i.append(x)
        v2i.append(y)
        c3b.append(255)
        c3b.append(0)
        c3b.append(0)

        self.red_dots = pyglet.graphics.vertex_list(size,
            ('v2i', v2i),
            ('c3B', c3b)
        )

window = pyglet.window.Window()
fps_display = pyglet.clock.ClockDisplay()
map = gps_map()

@window.event
def on_draw():
    window.clear()
    fps_display.draw()
    map.draw()
 
@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        map.add_red_dot(x, y)

pyglet.app.run()
