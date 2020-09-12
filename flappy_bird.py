import pygame
import random
import math
import time

pygame.init()

clock=pygame.time.Clock()

width=600
height=600
jump_speed=0.1
jump=False
start=False
score=0
display=pygame.display.set_mode((width,height))

bg_image=pygame.image.load('background.png').convert_alpha()
bird_image=pygame.image.load('bird.png').convert_alpha()
upper_pipe=pygame.image.load('upper_pipe.png').convert_alpha()
lower_pipe=pygame.image.load('lower_pipe.png').convert_alpha()

font=pygame.font.Font('freesansbold.ttf',32)
text=font.render('GAME OVER',True,(0,0,0),(255,255,255))

textRect=text.get_rect()
textRect.center=(width//2,height//2)


pathway=175
bg_color=(0,0,255)
gravity_angle=math.pi
gravity_magnitude=0
rectangle_speed=0.3
temp=350
collision_detection=False

class Bird:
	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.size=18
		self.color=(255,255,0)
		self.speed=0
		self.angle=0
		self.mass=1



	def move(self):
		(self.angle,self.speed)=addvectors(self.angle,self.speed,gravity_angle,gravity_magnitude)
		self.y-=math.cos(self.angle)*self.speed
		if self.y<20:
			self.y=20

		if self.y>580:
			self.y=580
			self.speed=0
			self.angle=0

	def display(self):
		if self.angle<math.pi/4:
			a=pygame.transform.rotate(bird_image,40)
		elif self.angle==1.5707963267948966:
			a=pygame.transform.rotate(bird_image,0)
		else:
			a=pygame.transform.rotate(bird_image,-40)
		display.blit(a,(self.x-20,self.y-20))


def jump():
	new_bird.angle=0
	new_bird.speed=0.5
	jumping=False
					
def addvectors(angle1,vector1,angle2,vector2):
	x_coordinate=math.sin(angle1)*vector1+math.sin(angle2)*vector2
	y_coordinate=math.cos(angle1)*vector1+math.cos(angle2)*vector2

	length=math.hypot(x_coordinate,y_coordinate)

	angle=0.5*math.pi-math.atan2(y_coordinate,x_coordinate)
	
	return(angle,length)

class Rectangle:
	def __init__(self,rx,rh):
		self.x=rx
		self.y=0
		self.width=50
		self.height=rh
		self.color=(0,255,0)
		self.x_change=rectangle_speed


	def display(self):
		display.blit(upper_pipe,(self.x,self.height-width))
		display.blit(lower_pipe,(self.x,self.height+pathway))

	def move(self):
		self.x-=self.x_change
		if self.x<-50:

			self.x=600
			self.height=random.randint(100,400)

def collision(tempr,tempb):
	if tempr.x<=tempb.x+tempb.size and tempr.x>tempb.x-tempb.size:
		if tempb.y<tempr.height or tempb.y>tempr.height+pathway:
			return True

	if tempr.x+tempr.width<=tempb.x+tempb.size and tempr.x+tempr.width>tempb.x-tempb.size:
		if tempb.y<tempr.height or tempb.y>tempr.height+pathway:
			return True

	if tempr.x<=tempb.x and tempr.x>tempb.x-tempb.size:
		if tempb.y+tempb.size>tempr.height+pathway or tempb.y-tempb.size<tempr.height:
			return True

	if tempr.x+50<=tempb.x + tempb.size and tempr.x + 50 > tempb.x:
		if tempb.y+tempb.size>tempr.height+pathway or tempb.y-tempb.size<tempr.height:
			return True



		

my_rectangles=[]
for i in range(2):
	x=600+i*temp
	h=random.randint(100,400)
	my_rectangles.append(Rectangle(x,h))






new_bird=Bird(40,300)
jumping=False

loop=True

while loop:
	display.blit(bg_image,(0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			loop= False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				jumping=True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				jumping=False

	if jumping:
		if collision_detection==False:
			jump()
	new_bird.move()
	keys=pygame.key.get_pressed()
	if keys[pygame.K_SPACE]:
		start=True
		gravity_magnitude=0.003
	if start:
		for rect in my_rectangles:
			if collision(rect,new_bird):
				collision_detection=True

		for rect in my_rectangles:
			rect.move()
			rect.display()

		if collision_detection:
			new_bird.speed=0
			gravity_magnitude=0
			my_rectangles[0].x_change=0
			my_rectangles[1].x_change=0
			display.blit(text,textRect)



	new_bird.display()
           
	pygame.display.update()
			