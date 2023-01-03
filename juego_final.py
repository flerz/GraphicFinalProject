#import de librerias
import pygame
import random
import json

#dimensiones de pantalla
ANCHO = 700
ALTO = 425

#definicion de colores
Negro = [0,0,0]
Verde = [0,255,0]
Rojo = [255,0,0]
Amarillo = [0,255,35]
Blanco = [255,255,255]
Azul = [0,0,255]






#Recorte sabana de sprites
def Recortar(nf,nc,archivo,limites):
	imagen=pygame.image.load(archivo)
	info=imagen.get_rect()
	an_img=info[2]
	al_img=info[3]
	an_corte=int(an_img/nc)
	al_corte=int(al_img/nf)
	m=[]

	for y in range(nf):
		fila=[]
		
		for x in range(limites[y]):
			cuadro=imagen.subsurface(x*an_corte,y*al_corte, an_corte,al_corte)
			fila.append(cuadro)
		m.append(fila)
		

	return m

#Recortar mapa
def Recortarmap(nf,nc,archivo):
	imagen=pygame.image.load(archivo)
	info=imagen.get_rect()
	an_img=info[2]
	al_img=info[3]
	an_corte=int(an_img/nc)
	al_corte=int(al_img/nf)
	m=[]

	for y in range(nf):
		fila=[]
		
		for x in range(nc):
			cuadro=imagen.subsurface(x*an_corte,y*al_corte, an_corte,al_corte)
			fila.append(cuadro)
		m.append(fila)
		

	return m

#Cargar el archivo .json
def cargar(ruta):
	with open(ruta) as json_file:
			base = json.load(json_file)
	return base

#Cargar las plataformas del nivel
def cargar_pl(ruta,todos,plataformas):
	base=cargar(ruta)
	j=0
	i=0

	for b in base ['layers'][0]['data']:
		px= int(b/73)
		py= int((b%73)-1)
		if b != 0:
			plata=Plataforma([(j*anc[2]),(i*anc[3])],nivel[px][py])
			plataformas.add(plata)
			todos.add(plata)
		#print 'row',px,' col', py
		j+=1

		if(j >= base['layers'][0]['width']):
			i+=1
			j=0	

	return (base['layers'][0]['width'] - 48) * 17



#Clase jugador
class Jugador(pygame.sprite.Sprite):
	def __init__(self,m):
		pygame.sprite.Sprite.__init__(self)
		self.action=1
		self.i=0
		self.m = m
		self.image=self.m[self.action][self.i]		
		self.rect=self.image.get_rect()
		self.vel_x=0
		self.vel_y=0
		self.pls=None
		self.sl=0
		self.health=100
		self.shield=2
		self.mf=False
		self.pra=self.action
		#self.sonido1=pygame.mixer.Sound('Damn_It.ogg')
		#self.sonido2=pygame.mixer.Sound('Ouch.ogg')

	def update(self):
		
		self.image=self.m[self.action][self.i]


		if (self.action == 2 and self.i == 2) or (self.action == 7 and self.i == 2):
			if self.vel_x != 0 or self.mf:
				self.action=0
				self.i=0

			if self.vel_x == 0 and (not self.mf):
				if self.action >4:
					self.action=6
				else:
					self.action=1
		
		if self.vel_y == 0:
			self.vel_y=1
		elif self.vel_y < 0:
			self.i = 0
			if self.action < 5:
				self.action = 2
			elif self.action > 4:
				self.action = 7
			self.vel_y+=0.5
		elif self.vel_y > 0:
			self.i = 1
			if self.action < 5:
				self.action = 2
			elif self.action > 4:
				self.action = 7
			self.vel_y+=0.5

		else:
			self.vel_y+=0.5

		self.rect.x+= self.vel_x
		self.rect.y+= self.vel_y


		if (self.action == 2 and self.i == 1 and (self.vel_y == 0 or self.vel_y == 1)) or (self.action == 7 and self.i == 1 and (self.vel_y == 0 or self.vel_y == 1)):
			self.i+=1
			self.image=self.m[self.action][self.i]
			

		if self.action != 2 and self.action != 3 and self.action != 7 and self.action != 8:
			self.i+=1
		if self.i >= len(self.m[self.action]):
				self.i=0
				if self.action == 4 or self.action==9:
					self.action=self.pra
					
						

		

		col=pygame.sprite.spritecollide(self,self.pls,False)
		for p in col:
			'''if(self.vel_y<=0) and (self.rect.top <= p.rect.bottom):
				self.rect.top=p.rect.bottom
				self.vel_y=0'''

			if(self.vel_y>0) and (self.rect.bottom >= p.rect.top):
				self.rect.bottom=p.rect.top
				self.vel_y=0
				self.sl = 0
				if (self.action == 2 and (self.i == 0 or self.i == 1)) or (self.action == 7 and (self.i == 0 or self.i == 1)):
					self.i=2


		'''col=pygame.sprite.spritecollide(self,self.pls,False)
		for p in col:
			if(self.vel_x<=0) and (self.rect.left <= p.rect.right):
				self.rect.left=p.rect.right
				self.vel_x=0

			if(self.vel_x>0) and (self.rect.right >= p.rect.left):
				self.rect.right=p.rect.left
				self.vel_x=0'''

		

		
