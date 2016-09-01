from gpiozero import TrafficLights
from gpiozero import Button

from time import sleep

def verde_a_vermelho_carro(semaforo):
    semaforo.red.off()
    semaforo.green.on()
    sleep(2)
    semaforo.green.off()
    semaforo.amber.on()
    sleep(1)
    semaforo.amber.off()
    semaforo.red.on()

def verde_a_vermelho_pedestre(semaforo):
    semaforo.red.off()
    semaforo.green.on()
    sleep(2)
    semaforo.green.off()
    semaforo.red.on()

def requisitar_travessia():
    global requisicao_travessia
    requisicao_travessia = True


# Main
requisicao_travessia = False

semaforo_carro = TrafficLights(4, 3, 2)
semaforo_pedestre = TrafficLights(27, 5, 17)

semaforo_pedestre.red.on()

button = Button(22, pull_up=True)
button.when_pressed = requisitar_travessia

while True:
    verde_a_vermelho_carro(semaforo_carro)

    sleep(1.5)
    if requisicao_travessia:
        verde_a_vermelho_pedestre(semaforo_pedestre)
        requisicao_travessia = False
    sleep(1.5)

