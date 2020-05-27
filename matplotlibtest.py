from random import choice

class RandomWalk():

    def __init__(self,point_num=5000):
        self.point_num = point_num

        self.x_values = [0]
        self.y_values = [0]




    def fill_walk(self):
        while len(self.x_values) < self.point_num:
            self.x_direction = choice([1, -1])  # 选择x水平方向的正反
            self.x_distance = choice([0, 1, 2, 3, 4])  # 选择移动的距离
            self.x_step = self.x_direction * self.x_distance  # 计算出x轴水平方向的矢量

            self.y_direction = choice([1, -1])
            self.y_distance = choice([0, 1, 2, 3, 4])
            self.y_step = self.y_direction * self.y_distance

            if self.x_step==0 and self.y_step==0:
                continue

            self.x_position = self.x_values[-1] + self.x_step
            self.y_position = self.y_values[-1] + self.y_step

            self.x_values.append(self.x_position)
            self.y_values.append(self.y_position)

