class Libro:

    def __init__(self, titulo, autor, paginas):
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas
        self.disponible = True

    def prestar(self):
        if self.disponible:
            self.disponible = False
            return f"El libro '{self.titulo}' ha sido prestado."
        else:
            return f"El libro '{self.titulo}' ya está prestado."

    def devolver(self):
        self.disponible = True
        return f"El libro '{self.titulo}' ha sido devuelto."

    def estado(self):
        if self.disponible:
            return "Disponible"
        else:
            return "Prestado"


# Crear libros
libro1 = Libro("Cien años de soledad", "Gabriel García Márquez", 417)
libro2 = Libro("El principito", "Antoine de Saint-Exupéry", 96)

# Uso del sistema
print(libro1.estado())
print(libro1.prestar())
print(libro1.estado())
print(libro1.devolver())

print("\n---")

print(libro2.estado())