#		if self.action == 1:



#Enemigos
class Foe(pygame.sprite.Sprite):
	def __init__(self,pos,m):
		pygame.sprite.Sprite.__init__(self)
		self.m = m
		self.action = 0
		self.i = 0
		self.image= self.m[self.action][self.i]
		self.rect=self.image.get_rect()
		self.vel_x=0
		self.vel_y=0
		self.rect.x=pos[0]
		self.rect.y=pos[1]
		self.salud=0
		self.pls=None
		self.tipo=''
		self.health=0

	def gravity(self):
		if self.vel_y == 0:
			self.vel_y+=1
		else:
			self.vel_y+=0.5

	def update(self):
		self.image = self.m[self.action][self.i]
		if self.tipo != 'a':
			self.gravity()
			self.i+=1

			if self.i >= len(self.m[self.action]):
				self.i=0

			col=pygame.sprite.spritecollide(self,self.pls,False)
			for p in col:
				'''if(self.vel_y<=0) and (self.rect.top <= p.rect.bottom):
					self.rect.top=p.rect.bottom
					self.vel_y=0'''

				if(self.vel_y>0) and (self.rect.bottom >= p.rect.top):
					self.rect.bottom=p.rect.top
					self.vel_y=0
					self.sl = 0

		self.rect.x += self.vel_x
		self.rect.y += self.vel_y

#Jefes
class Jefe(pygame.sprite.Sprite):
	def __init__(self, pos,m):
		pygame.sprite.Sprite.__init__(self)
		self.m=m
		self.action=0
		self.i=0
		self.image=self.m[self.action][self.i]
		self.rect=self.image.get_rect()
		self.rect.x=pos[0]
		self.rect.y=pos[1]
		self.vel_x=0
		self.vel_y=0
		self.tipo='b'
		self.l=0
		self.pls=None
		self.health=200
		

	def gravity(self):
		if self.vel_y == 0:
			self.vel_y+=1
		else:
			self.vel_y+=0.5

	def update(self):
		self.image=self.m[self.action][self.i]
		
		self.gravity()

		if self.l == 2 and (self.action == 1 or self.action == 6):
			if self.vel_y < 0:
				self.i=1

			elif self.vel_y >= 0:
				self.i=2

		if (self.action != 1 and self.action != 6 and self.vel_x != 0) or self.l != 2:
			self.i+=1
		
		if self.i >= len(self.m[self.action]):
				self.i=0

		self.rect.x+= self.vel_x
		self.rect.y+= self.vel_y

		col=pygame.sprite.spritecollide(self,self.pls,False)
		for p in col:
			'''if(self.vel_y<=0) and (self.rect.top <= p.rect.bottom):
				self.rect.top=p.rect.bottom
				self.vel_y=0'''

			if(self.vel_y>0) and (self.rect.bottom >= p.rect.top):
				self.rect.bottom=p.rect.top
				self.vel_y=0
				self.sl = 0
				if self.action==1 or self.action==6:
					self.action-=1
					self.i=0


		if self.rect.left <= 0:
			self.vel_x=0
			self.rect.left=0

		if self.rect.right >= ANCHO:
			self.vel_x=0
			self.rect.right=ANCHO



