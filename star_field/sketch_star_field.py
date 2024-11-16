from typing import List, NamedTuple
import vsketch
from shapely.geometry import box
import random


class Star(NamedTuple):
    x: int
    y: int
    radius: int

class StarFieldParams(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_radius: int
    max_radius: int
    num_stars: int
    star_gap: int

def draw_bezier(vsk, a1, c1, c2, a2, render_control: bool = False):
    vsk.bezier(a1[0], a1[1], c1[0], c1[1], c2[0], c2[1], a2[0], a2[1])
    if render_control:
        vsk.stroke(2)
        vsk.square(a1[0], a1[1], 5, mode="center")
        vsk.square(a2[0], a2[1], 5, mode="center")
        vsk.line(a1[0], a1[1], c1[0], c1[1])
        vsk.line(a2[0], a2[1], c2[0], c2[1])
        vsk.circle(c1[0], c1[1], 5)
        vsk.circle(c2[0], c2[1], 5)
        vsk.stroke(1)


def draw_star(vsk, size, curve_scale=1):
    for _ in range(4):
        # anchor points
        a1 = (size, 0)
        a2 = (0, size)

        # control points
        curve = 0.05 * curve_scale
        x2 = y2 = x3 = y3 = size * curve

        draw_bezier(vsk, a1, (x2, y2), (x3, y3), a2, render_control=False)
        vsk.rotate(90, degrees=True)


def draw_double_star(vsk, size):
    draw_star(vsk, size)
    # offset the next star by 45 degrees
    vsk.rotate(45, degrees=True)
    draw_star(vsk, size*0.6, 0.01)
    # shift back
    vsk.rotate(315, degrees=True)

def get_star_radius(vsk, params: StarFieldParams) -> int:
        # bias towards smaller stars
        if vsk.random(10) < 7:
            return vsk.random(params.min_radius, params.max_radius/2)
        return vsk.random(params.min_radius, params.max_radius)

def generate_star_centerpoint_grid(vsk, params: StarFieldParams) -> List[Star]:
    stars = []
    stars_personal_space = []
    #vsk.rectMode("center")

    for _ in range(params.num_stars):
        star_redo_fuel = 100
        while(star_redo_fuel > 0):
            print(f"star redo fuel: {star_redo_fuel}")
            x = vsk.random(params.min_x, params.max_x)
            y = vsk.random(params.min_y, params.max_y)
            radius = get_star_radius(vsk, params)
            star = Star(x, y, radius)
            # draw a bounding box & check for intersection
            star_box = box(x-radius, y-radius, x+radius, y+radius)
            #print(f'star box was: {star_box}')
            intersects_none = True
            for existing_star_box in stars_personal_space:
                if existing_star_box.intersects(star_box):
                    intersects_none = False
                    break
                #print(f'checking existing star box: {existing_star_box}')
            if intersects_none: # we found a star worth keeping, yay!
                #print('found non-intersecting star')
                star_redo_fuel = 0
            # otherwise we'll try again
            star_redo_fuel -= 1

        #vsk.rect(x, y, radius, radius)
        stars_personal_space.append(star_box)
        stars.append(star)
    


    return stars    


def plot_stars(vsk, stars: List[Star], params: StarFieldParams):
    for star in stars:
        vsk.translate(star.x, star.y)
        # maybe draw a double star
        star_is_big_enough = star.radius > (params.max_radius + params.min_radius) // 2
        die_roll = random.random() < 0.3
        #draw_double_star(vsk, star.radius)
        if star_is_big_enough and die_roll:
            draw_double_star(vsk, star.radius)
        elif star.radius < params.min_radius + 4:
            vsk.circle(0, 0, star.radius+2)
        elif random.random() < 0.9:
            draw_star(vsk, params.min_radius + star.radius // 3)
        else:
            draw_star(vsk, star.radius)
        # move back (so that all x, y's are interpretted in absolute terms)
        vsk.translate(-star.x, -star.y)

 
class StarfieldSketch(vsketch.SketchClass):
    paper_size_x = vsketch.Param(15)
    paper_size_y = vsketch.Param(11)
    min_x = vsketch.Param(0, step=20)
    max_x = vsketch.Param(400, step=20)
    min_y = vsketch.Param(0, step=20)
    max_y = vsketch.Param(400, step=20)
    min_radius = vsketch.Param(5)
    max_radius = vsketch.Param(25)
    num_stars = vsketch.Param(25, step=5)
    star_gap = vsketch.Param(20, step=2)


    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size(f"{self.paper_size_x}in", f"{self.paper_size_y}in")
        param1 = StarFieldParams(min_x = self.min_x,
                                max_x = self.max_x,
                                min_y = self.min_y,
                                max_y = self.max_y,
                                min_radius = self.min_radius,
                                max_radius = self.max_radius,
                                num_stars = self.num_stars,
                                star_gap = self.star_gap)
        # param2 = StarFieldParams(min_x = 0,
        #                 max_x = 900,
        #                 min_y = 300,
        #                 max_y = 900,
        #                 min_radius = 10,
        #                 max_radius = 45,
        #                 num_stars = 20,
        #                 star_gap = 10)

        plot_stars(vsk, generate_star_centerpoint_grid(vsk, param1), param1)
        # plot_stars(vsk, generate_star_centerpoint_grid(vsk, param2))
        # generate_star_centerpoint_grid(vsk, param1)
        

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linesimplify linesort")


if __name__ == "__main__":
    StarfieldSketch.display()
