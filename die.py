# from random import randint
#
# class Die():
#
#     def __init__(self,sides_num=6):
#         self.sides_num = sides_num
#
#
#     def roll(self):
#         return randint(1,self.sides_num)

class Ball():
        color = 'black'
        size = 'middle'
        volumn = 50
        weight = 15



soccer_ball = Ball()
soccer_ball.color = 'red'
soccer_ball.size = 'large'
soccer_ball.volumn = 500
soccer_ball.weight = 140
print(soccer_ball.__dict__)
