import tkinter as tk
from tkinter import ttk, messagebox
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# =========================
# 1) DATOS SINTÉTICOS COHERENTES
# =========================
def generar_datos_sinteticos(n: int, seed=None):

    if seed is not None:
        random.seed(seed)

    servidores = []

    for _ in range(n):

        cpu = random.uniform(30, 100)

        # temperatura ligeramente relacionada con cpu
        temperatura = random.uniform(40, 60) + (cpu * 0.35)

        # energía relacionada con cpu
        energia = 150 + (cpu * 3) + random.uniform(-20, 20)

        procesos_restantes = max(0, 100 - cpu) if cpu >= 90 else None

        servidores.append([temperatura, cpu, energia, procesos_restantes])

    return servidores


# =========================
# 2) REGLAS DEL NEGOCIO
# =========================
def evaluar_estado(temp, cpu, energia):

    if temp > 75 and cpu > 80:
        return "CRÍTICO"

    if energia > 400:
        return "EXCESO"

    if temp > 75 or cpu > 80:
        return "ADVERTENCIA"

    return "OK"


def calcular_metricas(servidores):

    total = len(servidores)
    if total == 0:
        return None

    temperaturas = [s[0] for s in servidores]
    cpus = [s[1] for s in servidores]
    energias = [s[2] for s in servidores]

    estados = [evaluar_estado(s[0], s[1], s[2]) for s in servidores]

    criticos = estados.count("CRÍTICO")
    advertencias = estados.count("ADVERTENCIA")
    ok = estados.count("OK")
    exceso = estados.count("EXCESO")

    cpu_alta = sum(1 for c in cpus if c >= 90)

    return {
        "total": total,
        "prom_temp": sum(temperaturas) / total,
        "prom_cpu": sum(cpus) / total,
        "prom_energia": sum(energias) / total,
        "max_cpu": max(cpus),
        "crit": criticos,
        "adv": advertencias,
        "ok": ok,
        "exceso": exceso,
        "cpu_alta": cpu_alta,
        "temperaturas": temperaturas,
        "cpus": cpus,
        "energias": energias,
        "estados": estados
    }


# =========================
# 3) UI
# =========================
class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("The Data Center Guardian - Dashboard Profesional")
        self.geometry("1250x720")

        self.servidores = []
        self.metricas = None
        self.seed_actual = 42

        self._build_ui()

    def _build_ui(self):

        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Analista:").pack(side="left")
        self.nombre_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.nombre_var, width=20).pack(side="left", padx=8)

        ttk.Label(top, text="N registros:").pack(side="left")
        self.n_var = tk.IntVar(value=40)
        ttk.Entry(top, textvariable=self.n_var, width=8).pack(side="left", padx=8)

        ttk.Label(top, text="Seed:").pack(side="left")
        self.seed_var = tk.IntVar(value=42)
        ttk.Entry(top, textvariable=self.seed_var, width=8).pack(side="left", padx=8)

        ttk.Button(top, text="Generar Datos", command=self.on_generar).pack(side="left", padx=5)
        ttk.Button(top, text="Analizar + Graficar", command=self.on_analizar).pack(side="left", padx=5)

        # Panel métricas
        self.stats = ttk.LabelFrame(self, text="Métricas Globales", padding=10)
        self.stats.pack(fill="x", padx=10, pady=5)

        self.stats_text = tk.StringVar(value="Genera datos para iniciar.")
        ttk.Label(self.stats, textvariable=self.stats_text, font=("Segoe UI", 11)).pack(anchor="w")

        # Panel reporte
        self.reporte_frame = ttk.LabelFrame(self, text="Reporte Ejecutivo", padding=10)
        self.reporte_frame.pack(fill="x", padx=10, pady=5)

        self.reporte_text = tk.StringVar(value="")
        ttk.Label(self.reporte_frame, textvariable=self.reporte_text, font=("Segoe UI", 10)).pack(anchor="w")

        # Panel gráficos
        self.graphs = ttk.LabelFrame(self, text="Visualización Analítica", padding=10)
        self.graphs.pack(fill="both", expand=True, padx=10, pady=10)

        self.fig = Figure(figsize=(11, 5), dpi=100)
        self.ax1 = self.fig.add_subplot(131)
        self.ax2 = self.fig.add_subplot(132)
        self.ax3 = self.fig.add_subplot(133)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graphs)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # =========================
    # BOTONES
    # =========================
    def on_generar(self):

        n = self.n_var.get()
        seed = self.seed_var.get()

        if n <= 0:
            messagebox.showerror("Error", "N debe ser mayor a 0.")
            return

        self.seed_actual = seed
        self.servidores = generar_datos_sinteticos(n, seed)
        self.metricas = None

        self._limpiar_graficas()
        self.canvas.draw()

        self.stats_text.set(
            f"Datos generados correctamente con seed={seed}. "
            f"Total registros: {len(self.servidores)}. "
            f"Presiona 'Analizar + Graficar'."
        )

        self.reporte_text.set("")

    def on_analizar(self):

        if not self.servidores:
            messagebox.showwarning("Atención", "Primero genera datos.")
            return

        self.metricas = calcular_metricas(self.servidores)
        m = self.metricas

        nombre = self.nombre_var.get().strip() or "N/D"

        resumen = (
            f"Analista: {nombre} | Seed: {self.seed_actual}\n"
            f"Total: {m['total']} | CPU Máx: {m['max_cpu']:.2f}%\n"
            f"Prom Temp: {m['prom_temp']:.2f}°C | Prom CPU: {m['prom_cpu']:.2f}% | Prom Energía: {m['prom_energia']:.2f} kWh\n"
            f"OK: {m['ok']} | Advertencia: {m['adv']} | Crítico: {m['crit']} | Exceso: {m['exceso']}"
        )

        self.stats_text.set(resumen)

        # Generar reporte automático
        nivel_riesgo = "ALTO" if m["crit"] > 0 else "MEDIO" if m["adv"] > 0 else "BAJO"

        reporte = (
            f"Nivel General del Sistema: {nivel_riesgo}\n"
            f"Servidores con CPU ≥ 90%: {m['cpu_alta']}\n"
            f"Recomendación: "
        )

        if nivel_riesgo == "ALTO":
            reporte += "Revisar servidores críticos inmediatamente."
        elif nivel_riesgo == "MEDIO":
            reporte += "Monitoreo continuo recomendado."
        else:
            reporte += "Sistema operando con normalidad."

        self.reporte_text.set(reporte)

        self._graficar()

    # =========================
    # GRÁFICOS
    # =========================
    def _limpiar_graficas(self):
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

    def _graficar(self):

        m = self.metricas
        self._limpiar_graficas()

        # Histograma temperatura
        self.ax1.set_title("Distribución Temperatura")
        self.ax1.hist(m["temperaturas"], bins=12)

        # Serie CPU
        self.ax2.set_title("CPU por Servidor")
        self.ax2.plot(range(1, len(m["cpus"]) + 1), m["cpus"])

        # Barras estado
        self.ax3.set_title("Estados del Sistema")
        self.ax3.bar(
            ["OK", "Advertencia", "Crítico", "Exceso"],
            [m["ok"], m["adv"], m["crit"], m["exceso"]]
        )

        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    app = App()
    app.mainloop()