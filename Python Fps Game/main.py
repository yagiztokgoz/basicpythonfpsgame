from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
sky_texture = load_texture('assets/skybox.png')
punch_sound = Audio('assets/shoot', loop=False, autoplay=False)
walking_sound = Audio("assets/walking", loop=False, autoplay=False)

window.borderless = False
window.fps_counter.enabled = True
window.exit_button.visible = True
window.title = "battlefield 2042"

ground = Entity(model='cube', scale=(100, 1, 100), color=color.green.tint(-.4), texture="white_cube",
                texture_scale=(100, 100), collider='box', position=(0, -2, 0), grounded=True)
ammo = 30
player = FirstPersonController()
player.gun = None

gun = Button(parent=scene, model='assets/arm', color=color.black, origin_y=-.5, position=(3, 0, 3), collider='box')
gun.on_click = Sequence(Func(setattr, gun, 'parent', camera), Func(setattr, player, 'gun', gun))


def input(key):
    global ammo
    walking_sound.volume = 1
    if (held_keys["w"] or held_keys["s"] or held_keys["s"] or held_keys["a"]) and not held_keys["right mouse"]:
        walking_sound.play()
    else:
        walking_sound.volume = 0
    if key == 'left mouse down' and gun.parent != scene:
        ammo -= 1
        punch_sound.play()
        gun.blink(color.red)
        bullet = Entity(parent=gun, model='sphere', scale=.5, color=color.black)
        bullet.world_parent = scene
        bullet.animate_position(bullet.position + (bullet.forward * 1000), duration=0.2)
        Text(text=f"Ammo: {ammo}", position=(-0.65, 0.4), origin=(0, 0), scale=2, color=color.red,
             background=True)

        destroy(bullet, delay=5)

    if held_keys["right mouse"]:
        gun.position = (1.7, -1, 3)
        player.speed = 2
    else:
        player.speed = 9
        gun.position = Vec2(1, -2)

    if held_keys["g"]:
        gun.parent = scene
        gun.position = player.position


class Sky(Entity):
    def __init__(self):
        super().__init__(parent=scene, model='sphere', texture=sky_texture, scale=150, double_sided=True)


text = Text(text=' ')
sky = Sky()
app.run()
