from flask import Flask, render_template, request

app = Flask(__name__)

class NodoTipoCircular:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaTipoCircular:
    def __init__(self):
        self.cabeza = None

    def insertar_al_principio(self, dato):
        nuevo_nodo = NodoTipoCircular(dato)
        if self.cabeza is None:
            nuevo_nodo.siguiente = nuevo_nodo
            self.cabeza = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            nodo_actual = self.cabeza
            while nodo_actual.siguiente != self.cabeza:
                nodo_actual = nodo_actual.siguiente
            nodo_actual.siguiente = nuevo_nodo
            self.cabeza = nuevo_nodo

    def eliminar(self, dato):
        if self.cabeza is None:
            print("Lista circular vacía")
            return
        
        nombre, apellido = dato
        # Eliminar espacios en blanco al principio y al final de los nombres
        nombre = nombre.strip()
        apellido = apellido.strip()
        nodo_actual = self.cabeza
        nodo_anterior = None
        
        while True:
            if nodo_actual.dato[:2] == (nombre, apellido):
                if nodo_actual == self.cabeza:
                    while nodo_actual.siguiente != self.cabeza:
                        nodo_actual = nodo_actual.siguiente
                    nodo_actual.siguiente = self.cabeza.siguiente
                    if self.cabeza.siguiente == self.cabeza:
                        self.cabeza = None
                    else:
                        self.cabeza = self.cabeza.siguiente
                else:
                    nodo_anterior.siguiente = nodo_actual.siguiente
                del nodo_actual
                print(f"Nodo con dato {dato} eliminado")
                return
            elif nodo_actual.siguiente == self.cabeza:
                print(f"Nodo con dato {dato} no encontrado")
                return
            nodo_anterior = nodo_actual
            nodo_actual = nodo_actual.siguiente

    def buscar(self, dato):
        if self.cabeza is None:
            print("Lista circular vacía")
            return None

        nombre, apellido = dato
        # Eliminar espacios en blanco al principio y al final de los nombres
        nombre = nombre.strip()
        apellido = apellido.strip()
        nodo_actual = self.cabeza
        while True:
            if nodo_actual.dato[:2] == (nombre, apellido):
                return nodo_actual.dato
            nodo_actual = nodo_actual.siguiente
            if nodo_actual == self.cabeza:
                break
        print(f"Empleado con nombre {dato[0], dato[1]} no encontrado")
        return None

    def mostrar(self):
        empleados = []
        if self.cabeza is None:
            print("Lista circular vacía")
        else:
            nodo_actual = self.cabeza
            while True:
                empleados.append(nodo_actual.dato)
                nodo_actual = nodo_actual.siguiente
                if nodo_actual == self.cabeza:
                    break
        return empleados

# Crear una lista circular para los empleados
lista_circular = ListaTipoCircular()

@app.route('/')
def index():
    global lista_circular  
    lista_circular = ListaTipoCircular()
    return render_template('index.html')


@app.route('/acciones', methods=['GET', 'POST'])
def acciones():
    accion = request.form.get('accion')
    empleado_encontrado = None
    console_messages = []  # Inicializa la lista de mensajes de la consola
    if accion == 'buscar':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        empleado_encontrado = lista_circular.buscar((nombre, apellido))
        if empleado_encontrado:
            console_messages.append("Empleado encontrado")
        else:
            console_messages.append("Empleado encontrado")
    elif accion == 'agregar':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        salario = request.form['salario']
        lista_circular.insertar_al_principio((nombre, apellido, salario))
        console_messages.append(f"Se agregó el empleado {nombre} {apellido}")
    elif accion == 'eliminar':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        empleado_eliminado = lista_circular.eliminar((nombre, apellido))
        if empleado_eliminado:
            console_messages.append(f"Se eliminó el empleado {nombre} {apellido}")
        else:
            console_messages.append(f"No se encontró al empleado {nombre} {apellido}")
    empleados = lista_circular.mostrar() 
    return render_template('empleados.html', empleados=empleados, empleado_encontrado=empleado_encontrado, console_messages=console_messages)

if __name__ == "__main__":
    app.run(debug=True)