Аркада


1)import arcade


2.1)class ArcadeGame(arcade.Window):
    def __init__(self, *args):
        super().__init__(width, height, title, realizable=True). 
        self.background_color = arcade.color.<цвет, пример: TEA_GREEN>
        self.dots_list = arcade.shape_list.ShapeElementList()

#ShapeElementList() контейнер-список фигур. Использовать в on_draw
#realizable это для масштабирования пользователем
2.2) def setup(self):
==arcade.draw_point(x, y, color, size)== #нарисовать_точку

==arcade.draw_line(x1, y1, x2, y2, цвет, толщина линии)==

==arcade.draw_rect_outline(arcade.rect.XYWH(x_центр, у_центр, высота, ширина), цвет, толщина-контура, угол_поворота)== #прямоугольник_без_заливки

==arcade.draw_rect_filled(arcade.rect.XYWH(x_центр, у_центр, высота, ширина), цвет, толщина-контура, угол_поворота) ==#прямоугольник_с_заливкой

==arcade.draw_circle_outline(center_x, center_y, radius, color, ширина-контура)== #круг_без_заливки

==arcade.draw_circle_filled(center_x, center_y, radius, color)== #круг_с_заливкой

==arcade.draw_ellipse_outline(center_x, center_y, width, height, color, border_width, tilt_angle=0) или ..._filled(...)== #эллипс

==arcade.draw_triangle_outline(x1, y1, x2, y2, x3, y3, color, border_width) и ..._filled(...)== #треугольник

==arcade.draw_polygon_outline(список координатных кортежей, color, border_width) ==#многоугольник



RGBA - появилась прозрачность альфа, в диапазоне от 0 до 255





2.3)def on_draw(self):   #очищение_экрана 
           self.clear()
self.dots_list.draw() 

2.4) def on_update(self, delta_time: float): 
delta_time - время прошедшее с последнего вызова


3) def main():
    game = MyFirstArcadeGame(высота, ширина, имя)
    game.setup()
    arcade.run()

if name == "__main__":
    main()