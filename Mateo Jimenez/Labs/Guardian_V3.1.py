import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import statistics
from datetime import datetime


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
    return ""


def generar_datos(n, seed):
    random.seed(seed)
    datos_generados = []

    for i in range(n):
        cpu = random.uniform(10, 100)
        temperatura = random.uniform(30, 90)
        energia = random.uniform(100, 500)

        estado = evaluar_estado(cpu, temperatura, energia)
        procesos = calcular_procesos_restantes(cpu)

        datos_generados.append({
            "id": i + 1,
            "cpu": cpu,
            "temperatura": temperatura,
            "energia": energia,
            "estado": estado,
            "procesos": procesos
        })

    return datos_generados


def analizar_datos(datos):
    total = len(datos)
    estados = {"OK": 0, "ADVERTENCIA": 0, "CRITICO": 0}

    for d in datos:
        estados[d["estado"]] += 1

    promedio_cpu = statistics.mean([d["cpu"] for d in datos])
    max_temp = max([d["temperatura"] for d in datos])

    return total, estados, promedio_cpu, max_temp


def generar_reporte_txt(datos, metricas):
    archivo = filedialog.asksaveasfilename(defaultextension=".txt",
                                           filetypes=[("Archivo de texto", "*.txt")])
    if not archivo:
        return

    total, estados, promedio_cpu, max_temp = metricas

    with open(archivo, "w", encoding="utf-8") as f:
        f.write("REPORTE GUARDIAN v3.1\n")
        f.write(f"Fecha: {datetime.now()}\n\n")
        f.write("MÉTRICAS GENERALES\n")
        f.write(f"Total registros: {total}\n")
        f.write(f"OK: {estados['OK']}\n")
        f.write(f"Advertencia: {estados['ADVERTENCIA']}\n")
        f.write(f"Crítico: {estados['CRITICO']}\n")
        f.write(f"Promedio CPU: {promedio_cpu:.2f}%\n")
        f.write(f"Temperatura Máxima: {max_temp:.2f}°C\n\n")
        f.write("DETALLE DE REGISTROS\n")

        for d in datos:
            f.write(
                f"ID {d['id']} | CPU: {d['cpu']:.2f}% | Temp: {d['temperatura']:.2f}°C | "
                f"Energía: {d['energia']:.2f}W | Estado: {d['estado']} | "
                f"Procesos Restantes: {d['procesos']}\n"
            )

    messagebox.showinfo("Éxito", "Reporte exportado correctamente.")


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

    global datos_actuales, metricas_actuales
    datos_actuales = generar_datos(n, seed)
    metricas_actuales = analizar_datos(datos_actuales)

    total, estados, promedio_cpu, max_temp = metricas_actuales

    label_total.config(text=f"Total: {total}")
    label_ok.config(text=f"OK: {estados['OK']}")
    label_adv.config(text=f"Advertencia: {estados['ADVERTENCIA']}")
    label_crit.config(text=f"Crítico: {estados['CRITICO']}")
    label_cpu.config(text=f"Promedio CPU: {promedio_cpu:.2f}%")
    label_temp.config(text=f"Temp Máx: {max_temp:.2f}°C")

    actualizar_tabla()
    actualizar_graficos()


def actualizar_tabla():
    for row in tabla.get_children():
        tabla.delete(row)

    for d in datos_actuales:
        tabla.insert("", "end", values=(
            d["id"],
            f"{d['cpu']:.2f}",
            f"{d['temperatura']:.2f}",
            f"{d['energia']:.2f}",
            d["estado"],
            d["procesos"]
        ), tags=(d["estado"],))


def actualizar_graficos():
    for widget in frame_graficos.winfo_children():
        widget.destroy()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))

    temperaturas = [d["temperatura"] for d in datos_actuales]
    estados = [d["estado"] for d in datos_actuales]

    ax1.hist(temperaturas, bins=10)
    ax1.set_title("Distribución Temperatura")

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
ventana.title("Guardian v3.1 - Sistema Inteligente")
ventana.geometry("1100x750")
ventana.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background="#2b2b2b",
                foreground="white",
                rowheight=25,
                fieldbackground="#2b2b2b")

style.map('Treeview', background=[('selected', '#4a6984')])

frame_top = tk.Frame(ventana, bg="#1e1e1e")
frame_top.pack(pady=10)

tk.Label(frame_top, text="Registros:", bg="#1e1e1e", fg="white").grid(row=0, column=0)
entry_n = tk.Entry(frame_top)
entry_n.grid(row=0, column=1)

tk.Label(frame_top, text="Seed:", bg="#1e1e1e", fg="white").grid(row=0, column=2)
entry_seed = tk.Entry(frame_top)
entry_seed.grid(row=0, column=3)

tk.Button(frame_top, text="Generar", command=generar_y_mostrar).grid(row=0, column=4, padx=10)
tk.Button(frame_top, text="Exportar TXT",
          command=lambda: generar_reporte_txt(datos_actuales, metricas_actuales)
          ).grid(row=0, column=5)

frame_metricas = tk.Frame(ventana, bg="#1e1e1e")
frame_metricas.pack(pady=10)

label_total = tk.Label(frame_metricas, text="Total: 0", bg="#1e1e1e", fg="white")
label_total.grid(row=0, column=0, padx=10)

label_ok = tk.Label(frame_metricas, text="OK: 0", bg="#1e1e1e", fg="#00ff00")
label_ok.grid(row=0, column=1, padx=10)

label_adv = tk.Label(frame_metricas, text="Advertencia: 0", bg="#1e1e1e", fg="#ffaa00")
label_adv.grid(row=0, column=2, padx=10)

label_crit = tk.Label(frame_metricas, text="Crítico: 0", bg="#1e1e1e", fg="#ff4444")
label_crit.grid(row=0, column=3, padx=10)

label_cpu = tk.Label(frame_metricas, text="Promedio CPU: 0", bg="#1e1e1e", fg="white")
label_cpu.grid(row=1, column=0, padx=10)

label_temp = tk.Label(frame_metricas, text="Temp Máx: 0", bg="#1e1e1e", fg="white")
label_temp.grid(row=1, column=1, padx=10)

frame_tabla = tk.Frame(ventana)
frame_tabla.pack(pady=10)

columnas = ("ID", "CPU %", "Temp °C", "Energía W", "Estado", "Proc Rest")

tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, width=100)

tabla.pack()

tabla.tag_configure("OK", background="#1e4620")
tabla.tag_configure("ADVERTENCIA", background="#665500")
tabla.tag_configure("CRITICO", background="#661111")

frame_graficos = tk.Frame(ventana)
frame_graficos.pack(pady=20)

datos_actuales = []
metricas_actuales = (0, {"OK": 0, "ADVERTENCIA": 0, "CRITICO": 0}, 0, 0)

ventana.mainloop()