#Plataformas
class Plataforma (pygame.sprite.Sprite):
	def __init__(self,pos,imagen):
		pygame.sprite.Sprite.__init__(self)
		self.image=imagen
		
		self.rect=self.image.get_rect()
		self.rect.x=pos[0]
		self.rect.y=pos[1]


#Proyectiles (Balas, misiles)
class Bullet(pygame.sprite.Sprite):
	def __init__(self,m):
		pygame.sprite.Sprite.__init__(self)
		self.m = m
		self.action = 0
		self.i = 0
		self.image = self.m[self.action][self.i]
		self.rect=self.image.get_rect()
		self.vel_y=0
		self.vel_x=0
		self.tipo=0


	def update(self):

		self.image=self.m[self.action][self.i]
		
		if self.tipo == 2:
			self.i+=1

		if self.i >= len(self.m[self.action]):
				self.i=0

		
		self.rect.x+= self.vel_x
		self.rect.y+= self.vel_y


#Modificadores
class Modificador (pygame.sprite.Sprite):
	def __init__(self,m):
		pygame.sprite.Sprite.__init__(self)
		self.m = m
		self.i=0
		self.action=0
		self.image=self.m[self.action][self.i]
		self.rect=self.image.get_rect()
		self.vel_y=0
		self.vel_x=0
		self.pls=None

	def gravity(self):
		if self.vel_y == 0:
			self.vel_y+=1
		else:
			self.vel_y+=0.5

	def update(self):
		self.gravity()
		self.image = self.m[self.action][self.i]
		self.rect.y+=self.vel_y
		self.rect.x+=self.vel_x

		col=pygame.sprite.spritecollide(self,self.pls,False)
		for p in col:
			'''if(self.vel_y<=0) and (self.rect.top <= p.rect.bottom):
				self.rect.top=p.rect.bottom
				self.vel_y=0'''

			if(self.vel_y>0) and (self.rect.bottom >= p.rect.top):
				self.rect.bottom=p.rect.top
				self.vel_y=0
				self.sl = 0
		
#Salud
class Salud (pygame.sprite.Sprite):
	def __init__(self,s,color):
		pygame.sprite.Sprite.__init__(self)
		self.s=s
		self.color=color
		self.image = pygame.Surface([s,5])
		self.image.fill(self.color)
		self.rect = self.image.get_rect()
		self.rect.x=25
		self.rect.y=0
		self.posy = 0
		self.posx = 0


	def update(self):
		self.image = pygame.Surface([self.s,5])
		self.image.fill(self.color)
		self.rect = self.image.get_rect()
		self.rect.y = self.posy
		self.rect.x = self.posx






