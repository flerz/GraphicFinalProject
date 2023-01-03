#prueba2

import pygame
import random

ANCHO=600
ALTO=400

Verde=[0,255,0]
Rojo=[255,0,0]

class Jugador(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface([30,30])
		self.image.fill(Verde)
		self.rect=self.image.get_rect()
		

	def gravity(self):
		if self.vel_y == 0:
			self.vel_y+=1
		else:
			self.vel_y+=0.5

	def update(self):

		self.gravity()

		if self.vel_x > 0:
			self.rect.x+= self.vel_x

		if self.vel_x < 0:
			self.rect.x+= self.vel_x

		if self.vel_y > 0:
			self.rect.y+= self.vel_y

		if self.vel_y < 0:
			self.rect.y+= self.vel_y

		if self.rect.y >= 300:
			self.vel_y=0
			self.rect.y=300

		if self.rect.left <= 0:
			self.vel_x=0
			self.rect.left=0

		if self.rect.right >= ANCHO:
			self.vel_x=0
			self.rect.right=ANCHO

class Foe(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface([30,30])
		self.image.fill(Rojo)
		self.rect=self.image.get_rect()
		self.vel_x=-2
		self.espera=random.randrange(100)

	def update(self):
		if self.espera > 0:
			self.espera-=1
		else:
			self.rect.x+= self.vel_x

class Bullet(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface([10,10])
		self.image.fill(Rojo)
		self.rect=self.image.get_rect()
		self.vel_x=0
		self.vel_y=0
		self.tipo=0

	def gravity(self):
		if self.vel_y == 0:
			self.vel_y+=1
		else:
			self.vel_y+=0.5

	def update(self):
		if self.tipo !=0:
			self.gravity()
		self.rect.x+= self.vel_x
		self.rect.y+= self.vel_y

		

if __name__ == '__main__':
	pygame.init()
	#Definicion Variables
	pantalla=pygame.display.set_mode([ANCHO,ALTO])
	
	todos = pygame.sprite.Group()
	jugadores = pygame.sprite.Group()
	balas = pygame.sprite.Group()

	r=0
	jugador= Jugador()
	jugador.rect.x=50
	jugadores.add(jugador)
	todos.add(jugador)

	jugador.rect.y=200

	move=False
	up=False
	down=False
	left=False
	right=False
	jugador.vel_y=0
	jugador.vel_x=0

	reloj=pygame.time.Clock()

	ptos=0
	ad=60
	af=120
	ja=100
	mx=100

	fin=False
	while not fin:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				fin=True

		if ad <= 0:
			ad=random.randrange(90, 130)
			jugador.vel_x=0

		if ja <= 0:
			ja=random.randrange(100, 130)

		if mx <= 0:
			mx=random.randrange(100, 130)
			

		if af <= 0:
			af=random.randrange(100,250)
			ad=random.randrange(90, 130)

		ad-=1
		af-=1
		ja-=1
		mx-=1

		if ja == 0:
			jugador.vel_y=-10

		if mx == 0:
			print 'te mueve'
			jugador.vel_x=random.randrange(-5,5)

		if af == 0:
			bala=Bullet()
			bala.rect.center=jugador.rect.center
			bala.vel_y=-20
			bala.vel_x=4
			bala.tipo=1
			balas.add(bala)
			todos.add(bala)	
		elif ad == 0:
			bala=Bullet()
			bala.rect.center=jugador.rect.center
			bala.vel_x=4
			balas.add(bala)
			todos.add(bala)

		todos.update()
		pantalla.fill([0,0,0])
		todos.draw(pantalla)
		pygame.display.flip()
		reloj.tick(60)
