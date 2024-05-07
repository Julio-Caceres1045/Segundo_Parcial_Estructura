class Nodo:
    def __init__(self, pregunta, izquierda=None, derecha=None): # aca construimos la clase nodo
        self.pregunta = pregunta
        self.izquierda = izquierda
        self.derecha = derecha

def jugar(juego): # Aca es donde se llevara a cabo el juego
    nodo_actual = juego
    while True:
        respuesta = input(nodo_actual.pregunta + " (si/no): ").lower()
        if respuesta == "si":
            print("¡He adivinado!")
            break
        elif respuesta == "no":
            if nodo_actual.derecha:
                nodo_actual = nodo_actual.derecha
            else:
                objeto = input("¡No he adivinado! ¿En qué estabas pensando? ")
                pregunta_distintiva = input("Dame una pregunta que distinga {} de {}: ".format(objeto, nodo_actual.pregunta))
                respuesta_nueva = input("¿Cuál es la respuesta para {}? (si/no): ".format(pregunta_distintiva))
                nodo_nuevo = Nodo(pregunta_distintiva)
                if respuesta_nueva == "si":
                    nodo_nuevo.izquierda = Nodo(objeto)
                    nodo_nuevo.derecha = Nodo("¿Es un mamífero?")
                else:
                    nodo_nuevo.izquierda = Nodo("¿Es un mamífero?")
                    nodo_nuevo.derecha = Nodo(objeto)
                if nodo_actual == juego:
                    juego = nodo_nuevo
                else:
                    padre = buscar_padre(juego, nodo_actual)
                    if padre.izquierda == nodo_actual:
                        padre.izquierda = nodo_nuevo
                    else:
                        padre.derecha = nodo_nuevo
                print("¡Gracias por enseñarme!")
                break
        else:
            print("Respuesta inválida. Por favor responde si o no.")

    return juego

def buscar_padre(raiz, nodo): # Aca buscara un padre para el arbol
    if raiz.izquierda == nodo or raiz.derecha == nodo:
        return raiz
    if raiz.izquierda:
        padre = buscar_padre(raiz.izquierda, nodo)
        if padre:
            return padre
    if raiz.derecha:
        padre = buscar_padre(raiz.derecha, nodo)
        if padre:
            return padre

def exportar_arbol_dot(raiz, archivo): # Aca es la base para el archivo exportado
    with open(archivo, 'w') as f:
        f.write("digraph Arbol {\n")
        exportar_nodo_dot(raiz, f)
        f.write("}\n")

def exportar_nodo_dot(nodo, f):
    if nodo.izquierda:
        f.write('"{0}" -> "{1}" [label="si"];\n'.format(nodo.pregunta, nodo.izquierda.pregunta))
        exportar_nodo_dot(nodo.izquierda, f)
    if nodo.derecha:
        pregunta_distintiva = nodo.pregunta.replace("¿Es ", "").replace("?", "").replace(" un", "").capitalize()
        if nodo.derecha.pregunta != "¿Es un mamífero?":
            f.write('"{0}" -> "{1}" [label="no"];\n'.format(nodo.pregunta, pregunta_distintiva))
            exportar_nodo_dot(nodo.derecha, f)

def exportar_ordenes_arbol(raiz, archivo): # Esta es la  que exporta los recorridos
    with open(archivo, 'w') as f:
        f.write("Recorrido Preorder:\n")
        preorder_texto(raiz, f)
        f.write("\nRecorrido Inorder:\n")
        inorder_texto(raiz, f)
        f.write("\nRecorrido Postorder:\n")
        postorder_texto(raiz, f)

# Aca se muestran los 3 ordenes
def preorder_texto(raiz, f):
    if raiz:
        f.write(raiz.pregunta + "\n")
        preorder_texto(raiz.izquierda, f)
        preorder_texto(raiz.derecha, f)

def inorder_texto(raiz, f):
    if raiz:
        inorder_texto(raiz.izquierda, f)
        f.write(raiz.pregunta + "\n")
        inorder_texto(raiz.derecha, f)

def postorder_texto(raiz, f):
    if raiz:
        postorder_texto(raiz.izquierda, f)
        postorder_texto(raiz.derecha, f)
        f.write(raiz.pregunta + "\n")

# Aquí comienza el juego
print("Bienvenido al juego de adivinanzas!")

juego = Nodo("¿Es un mamífero?")

while True:
    juego = jugar(juego)
    opcion = input("¿Quieres jugar de nuevo? (si/no): ").lower()
    if opcion != "si":
        break


archivo_dot = "arbol.dot"
exportar_arbol_dot(juego, archivo_dot) # Exporta el arbol generado
print("El árbol se ha exportado correctamente en formato DOT.")

archivo_ordenes = "ordenes_arbol.txt"
exportar_ordenes_arbol(juego, archivo_ordenes) # Aca exporta los recorridos
print("El árbol se han exportado correctamente en el archivo 'ordenes_arbol.txt'.")
