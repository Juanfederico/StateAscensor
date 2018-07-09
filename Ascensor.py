from transitions import Machine
import time
import os
import math

class Ascensor(object):

    states = ['detenido', 'interrumpido', 'moviendose', 'apagado']

    def __init__(self, name, pisoInicial):

        self.name = name

        self.piso = pisoInicial #"-2 = segundo subsuelo", "-1 = primer subsuelo", "0 = planta baja", "1= piso 1", "2= piso 2", "3= piso 3"

        self.machine = Machine(model=self, states=self.states, initial='detenido', ignore_invalid_triggers=True)

        #self.machine.add_transition('subirAscensor', 'subiendo', 'detenido', after=['subir_1_piso'])
        #self.machine.add_transition('subirAscensor', 'detenido', 'detenido', after=['subir_1_piso'], conditions=['piso_maximo'])
        #self.machine.add_transition('bajarAscensor', 'bajando', 'detenido', after=['bajar_1_piso'])
        #self.machine.add_transition('bajarAscensor', 'detenido', 'detenido', after=['bajar_1_piso'], conditions=['piso_minimo'])

        self.machine.add_transition('moverAscensor', 'detenido', 'moviendose')
        self.machine.add_transition('detenerAscensor', 'moviendose', 'detenido')

        self.machine.add_transition('habilitarAscensor', 'interrumpido', 'detenido')

        self.machine.add_transition('encenderAscensor', 'apagado', 'detenido')
        self.machine.add_transition('apagarAscensor', 'detenido', 'apagado')
        #self.machine.add_transition(trigger='apagar', source='detenido', dest='apagado')

    def piso_a_string(self, piso):
        if piso == -2: stringPiso = "Segundo subsuelo"
        if piso == -1: stringPiso = "Primer subsuelo"
        if piso == -0: stringPiso = "Planta baja"
        if piso == 1: stringPiso = "Piso 1"
        if piso == 2: stringPiso = "Piso 2"
        if piso == 3: stringPiso = "Piso 3"
        return stringPiso

    def piso_maximo(self):
        return self.piso == 3

    def piso_minimo(self):
        return self.piso == -2

    def is_apagado(self):
        return self.state == "apagado"

    def is_encendido(self):
        return self.state != "apagado"

    def is_interrumpido(self):
        return self.state == "interrumpido"

    def habilitar(self):
        if(self.state) == "interrumpido":
            print("Chequeando puerta abierta u obstruccion del ascensor...")
            time.sleep(3)
            print("No se detectaron problemas. Regresando a planta baja...")
            self.habilitarAscensor()
            self.ir_a_piso(0) #Planta baja
            print("Ascensor activado")
        else: print("El ascensor no se encuentra interrumpido")

    def apagar(self):
        if(self.state != "apagado"):
            print("Apagando ascensor...")
            time.sleep(5)
            self.apagarAscensor()
            print("Ascensor apagado")
            print(self.state)
        else: print("El ascensor ya se encuentra apagado ")

    def encender(self):
        if(self.state) == "apagado":
            print("Encendiendo ascensor...")
            time.sleep(5)
            self.encenderAscensor()
            print("Ascensor encendido")
        else: print("El ascensor ya se encuentra encendido")


    def subir_1_piso(self):
        if(self.state) == 'apagado':
            print("Ascensor fuera de servicio\n")
        elif(self.state) == "interrumpido":
            print("Ascensor interrumpido\n")
        elif self.piso == 3:
            print("No se puede subir, piso máximo alcanzado")
        else:
            print("Subiendo...")
            print("-----------------Estado al momento: ["+str(self.state)+"]-------------------")
            if not('.5' in str(self.piso)): 
                self.piso+= 0.5 #Entre un piso y el otro
                time.sleep(4)
            else: time.sleep(2)
            self.piso+= 0.5 #Terminó de subir 1 piso
        print ('Piso actual: ' + self.piso_a_string(self.piso))

    def bajar_1_piso(self):
        if(self.state) == "apagado":
            print("Ascensor fuera de servicio\n")
        elif(self.state) == "interrumpido":
            print("Ascensor interrumpido\n")
        elif self.piso == -2:
            print("No se puede bajar, piso mínimo alcanzado\n")
        else:
            print("Bajando...")
            print("-----------------Estado al momento: ["+str(self.state)+"]-------------------")
            if not('.5' in str(self.piso)): 
                self.piso-= 0.5 #Entre un piso y el otro
                time.sleep(4)
            else: time.sleep(2)
            self.piso-= 0.5 #Terminó de bajar 1 piso
        print ('Piso actual: ' + self.piso_a_string(self.piso))

    def ir_a_piso(self, pisoDestino):
        if(self.state=="interrumpido"): print("Error: el ascensor se encuentra interrumpido")
        elif(self.state=="apagado"): print("Error: ascensor apagado")
        elif(self.piso==pisoDestino): print("Ya se encuentra en el piso indicado\n")
        else:
            while(self.piso!=pisoDestino):
                self.moverAscensor()
                if(self.piso>pisoDestino): self.bajar_1_piso()
                else: self.subir_1_piso()
            self.detenerAscensor()
            print("Ha llegado al piso de destino ("+self.piso_a_string(self.piso)+")\n")

    def consultarEstado(self):
        print("Detalles actuales del ascensor\n")
        pisoDeAbajo = str(self.piso_a_string(math.floor(self.piso))) #Piso de abajo de entre los que se quedó trabado el ascensor
        pisoDeArriba =str(self.piso_a_string(math.ceil(self.piso))) #Piso de arriba de entre los que se quedó trabado el ascensor
        if('.5' in str(self.piso)): print("Piso actual: entre "+pisoDeAbajo+" y "+pisoDeArriba)
        else: print("Piso actual: " +str(self.piso_a_string(self.piso)))
        print("Estado: " + self.state)

def main():
    try:
        while(True):
            print("-----------------Estado al momento: ["+str(ascensor.state)+"]-------------------")
            print("Seleccione la opcion deseada: ")
            opcion = int(input("-2=(Segundo subsuelo)\n-1(Primer subsuelo)\n 0(Planta baja)\n 1(Primer piso)\n 2(Segundo piso)\n 3(Tercer piso)\n 4(Mas opciones)\n"))
            os.system('cls')
            if(opcion==4): 
                opcion = input(" C(Consultar estado actual)\n A(apagar)\n E(encender)\n H(habilitar)\n V(Volver)\n")
                os.system('cls')
                if(opcion.lower()=="C".lower()): ascensor.consultarEstado()
                if(opcion.lower()=="A".lower()): ascensor.apagar()
                elif(opcion.lower()=="E".lower()): ascensor.encender()
                elif(opcion.lower()=="H".lower()): ascensor.habilitar()
                else: time.sleep(1)
            else: ascensor.ir_a_piso(opcion)
    except KeyboardInterrupt:
        print("Interruptor activado: ascensor detenido")
        ascensor.state = "interrumpido"



if __name__ == '__main__':
    ascensor = Ascensor("ascensor", 0) #Planta baja
    while True:
        main()
