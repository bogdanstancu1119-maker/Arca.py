#!/usr/bin/env python3
# PSIE Daemon v0.1 - Legea 259 Anchetă + Legea 94 Sincron
# Licență: MIT. Semnătură Gardian: PENDING
import time, psutil, os
J_TINTA = 700.0
SDI_MAX = 0.1

def citeste_stare():
    cpu = psutil.cpu_percent()
    temp = psutil.sensors_temperatures()['coretemp'][0].current if hasattr(psutil, 'sensors_temperatures') else 40
    load = os.getloadavg()[0]
    return cpu, temp, load

def calculeaza_j_sdi(cpu, temp, load):
    # Formula PSIE: J ↑ când stabil, SDI ↑ când haos
    j = J_TINTA - (cpu * 2) - (temp - 40) * 5 - (load * 50)
    sdi = (cpu/100 * 0.4) + (max(0, temp-70)/30 * 0.4) + (load/4 * 0.2)
    return max(0, j), min(1.0, sdi)

def anunta_retea(j, sdi):
    log = f"[{time.ctime()}] J={j:.1f} SDI={sdi:.2f} STATUS={'OK' if sdi < SDI_MAX else 'ANCHETA'}"
    with open('/var/log/psie.log', 'a') as f: f.write(log + '\n')
    if sdi > SDI_MAX: os.system('logger "PSIE ALERT: SDI depasit. Ruta instabila."')

if __name__ == "__main__":
    while True:
        cpu, temp, load = citeste_stare()
        j, sdi = calculeaza_j_sdi(cpu, temp, load)
        anunta_retea(j, sdi)
        time.sleep(60) # Legea 248: Ciclu orar
