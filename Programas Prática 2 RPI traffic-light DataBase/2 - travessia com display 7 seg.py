from gpiozero import TrafficLights
from gpiozero import Button
from gpiozero import LED

from time import sleep


class SemaforoCarro(object):
    requisicao_travessia = False
    semaforo = None

    def __init__(self):
        self.semaforo = TrafficLights(4, 3, 2)

    def verde_a_vermelho(self):
        self.semaforo.red.off()
        self.semaforo.green.on()
        sleep(2)
        self.semaforo.green.off()
        self.semaforo.amber.on()
        sleep(1)
        self.semaforo.amber.off()
        self.semaforo.red.on()


class SemaforoPedestre(object):

    def __init__(self):
        self.semaforo = TrafficLights(27, 14, 17)

    def verde_a_vermelho(self):
        self.semaforo.red.off()
        self.semaforo.green.on()
        sleep(2)
        self.semaforo.green.off()
        self.semaforo.red.on()


class Semaforo(object):
    requisicao_travessia = False
    botao_requisicao = None

    def __init__(self):
        self.semaforo_carro = SemaforoCarro()
        self.semaforo_pedestre = SemaforoPedestre()

        self.botao_travessia = Button(22, pull_up=True)
        self.botao_travessia.when_pressed = self.requisitar_travessia
        self.display = Display(10, 9, 11, 5, 6, 13, 19)
        self.display.off()

    def requisitar_travessia(self):
         self.requisicao_travessia = True

    def iniciar(self):
        self.semaforo_pedestre.semaforo.red.on()

        while True:
            self.semaforo_carro.verde_a_vermelho()

            sleep(1.5)
            if self.requisicao_travessia:
                self.semaforo_pedestre.semaforo.red.off()
                self.semaforo_pedestre.semaforo.green.on()

                #self.semaforo_pedestre.verde_a_vermelho()
                self.requisicao_travessia = False
                sleep(0.5)

				for i in range(10):
                    self.display.write(9-i)
                    sleep(0.5)
                self.display.off()

                self.semaforo_pedestre.semaforo.green.off()
                self.semaforo_pedestre.semaforo.red.on()

            sleep(1.5)

class Display(object):

    pins = []

    symbols = {
        0: 0b11111100,
        1: 0b01100000,
        2: 0b11011010,
        3: 0b11110010,
        4: 0b01100110,
        5: 0b10110110,
        6: 0b10111110,
        7: 0b11100000,
        8: 0b11111110,
        9: 0b11100110,

		'A': 0b11101110,
        'B': 0b00111110,
        'C': 0b10011100,
        'D': 0b01111010,
        'E': 0b10011110,
        'F': 0b10001110,

        'off' : 0b00000000
    }

    def __init__(self, a, b, c, d, e, f, g, anode=False):
        self.pins = [
            LED(a),
            LED(b),
            LED(c),
            LED(d),
            LED(e),
            LED(f),
            LED(g)
        ]

        self.anode = anode

    def write(self, char):
        character = self.symbols[char]
        comparator = 0b10000000

        if not self.anode:
            character = ~character

        for i in range(7):
            light = (comparator & character) == comparator

            if light:
                self.pins[i].on()
            else:
                self.pins[i].off()

            comparator = comparator >> 1

    def off(self):
        self.write('off')
 
semaforo = Semaforo()
semaforo.iniciar()






