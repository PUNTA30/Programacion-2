import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import statistics

def generar_datos(n, seed):
    random.seed(seed)
    datos = []

    for i in range(n):
        cpu = random.uniform(10, 100)
        temperatura = random.uniform(30, 90)
        energia = random.uniform(100, 500)

        estado = evaluar_estado(cpu, temperatura, energia)

        datos.append({
            "cpu": cpu,
            "temperatura": temperatura,
            "energia": energia,
            "estado": estado
        })

    return datos

def evaluar_estado(cpu, temperatura, energia):

    if temperatura > 75 and cpu > 80:
        return "CRITICO"
    elif energia > 400:
        return "ADVERTENCIA"
    elif cpu >= 90:
        return "ADVERTENCIA"
    else:
        return "OK"

def calcular_procesos_restantes(cpu):
    if cpu >= 90:
        return int((100 - cpu) * 2)
    return None

def analizar_datos(datos):

    total = len(datos)
    estados = {"OK": 0, "ADVERTENCIA": 0, "CRITICO": 0}

    for d in datos:
        estados[d["estado"]] += 1

    promedio_cpu = statistics.mean([d["cpu"] for d in datos])
    max_temp = max([d["temperatura"] for d in datos])

    return total, estados, promedio_cpu, max_temp

def generar_y_mostrar():

    try:
        n = int(entry_n.get())
        seed = int(entry_seed.get())

        if n <= 0:
            messagebox.showerror("Error", "El número de registros debe ser mayor que 0")
            return

    except ValueError:
        messagebox.showerror("Error", "Ingrese valores numéricos válidos")
        return

    global datos
    datos = generar_datos(n, seed)

    total, estados, promedio_cpu, max_temp = analizar_datos(datos)

    label_total.config(text=f"Total registros: {total}")
    label_ok.config(text=f"OK: {estados['OK']}")
    label_adv.config(text=f"Advertencia: {estados['ADVERTENCIA']}")
    label_crit.config(text=f"Crítico: {estados['CRITICO']}")
    label_cpu.config(text=f"Promedio CPU: {promedio_cpu:.2f}%")
    label_temp.config(text=f"Temperatura Máxima: {max_temp:.2f}°C")

    actualizar_graficos()


def actualizar_graficos():

    for widget in frame_graficos.winfo_children():
        widget.destroy()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))

    temperaturas = [d["temperatura"] for d in datos]
    estados = [d["estado"] for d in datos]

    # Histograma Temperatura
    ax1.hist(temperaturas, bins=10)
    ax1.set_title("Histograma Temperatura")

    # Barras por estado
    conteo = {
        "OK": estados.count("OK"),
        "ADVERTENCIA": estados.count("ADVERTENCIA"),
        "CRITICO": estados.count("CRITICO")
    }

    ax2.bar(conteo.keys(), conteo.values())
    ax2.set_title("Estados del Sistema")

    canvas = FigureCanvasTkAgg(fig, master=frame_graficos)
    canvas.draw()
    canvas.get_tk_widget().pack()


ventana = tk.Tk()
ventana.title("Guardian v3 - Sistema de Monitoreo")
ventana.geometry("900x600")

frame_top = tk.Frame(ventana)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Número de Registros:").grid(row=0, column=0)
entry_n = tk.Entry(frame_top)
entry_n.grid(row=0, column=1)

tk.Label(frame_top, text="Seed:").grid(row=0, column=2)
entry_seed = tk.Entry(frame_top)
entry_seed.grid(row=0, column=3)

tk.Button(frame_top, text="Generar Datos", command=generar_y_mostrar).grid(row=0, column=4, padx=10)

frame_metricas = tk.Frame(ventana)
frame_metricas.pack(pady=10)

label_total = tk.Label(frame_metricas, text="Total registros: 0")
label_total.grid(row=0, column=0, padx=10)

label_ok = tk.Label(frame_metricas, text="OK: 0")
label_ok.grid(row=0, column=1, padx=10)

label_adv = tk.Label(frame_metricas, text="Advertencia: 0")
label_adv.grid(row=0, column=2, padx=10)

label_crit = tk.Label(frame_metricas, text="Crítico: 0")
label_crit.grid(row=0, column=3, padx=10)

label_cpu = tk.Label(frame_metricas, text="Promedio CPU: 0")
label_cpu.grid(row=1, column=0, padx=10)

label_temp = tk.Label(frame_metricas, text="Temperatura Máxima: 0")
label_temp.grid(row=1, column=1, padx=10)

frame_graficos = tk.Frame(ventana)
frame_graficos.pack(pady=20)

ventana.mainloop()
