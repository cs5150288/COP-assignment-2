import random
from Tkinter import *

COUNT = 50
WIDTH = 1600
HEIGHT = 1600
BIRD_SIZE = 4
REPULSION_RAD = 50

def bound_speed(a):
	if(a.velocity.dist() > 600):
		a.velocity /= TwoD(1.5,1.5)

def bound_location(a):
	
	if(a.position.x < 30):
		a.position.x = 30
		a.velocity.x = -a.velocity.x

	elif(a.position.x > 770):
		a.position.x = 770
		a.velocity.x = -a.velocity.x
	
	if(a.position.y < 30):
		a.position.y = 30
		a.velocity.y = - a.velocity.y

	elif(a.position.y > 770):
		a.position.y = 770
		a.velocity.y = - a.velocity.y		


def allmightypush():
	
	for i in boids:
		i.newspeed()

	for i in boids:	
		i.newposition()

class TwoD:

	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)

	def __repr__(self):
		return 'TwoD(%s, %s)' %(self.x, self.y)

	def __add__(self, other):
		return TwoD(self.x + other.x, self.y + other.y)

	def __sub__(self,other):
		return TwoD(self.x - other.x, self.y - other.y)

	def __mul__(self,other):
		return TwoD(self.x * other.x, self.y * other.y)

	def __div__(self,other):
		return TwoD(self.x / other.x, self.y / other.y)

	def dist(self):
		return ((self.x ** 2) + (self.y ** 2)) ** 0.5


class Boid:
	def __init__(self):
		self.velocity = TwoD(random.randint(0,50),random.randint(0,50))
		self.position = TwoD(random.randint(0,400),random.randint(0,400))

	def newspeed(self):
		movement1 = self.centroid()
		movement2 = self.togetherness()
		movement3 = self.withTheCrowd()
		y = TwoD(0,0)
		y = y + (movement1)
		y = y + (movement2)
		y = y + (movement3)
		y /= (TwoD(200,200))
		self.velocity += y
		bound_speed(self)

	def newposition(self):
		self.position += self.velocity/TwoD(50,50)
		bound_location(self)

	def centroid(self):
		accumulator = TwoD(0,0)
		radius_vector = self.position
		for i in boids:
			if i is not self:
				# if((i.position-radius_vector).dist()<75):
				accumulator += (i.position)
		accumulator/=(TwoD(len(boids)-1,len(boids)-1))
		accumulator -= (self.position)
		# Saccumulator /= (TwoD(25,25))
		return accumulator

	def togetherness(self):
		radius_vector = self.position
		repulsion = TwoD(0,0)
		for i in boids:
			if i is not self:
				# if((i.position-radius_vector).dist()<75):
				radnew = i.position
				distance = radius_vector - (radnew)
				u = distance.dist()

				if (u < REPULSION_RAD):
					repulsion += TwoD(15,15)*(distance)
		return repulsion

	def withTheCrowd(self):
		jealousy = TwoD(0,0)
		radius_vector = self.position
		
		for i in boids:
			if i is not self:
			# if((i.position-radius_vector).dist()<75):
				jealousy += i.velocity

		jealousy /= (TwoD(len(boids)-1,len(boids)-1))

		difference = jealousy - (self.velocity)
		difference = difference/(TwoD(5,5))
		return difference

def gen_boids():
	global boids
	boids = tuple (Boid() for i in range(COUNT))

def simulator():
	gen_boids()
	grapher()
	mainloop()

def show():
	graph.delete(ALL)
	for i in boids:
		x1 = i.position.x - BIRD_SIZE
		y1 = i.position.y - BIRD_SIZE
		x2 = i.position.x + BIRD_SIZE
		y2 = i.position.y + BIRD_SIZE

		graph.create_oval((x1,y1,x2,y2), fill='brown')
	graph.update()	


def update():
	show()
	allmightypush()
	graph.after(0, update)


def grapher():	
	global graph
	root = Tk()
	root.overrideredirect(True)
	root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, ((WIDTH)/2-600) , (HEIGHT)/2-800))
	graph = Canvas(root, width=WIDTH, height=HEIGHT, background='lightblue')
	graph.after(10, update)
	graph.pack()


if __name__ == '__main__':
	simulator()