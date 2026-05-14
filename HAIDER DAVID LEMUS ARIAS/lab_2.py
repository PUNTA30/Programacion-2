import random
import os
import datetime

fecha_hora = datetime.datetime.now()

def limpiar():
    if os.name == "nt":      
        os.system("cls")
    else:                    
        os.system("clear")

def titulo(texto):
    
    print(texto)
    

try:
    Nombre = input("Ingrese nombre del tecnico socio: ")

    while True:
        try:
            num = int(input("Ingrese numero de servidores a revisar socio: "))
            if num <= 0:
                print("El número debe ser mayor que 0 socio.")
            else:
                break
        except ValueError:
            print("Error: Debe ingresar un número entero válido socio.")

    servidores_en_riesgo = []

    limpiar()
    titulo("Revision De Servidores socio")
    print("Fecha y hora del diagnóstico socio:", fecha_hora)
    

    for i in range(num):
        print(f"\nServidor {i+1}:")

        IDs = input("Ingrese ID del servidor socio: ")

        while True:
            try:
                Carga = float(input("Ingrese carga de CPU (%) socio: "))
                if 0 <= Carga <= 100:
                    break
                else:
                    print("La carga debe estar entre 0 y 100 socio.")
            except ValueError:
                print("Error: Ingrese un número válido socio.")

        while True:
            try:
                Ce = float(input("Ingrese el consumo de energia en watts socio: "))
                if Ce >= 0:
                    break
                else:
                    print("El consumo no puede ser negativo socio.")
            except ValueError:
                print("Error: Ingrese un número válido socio.")

        Temp = random.randint(40, 130)


        if Ce > 400:
            exceso = Ce - 400
            print(f"Socio el exceso de energia que se está consumiendo es de: {exceso} W")
        else:
            print("El consumo de energia es adecuado socio.")

        if Temp > 85 and Carga > 80:
            print("[PELIGRO CRÍTICO]: Apagado de emergencia inminente socio.")
        elif Temp > 80:
            print("[ADVERTENCIA]: Temperatura elevada socio.")
        elif Carga > 80:
            print("[ADVERTENCIA]: Rendimiento comprometido socio.")
        else:
            print("[ESTADO]: Operación normal socio.")

        if Carga >= 90:
            porcentajeFaltante = 100 - Carga
            procesos = int((porcentajeFaltante + 1) // 2)
            print("Procesos adicionales antes de colapsar:", procesos)
        else:
            print("Capacidad de reserva estable socio.")

        print("Temperatura actual:", Temp, "°C")

        if Ce > 400 or Temp > 80 or Carga > 80:
            servidores_en_riesgo.append([IDs, Carga, Ce, Temp])

        

    print()
    titulo("Resumen final")

    if servidores_en_riesgo:
        print("Servidores en riesgo:")
        
        for servidor in servidores_en_riesgo:
            print("ID:", servidor[0],
                "| Carga:", servidor[1],
                "| Consumo:", servidor[2],
                "| Temperatura:", servidor[3])
            
    else:
        print("Todos los servidores están estables socio.")
        

except Exception as e:
    print("Ocurrió un error inesperado en el sistema.")
    print("Detalle técnico:", e)