#progrma principal
if __name__ == '__main__':
	pygame.init()

	#Definicion de variables
	#Pantalla
	pantalla = pygame.display.set_mode([ANCHO,ALTO])
	#Sabana sprites Jugador 1
	j1m = Recortar(10,4,'player/j1.png',[4,1,3,1,2,4,1,3,1,2])
	#Sabana de plataformas
	nivel=Recortarmap(21,73,'maps/terrenos.png')
	#Dimensiones en alto y ancho de cada seccion de plataforma
	anc=nivel[0][0].get_rect()
	#Sabana sprites de Aviones
	am = Recortar(1,2,'foes/avion.png',[2])
	#Sabana sprites de Balas
	bm = Recortar(1,7,'balas/modificadores.png',[7])
	#Sabana proyectiles del jugador
	jbm = Recortar(2,8,'balas/book.png',[8,1])
	#Sabana sprites enemigo mobiles
	el1 = Recortar(6,3,'enemigos/el11.png',[3,3,3,3,3,3])
	#Sabana sprites enemigo estatico
	es = Recortar(1,1,'enemigos/es.png',[1])
	#Sabana de maquinaria jefe1
	boss1 =Recortar(2,8,'boss/boss11.png',[8,4])
	#Sabana de hombre cerdo jefe2
	boss2 =Recortar(10,8,'boss/boss22.png',[8,3,6,7,7,8,3,6,7,7])
	#Sabana de maquinaria jefe1
	boss3 =Recortar(4,4,'boss/boss3.png',[4,2,4,2])
	#Balas jefe 1
	bmq =Recortar(1,1,'balas/bmq.png',[1])
	#Balas enemigo estatico
	bstc = Recortar(1,2,'balas/bstc.png',[2])
	#Balas jugador
	bj = Recortar(2,8,'balas/book.png',[8,1])
	#Cargar Game over
	go = pygame.image.load('game_over.png')

	#Cargar fondo nivel 1
	#Cargar game over
	#Cargar You Win
	#Variable posicion del fondo
	pos_f = 0

	#Definicion de grupos
	todos = pygame.sprite.Group()
	jugadores = pygame.sprite.Group()
	modificadores = pygame.sprite.Group()
	plataformas=pygame.sprite.Group()
	enemigos = pygame.sprite.Group()
	balas=pygame.sprite.Group()
	pi=0

	ruta='maps/nivel0.json'
	#Definicion de plataformas
	#bs=cargar_pl(ruta,todos,plataformas)

	#Defiicion de jugadores
	j1 = Jugador(j1m)
	#j1.action=0
	j1.rect.x=70
	j1.rect.y=50
	j1.health=100
	j1.shield=0
	j1.pls=plataformas
	jugadores.add(j1)
	todos.add(j1)
	s1=Salud(j1.health,Verde)
	s1.posx=25
	todos.add(s1)
	sh1=Salud(j1.shield,Azul)
	sh1.posx=25
	sh1.posy=7
	todos.add(sh1)

	#Definicion de avion arrojador de Modificadores
	plane= Foe([-100, 50],am)
	plane.tipo='a'
	enemigos.add(plane)
	todos.add(plane)

	#Baderas de movimiento
	move=False
	
	#Banderas jugador
	up1=False
	down1=False
	left1=False
	right1=False	
	salto1=False

	

	fonm1=False

	#bandera movimiento del fondo
	fondm=False

	#Orientacion del avion
	plm=False

	#Bandera de movimiento de plataformas
	plaav = False

	#Bandera de nivel
	level=1
	leve=0

	#Winner
	wi=False

	#Bandera cambio de nivel
	c=True

	#Bandera de displaros del avion
	dplane=0

	#Bandera disparos enemigo mobible
	dmob=0

	#Bandera del Boss Field
	bs=0

	#Bandera orientacion de enemigo
	be=False

	#Bandera movilidad de enemigos en pantalla
	ons=False

	#Badera para crear Jefe
	cb=True

	#Bandera disparos de enemigo estatico
	dis=0

	#Banderas comportamieto del Jefe
	ad=60
	af=120
	ja=100
	mx=100

	#Claves para pasar de nivel
	#golvl2, golvl3
	#Claves para llegar hasta el boss de cada nivel
	#gotoboss
	cheats=''

	#Orientacion
	ori=5

	#Baderas de modificadores
	tim=False #Velocidad de enemigos es reducida al cambiaar a True
	noa=False #Los enemigos no atacan al cambiar a True
	velc=True #La velocidad del jugador decrece a la mitad al cambiar a False
	rj=False #El salto del jugador se reduce a la mitad al cambiar a True

	#Banderas de tiempo de mods
	rjcd=0 #Salto retringido
	timcd=0 #Velocida reducida de enemigos
	noacd=0 #Enemigos no atacan
	velcd=0 #Velocidad del jugador se reduce

	#Pausa
	pause=False

	#Definicion del reloj
	reloj=pygame.time.Clock()

	#Cilco de programa
	fin = False
	while not fin:

		s1.s=j1.health
		sh1.s=j1.shield


		if dis == 0:
			dis =100
		dis-=1
		if rjcd == 0:
			rj=False
		rjcd-=1
		if timcd == 0:
			tim=False
		timcd-=1
		if noacd==0:
			noa=False
		noacd-=1
		if velcd==0:
			velc=True
		velcd-=1
		
		if bs <= 0: 
			
			if not cb and level==3:
				boss=Jefe([ANCHO-30,0],boss1)
				boss.pls=plataformas
				enemigos.add(boss)
				todos.add(boss)
				
				sb=Salud(boss.health,Rojo)
				sb.posx=(ANCHO-boss.health)
				sb.posy=(ALTO-10)
				todos.add(sb)
				cb=True
			elif not cb and level==5:
				boss=Jefe([ANCHO-30,0],boss2)
				boss.pls=plataformas
				boss.action=6
				boss.l=2
				enemigos.add(boss)
				todos.add(boss)

				sb=Salud(boss.health,Rojo)
				sb.posx=(ANCHO-boss.health)
				sb.posy=(ALTO-10)
				todos.add(sb)
				cb=True
			elif not cb and level==6:
				boss=Jefe([ANCHO-30,0],boss3)
				boss.pls=plataformas
				boss.action=2
				boss.l=3
				boss.health=500
				enemigos.add(boss)
				todos.add(boss)

				sb=Salud(boss.health,Rojo)
				sb.posx=(ANCHO-boss.health)
				sb.posy=(ALTO-10)
				todos.add(sb)
				cb=True

			if c:
				if level == 1:
					bs=cargar_pl(ruta,todos,plataformas)
					for i in range(int(bs/300)):
						e=Foe([(350*(i+1)),100],el1)
						e.pls = plataformas
						e.tipo = 'mob'
						e.health = 5
						enemigos.add(e)
						todos.add(e)

						ne=Foe([(350*(i+1)),100],es)
						ne.pls = plataformas
						ne.tipo = 'stc'
						enemigos.add(ne)
						todos.add(ne)

					level=3
					c=False
					cb=False

				elif level == 3:
					for p in plataformas:
						pygame.sprite.Sprite.kill(p)
					for e in enemigos:
						if e.tipo != 'a':
							pygame.sprite.Sprite.kill(e)

					bs=cargar_pl('maps/nivel1.json',todos,plataformas)
					for i in range(int(bs/300)):
						e=Foe([(350*(i+1)),290],el1)
						e.pls=plataformas
						e.tipo= 'mob'
						e.health = 10
						enemigos.add(e)
						todos.add(e)

						ne=Foe([(350*(i+1)),100],es)
						ne.pls = plataformas
						ne.tipo = 'stc'
						enemigos.add(ne)
						todos.add(ne)
					level=5
					c=False
					cb=False

				elif level == 5:
					for p in plataformas:
						pygame.sprite.Sprite.kill(p)
					for e in enemigos:
						if e.tipo != 'a':
							pygame.sprite.Sprite.kill(e)

					bs=cargar_pl('maps/nivel2.json',todos,plataformas)
					for i in range(int(bs/300)):
						e=Foe([(350*(i+1)),290],el1)
						e.pls=plataformas
						e.tipo= 'mob'
						e.health = 15
						enemigos.add(e)
						todos.add(e)

						ne=Foe([(350*(i+1)),100],es)
						ne.pls = plataformas
						ne.tipo = 'stc'
						enemigos.add(ne)
						todos.add(ne)
					level=6
					c=False
					cb=False

				elif level==6:
					fin=True

			else:
				for e in enemigos:
					if e.tipo == 'mob' or e.tipo == 'stc':
						pygame.sprite.Sprite.kill(e)


				


		#Gestion de eventos
		for event in pygame.event.get():

			#Fin de programa
			if event.type == pygame.QUIT:
				fin = True

			#Definicion de movimientos
			if event.type in (pygame.KEYDOWN, pygame.KEYUP):
				if event.type == pygame.KEYDOWN:
					move=True
					if event.key <256:
						cheats+= chr(event.key)

					if event.key == pygame.K_UP:
						cheats=''
						j1.pra=j1.action
						if j1.sl < 2:
							if not rj:
								j1.vel_y=-10
							else:
								j1.vel_y=-5
							j1.sl+=1
					#	j1.vel_y=1

						
					if event.key == pygame.K_DOWN:
						cheats=''
						j1.pra=j1.action
						down1=True
						j1.i=0
					#	j1.action=1
						
					if event.key == pygame.K_LEFT:
						cheats=''
						j1.pra=j1.action
						left1=True
						j1.action=5
						j1.i=0

					if event.key == pygame.K_RIGHT:
						cheats=''
						j1.pra=j1.action
						right1=True
						j1.action=0
						j1.i=0
					
					if event.key == pygame.K_p:
						cheats=''
						pause= not pause

					if event.key == pygame.K_a:
						j1.pra=j1.action
						ag = Bullet(bj)
						ag.action=1
						ag.i=0
						ag.tipo=2
						ag.rect.center=j1.rect.center
						if j1.action< 4:
							j1.action=4
							ag.vel_x=6
						elif j1.action>4:
							j1.action=9
							ag.vel_x=-6
						j1.i=0
						balas.add(ag)
						todos.add(ag)


					if event.key == pygame.K_s:
						j1.pra=j1.action
						bk = Bullet(bj)
						bk.action=0
						bk.i=0
						bk.tipo=2
						bk.rect.center=j1.rect.center
						if j1.action< 4:
							j1.action=4
							bk.vel_x=6
						elif j1.action>4:
							j1.action=9
							bk.vel_x=-6
						j1.i=0
						balas.add(bk)
						todos.add(bk)


				if event.type == pygame.KEYUP:
					
					
					
					if event.key == pygame.K_DOWN:
						down1=False
						j1.action=1
						if right1:
							j1.action=0
							j1.i=0



					if event.key == pygame.K_LEFT:
						left1=False
						j1.vel_x=0
						j1.i=0
						j1.action=6


					if event.key == pygame.K_RIGHT:
						right1=False
						fonm1 = False
						plaav = False
						j1.vel_x=0
						j1.i=0
						j1.action=1

					
					if (not right1) and (not left1) and (not up1) and (not down1):
						move= False
						
					

		if j1.health > 0 and not wi and j1.rect.y < 500 and not pause:
			if move:

				if right1 and not down1:
					
					if j1.rect.x >= (ANCHO-300) and bs > 0:
						j1.vel_x=0 
						j1.mf=True
						plaav=True

					elif j1.rect.x < (ANCHO-25):
						if velc:
							j1.vel_x=5
						else:
							j1.vel_x=2
						j1.mf=False

					elif j1.rect.x >= (ANCHO-25):
						j1.vel_x=0

				if down1 :
					if j1.action < 5:
						j1.action=3

					else:
						j1.action=8

					j1.i=0

					if j1.vel_x != 0:
						if j1.vel_x < 0:
							j1.vel_x+=0.2
						if j1.vel_x > 0:
							j1.vel_x+=-0.2
					

				if left1 and not down1 :
					if j1.rect.x >= 0:
						if velc:
							j1.vel_x=-5
						else:
							j1.vel_x=-2
					else:
						j1.vel_x=0



			#Desplazamiento de plataformas
			for pla in plataformas:
				if plaav and bs > 0:
					pla.rect.x-=5
				if cheats== 'gotobosz':
					pla.rect.x-=bs
			if plaav:
				bs-=5
			elif cheats== 'gotobosz':
				bs=0
				j1.vel_y=-1

			#Frecuencia de disparo avion
			if dplane == 0:
				dplane = random.randrange(50,100)

			#Frecuencia disparo de mobs
			if dmob == 0:
				dmob = random.randrange(30,70)
			#Reduccion de la bandera para generar un disparo
			dplane-=1
			dmob-=1

			#Dezplazamiento de enemigos
			for e in enemigos:
				cole = pygame.sprite.spritecollide(e,balas,False)
				for bt in cole:
					if bt.tipo == 2 and e.tipo != 'a' and e.tipo != 'stc':
						if bt.action==0:
							e.health-=5
							
						elif bt.action==1:
							e.health-=10
						if e.health <= 0:
							if e.tipo == 'b':
								e.health=1
								c=True
							pygame.sprite.Sprite.kill(e)
						pygame.sprite.Sprite.kill(bt)

				if e.tipo == 'mob':

					if e.rect.left > ANCHO:
						ons = False
					elif e.rect.left <= ANCHO:
						ons = True

					if j1.rect.center[0] < e.rect.center[0]:
						if e.health < 10:
							leve=0
						elif e.health < 15:
							leve=2
						elif e.health < 20:
							leve=4
						e.action=leve
						be=False

					elif j1.rect.center[0] > e.rect.center[0]:
						if e.health < 10:
							leve=1
						elif e.health < 15:
							leve=3
						elif e.health < 20:
							leve=5

						e.action=leve
						be=True

						#print j1.rect.center
					if ons:
						if  be and not plaav:
							if noa:
								e.vel_x=0
							elif not tim:
								e.vel_x=4.9
							else:
								e.vel_x=1.9

						elif be and plaav:
							if noa:
								e.vel_x=-5
							elif not tim:
								e.vel_x= -0.1
							else:
								e.vel_x= -0.01

						elif not be and plaav:
							if noa:
								e.vel_x=-5
							elif not tim:
								e.vel_x=-9.9
							else:
								e.vel_x=-6.9

						elif not be and not plaav:
							if noa:
								e.vel_x=0
							elif not tim:
								e.vel_x=-4.9
							else:
								e.vel_x=-1.9

					else:
						if plaav:
							e.vel_x=-5
						else:
							e.vel_x=0

					if e.rect.top > ALTO:
						pygame.sprite.Sprite.kill(e)

				elif e.tipo == 'stc':
					if plaav:
						e.vel_x=-5
					else:
						e.vel_x=0
					if dis == 0:
						if j1.rect.right < (e.rect.left - 10):
							bala= Bullet(bstc)
							bala.i=0
							bala.vel_x=-7
							
						elif j1.rect.left > (e.rect.right + 10):
							bala= Bullet(bstc)
							bala.i=1
							bala.vel_x=7
						
						bala.rect.center= e.rect.center
						balas.add(bala)
						todos.add(bala)

				elif e.tipo == 'a':
					if (plm) and (not plaav):
							e.vel_x=7

					if plm and plaav:
						e.vel_x=2

					if (not plm) and (not plaav):
						e.vel_x=-7

					if (not plm) and plaav:
						e.vel_x=-12

					if e.rect.x >= (ANCHO+500):
						e.i=0
						plm=False
						

					if e.rect.x <= -500:
						e.i=1
						plm=True

					
					if dplane == 0:
						mod=Modificador(bm)
						mod.rect.center=e.rect.center
						mod.action=0
						mod.pls=plataformas
						mod.i=random.randrange(7)
						modificadores.add(mod)
						todos.add(mod)

				elif e.tipo == 'b':
					#Comportamiento de Jefes
					sb.s=e.health
					if ad <= 0:
						ad=random.randrange(90, 130)
						af= random.randrange(100,130)
						e.vel_x=0

					if ja <= 0:
						ja=random.randrange(100, 130)
						

					if mx <= 0:
						mx=random.randrange(100, 130)
						ja=random.randrange(100, 130)
						

					if af <= 0:
						af=random.randrange(100,250)
						ad=random.randrange(90, 130)

					ad-=1
					af-=1
					ja-=1
					mx-=1
					if e.rect.x < j1.rect.x:
						ori=0
						if level==6:
							ori=2
					else:
						if level==5:
							ori=5
						elif level==6:
							ori=0


					if ja == 0:
						if level==5:
							e.action=ori+1
							e.i=1
						else:
							e.i=0
						e.vel_y=-10
						mx=random.randrange(100, 130)
						

					if mx == 0:
						e.i=0
						if e.rect.x < j1.rect.x:
							e.action=0
							if level==6:
								e.action=0
							e.vel_x=random.randrange(2,3)

						elif e.rect.x > j1.rect.x:
							if level== 5:
								e.action=5
							elif level==6:
								e.action=2

							e.vel_x=random.randrange(-3,-2)


					if ad == 0:
						e.i=0

						if level==3:
							e.action=1
						
						if level==5:
							e.action=ori+2
							
						if e.rect.x < j1.rect.x:
							bala=Bullet(bmq)
							bala.rect.center=e.rect.center
							bala.vel_x=4
							bala.tipo=1
							
						elif e.rect.x > j1.rect.x:
							bala=Bullet(bmq)
							bala.rect.center=e.rect.center
							bala.vel_x=-4
							bala.tipo=1

						balas.add(bala)
						todos.add(bala)
					

					'''
					if af == 0:
						bala=Bullet()
						bala.rect.center=jugador.rect.center
						bala.vel_y=-20
						bala.vel_x=4
						bala.tipo=1
						balas.add(bala)
						todos.add(bala)	
					'''


			for b in balas:
				if b.tipo==0:
					if plaav and (b.vel_x < 0):
						b.vel_x=-12
					elif plaav and (b.vel_x < 0):
						b.vel_x=-7
				if b.rect.right < 0 or b.rect.left > ANCHO:
					pygame.sprite.Sprite.kill(b)


			for b in modificadores:
				if plaav:
					b.vel_x=-5

				elif not plaav:
					b.vel_x=0

				if b.rect.top > ALTO or b.rect.right < 0 or b.rect.left > ANCHO:
					pygame.sprite.Sprite.kill(b)

			colm=pygame.sprite.spritecollide(j1,modificadores,True)
			for modi in colm:
				if modi.i == 0:
					j1.health=100
				if modi.i == 1:
					j1.health-=25
				if modi.i == 2:
					tim=True
					timcd=150
				if modi.i == 3:
					j1.shield=102
				if modi.i == 4:
					noa=True
					noacd=100
				if modi.i == 5:
					velc=False
					velcd=150
				if modi.i == 6:
					j1.health-=5
					rj=True
					rjcd=300

			cole=pygame.sprite.spritecollide(j1,enemigos,False)
			for enc in cole:
				if enc.tipo=='mob' :
					if not noa:
						
						if j1.shield >2:
							j1.shield-=5

						if j1.shield <=2:
							j1.shield=2
							j1.health-=2


						

						

			


			colb=pygame.sprite.spritecollide(j1,balas,False)
			for bls in colb:
				if bls.tipo != 2:
					if j1.shield>2:
						j1.shield-=5

					if j1.shield <=2:
						j1.shield=2
						j1.health-=3
					pygame.sprite.Sprite.kill(bls)
			
			if  'golvl2' in cheats :
				bs=0
				c=True
				cheats=''
			elif 'golvl3' in cheats:
				bs=0
				c=True
				level=5
				cheats=''

			#Refresco de pantalla
			todos.update()
			pantalla.fill(Blanco)
			todos.draw(pantalla)

		#Cierre de juego al perder todad la vida
		if j1.health <= 0 or j1.rect.y >= 500:
			pantalla.blit(go ,[0,0])
			pygame.mixer.music.pause()

		if wi:
			pantalla.blit(fg,[10,200])
			pygame.mixer.music.pause()




		pygame.display.flip()
		#Optimo con 15
		reloj.tick(30) 