import pyglet
import pyglet.window
import pyglet.graphics
       
window = pyglet.window.Window()
label = pyglet.text.Label('Hello, world', 
                          font_name='Times New Roman', 
                          font_size=12,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

fps_display = pyglet.clock.ClockDisplay()

dots = pyglet.graphics.vertex_list(2,
    ('v2i', (10, 15, 30, 35)),
    ('c3B', (255, 0, 0, 255, 0, 0))
)

def add_dot(x, y):
    size = dots.get_size()
    size = size + 1

    v2i = dots.verticies
    c3b = dots.colors

    v2i.append(x)
    v2i.append(y)
    c3b.append(255)
    c3b.append(0)
    c3b.append(0)

    dots = pyglet.graphics.vertex_list(size,
        ('v2i', v2i),
        ('c3B', c3b)
    )


@window.event
def on_draw():
    window.clear()
    label.draw()
    fps_display.draw()
    dots.draw(pyglet.gl.GL_POINTS)
    #import pdb; pdb.set_trace()

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        add_dot(x, y)
        
        #label.x = x
        #label.y = y


pyglet.app.run()
