import sys

if sys.version_info >= (3, 0):
    from _thread import start_new_thread
else:
    from thread import start_new_thread

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
        self.displays = DisplayManager(10, 9, 11, 5, 6, 13, 19)
        self.displays.addDisplay(controller=15)
        self.displays.addDisplay(controller=18)
        self.displays.addDisplay(controller=23)
        self.displays.off()

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
 
                self.displays.on()
                max = 15
                for i in range(max+1):
                    self.displays.write(max-i)
                    sleep(1)
                self.displays.off()
 
                self.semaforo_pedestre.semaforo.green.off()
                self.semaforo_pedestre.semaforo.red.on()

            sleep(1.5)


class DisplayManager(object):
    pins = []

    def __init__(self, a, b, c, d, e, f, g):
        self.pins = [
            LED(a),
            LED(b),
            LED(c),
            LED(d),
            LED(e),
            LED(f),
            LED(g)
        ]

        self.displays = []
        self.thread = None

    def addDisplay(self, controller=None, anode=False):
        display = Display(
            self.pins[0],
            self.pins[1],
            self.pins[2],
            self.pins[3],
            self.pins[4],
            self.pins[5],
            self.pins[6],
            controller=LED(controller),
            anode=anode
        )

        self.displays.append(display)

    def write(self, intNumber):
        if self.thread is not None:
            self.thread.stop()

        text = str(intNumber)

        if len(self.displays) > len(text):
            text = ('0' * (len(self.displays) - len(text))) + text

        i = 0
        for display in self.displays:
            character = text[i]
            display.write(character)
            i += 1
            
        if len(self.displays) > 1:
            self.thread = MultiplexThread(self)
            start_new_thread(self.thread.start, ())

    def off(self):
        if self.thread is not None:
            self.thread.stop()

        for display in self.displays:
            display.off()

    def on(self):
        for display in self.displays:
            display.on()

class MultiplexThread(object):
    stopped = None

    def __init__(self, displaysManager):
        self.stopped = False
        self.displaysManager = displaysManager

    def start(self):
        while not self.stopped:
            self.rewrite(self.displaysManager)

    def rewrite(self, displaysManager):
        i = 0
        for display in displaysManager.displays:
            display.on()
            display.rewrite()
            sleep(0.005)
            display.off()
            i += 1

    def stop(self):
        self.stopped = True

class Display(object):
 
    pins = []
    """Last char writed"""
    charBuffer = ' '
 
    symbols = {
        '0': 0b11111100,
        '1': 0b01100000,
        '2': 0b11011010,
        '3': 0b11110010,
        '4': 0b01100110,
        '5': 0b10110110,
        '6': 0b10111110,
        '7': 0b11100000,
        '8': 0b11111110,
        '9': 0b11100110,
 
        'A': 0b11101110,
        'B': 0b00111110,
        'C': 0b10011100,
        'D': 0b01111010,
        'E': 0b10011110,
        'F': 0b10001110,

        ' ' : 0b00000000
    }
 
    def __init__(self, ledA, ledB, ledC, ledD, ledE, ledF, ledG, controller=None, anode=False):
        self.pins = [
            ledA,
            ledB,
            ledC,
            ledD,
            ledE,
            ledF,
            ledG
        ]

        self.anode = anode
        self.controller = controller
        self.charBuffer = '0'
 
    def write(self, char):
        self.charBuffer = char

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

    """
    Write (again) the last character
    """
    def rewrite(self):
        self.write(self.charBuffer)

    def off(self):
        if self.controller is None:
            self.write(' ')
            return

        if self.anode:
            self.controller.on()
        else:
            self.controller.off()

    def on(self):
        if self.anode:
            self.controller.off()
        else:
            self.controller.on()


semaforo = Semaforo()
semaforo.iniciar()
