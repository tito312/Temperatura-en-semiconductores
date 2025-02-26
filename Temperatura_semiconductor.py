#Equipo 3. 	
#Tema del codigo: 1.6	Simulador de efectos de temperatura en semiconductores 
#Integrantes:
#Arath Jacob Gaucin Montoya.  Abraham Isaias De Leon Perez. Miguel De Jesus Guzman Tiscareño. Erick Amador Dias.
#Descripcion: Este programa simula el efecto de la temperatura en un semiconductor.
#El programa permite aumentar o disminuir la temperatura del semiconductor, verificar su estado y obtener datos de temperatura externa de una API.

############################################################################################################################################################

#Librerias utilizadas
import tkinter as tk  # Importa el módulo tkinter para crear interfaces gráficas
from tkinter import messagebox  # Importa el módulo messagebox para mostrar cuadros de mensaje
import requests  # Importa el módulo requests para hacer solicitudes HTTP
import matplotlib.pyplot as plt  # Importa matplotlib para crear gráficos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Importa FigureCanvasTkAgg para integrar gráficos en tkinter

############################################################################################################################################################

# Clase base para el semiconductor
class Semiconductor:
    def __init__(self, nombre, temperatura_actual=25):
        """
        Inicializa un objeto Semiconductor con un nombre y una temperatura inicial.
        También crea una lista para almacenar el historial de temperaturas.
        """
        self.nombre = nombre
        self.temperatura_actual = temperatura_actual
        self.historico_temperaturas = [temperatura_actual]  # Historial de temperaturas

    def aumentar_temperatura(self, incremento):
        """
        Aumenta la temperatura actual del semiconductor en una cantidad especificada.
        También agrega la nueva temperatura al historial.
        """
        self.temperatura_actual += incremento
        self.historico_temperaturas.append(self.temperatura_actual)
        return self.temperatura_actual

    def disminuir_temperatura(self, decremento):
        """
        Disminuye la temperatura actual del semiconductor en una cantidad especificada.
        También agrega la nueva temperatura al historial.
        """
        self.temperatura_actual -= decremento
        self.historico_temperaturas.append(self.temperatura_actual)
        return self.temperatura_actual

    def obtener_temperatura(self):
        """
        Devuelve la temperatura actual del semiconductor.
        """
        return self.temperatura_actual

    def obtener_historico(self):
        """
        Devuelve el historial de temperaturas del semiconductor.
        """
        return self.historico_temperaturas

############################################################################################################################################################

# Clase derivada para un tipo específico de semiconductor
class Diodo(Semiconductor):
    def __init__(self, nombre, temperatura_actual=25):
        """
        Inicializa un objeto Diodo, que es un tipo específico de Semiconductor.
        """
        super().__init__(nombre, temperatura_actual)

    def verificar_estado(self):
        """
        Verifica el estado del diodo basado en su temperatura actual.
        Devuelve un mensaje indicando si la temperatura es segura, alta o crítica.
        """
        if self.temperatura_actual > 100:
            return "Peligro: Temperatura crítica"
        elif self.temperatura_actual > 80:
            return "Advertencia: Temperatura alta"
        else:
            return "Normal: Temperatura segura"

############################################################################################################################################################

# Clase para la interfaz gráfica
class SemiconductorApp:
    def __init__(self, root):
        """
        Inicializa la aplicación de interfaz gráfica.
        Crea un objeto Diodo y configura los elementos de la interfaz.
        """
        self.root = root
        self.root.title("Simulación de Temperatura en Semiconductores")

        # Crear un objeto semiconductor
        self.semiconductor = Diodo("Diodo 1N4007")

        # Crear la interfaz gráfica
        self.label = tk.Label(root, text=f"Temperatura actual: {self.semiconductor.obtener_temperatura()}°C")
        self.label.pack(pady=10)

        self.btn_aumentar = tk.Button(root, text="Aumentar Temperatura", command=self.aumentar_temperatura)
        self.btn_aumentar.pack(pady=5)

        self.btn_disminuir = tk.Button(root, text="Disminuir Temperatura", command=self.disminuir_temperatura)
        self.btn_disminuir.pack(pady=5)

        self.btn_estado = tk.Button(root, text="Verificar Estado", command=self.verificar_estado)
        self.btn_estado.pack(pady=5)

        self.btn_obtener_datos = tk.Button(root, text="Obtener Datos Externos", command=self.obtener_datos_externos)
        self.btn_obtener_datos.pack(pady=5)

        # Crear un gráfico inicial
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(pady=10)
        self.actualizar_grafico()

    def aumentar_temperatura(self):
        """
        Aumenta la temperatura del semiconductor en 10 grados.
        Actualiza la interfaz y el gráfico.
        """
        self.semiconductor.aumentar_temperatura(10)
        self.actualizar_interfaz()
        self.actualizar_grafico()

    def disminuir_temperatura(self):
        """
        Disminuye la temperatura del semiconductor en 10 grados.
        Actualiza la interfaz y el gráfico.
        """
        self.semiconductor.disminuir_temperatura(10)
        self.actualizar_interfaz()
        self.actualizar_grafico()

    def verificar_estado(self):
        """
        Verifica el estado del semiconductor y muestra un mensaje con el resultado.
        """
        estado = self.semiconductor.verificar_estado()
        messagebox.showinfo("Estado del Semiconductor", estado)

    def actualizar_interfaz(self):
        """
        Actualiza la etiqueta de la interfaz gráfica con la temperatura actual del semiconductor.
        """
        self.label.config(text=f"Temperatura actual: {self.semiconductor.obtener_temperatura()}°C")

    def obtener_datos_externos(self):
        """
        Obtiene la temperatura externa de una API y muestra un mensaje con el resultado.
        En caso de error, muestra un mensaje de error.
        """
        try:
            # API de OpenWeatherMap
            api_key = "9c93fe0f927c4af36361afeee1d0f6f1"  # Reemplaza con tu API Key de OpenWeatherMap
            ciudad = "Mexico"  # Cambia la ciudad si lo deseas
            url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()

            # Verificar si la respuesta es válida
            if response.status_code == 200:
                temperatura_externa = data['main']['temp']
                messagebox.showinfo("Datos Externos", f"Temperatura externa en {ciudad}: {temperatura_externa}°C")
            else:
                messagebox.showerror("Error", f"No se pudo obtener la temperatura externa: {data['message']}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener la temperatura externa: {e}")

    def actualizar_grafico(self):
        """
        Actualiza el gráfico con el historial de temperaturas del semiconductor.
        """
        self.ax.clear()  # Limpiar el gráfico anterior
        historico = self.semiconductor.obtener_historico()
        self.ax.plot(historico, marker='o', linestyle='-', color='b')
        self.ax.set_title("Historial de Temperatura")
        self.ax.set_xlabel("Tiempo")
        self.ax.set_ylabel("Temperatura (°C)")
        self.ax.grid(True)
        self.canvas.draw()  # Redibujar el gráfico

# Función principal para ejecutar la aplicación
def main():
    """
    Función principal que crea la ventana principal de tkinter y ejecuta la aplicación.
    """
    root = tk.Tk()
    app = SemiconductorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

############################################################################################################################################################
# Fin del código
############################################################################################################################################################    