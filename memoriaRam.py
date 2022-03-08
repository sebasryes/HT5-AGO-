import simpy
import random
import statistics

#Se declaran variables
capRAM = 100
interval = 10
res = []
random.seed(11)
proc = 1
procesos = 25
inst = 3


#Se hacen funciones para cada parte del proceso
def new(env, nom, capRAM, res):
    #Comienza a correr el tiempo al crear el proceso
    inicio = env.now
    memoria = random.randint(1,10)
    print('Proceso %s creado en %d' %(nom, inicio))

    #Se revisa que hay memoria disponible
    if memoria > capRAM.capacity:
        print("Proceso %s espera a recibir memoria RAM en %d" %(nom, env.now))
    else:
        capRAM.get(memoria)
        yield env.process(ready(env, nom, capRAM, memoria, inicio))


def ready(env, nom, capRAM, memoria, inicio):
    #El proceso es atendido por el CPU
    print("Proceso %s espera a ser atendido por el CPU  en %d" %(nom, env.now))
    yield env.process(running(env, nom, capRAM, res, memoria, inicio))

def running(env, nom, capRAM, res, memoria, inicio):
    terminated = False
    instrucciones = random.randint(1,10)
    destino = random.randint(1,2)
    #Se hace el proceso hasta que no queden instrucciones
    while terminated == False:
        instrucciones = instrucciones - inst
        yield env.timeout(1)

        if instrucciones > 2:
            if destino == 1:
                print("Proceso %s hace operacion I/O en %d" % (nom, env.now))
                yield env.timeout(1)

        else:
            terminated = True

    #Se termina el proceso

    print("Proceso %s ha terminado en %d" %(nom, env.now))    
    capRAM.put(memoria)
    end = env.now
    tiempo = end - inicio
    res.append(tiempo)
#Se repite todo hasta que no quede ningun proceso por hacer
def ej(env, procesos, interval, capRAM, res):
    for i in range(procesos):
        t = random.expovariate(1/interval)
        yield env.timeout(t)
        env.process(new(env, i, capRAM, res))

#Se crea el ambiente, contenedor y recurso y luego se ejecuta el programa
env = simpy.Environment()
procesadores = simpy.Resource(env, capacity=proc)
ram = simpy.Container(env, init=capRAM, capacity=capRAM)
env.process(ej(env, procesos, interval, ram, res))
env.run()

#Se calcula el promedio y desviacion estandar
r = 0
for i in res:
    r = r + i
prom = r / procesos
desv = statistics.stdev(res)

print ("El tiempo promedio por proceso es: %s" %(prom))
print ("La desviación estandar es: %s"%(desv))