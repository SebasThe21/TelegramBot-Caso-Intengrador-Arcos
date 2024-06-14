

import sqlite3

def conectar_db():
    return sqlite3.connect('inventario.db')

def crear_tabla():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventario (
            nombre TEXT PRIMARY KEY,
            cantidad INTEGER,
            precio REAL,
            cantidad_inicial INTEGER
        )
    ''')

    conn.commit()
    conn.close()

def insertar_actualizar_producto(nombre, cantidad_inicial, precio):
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO inventario (nombre, cantidad, precio, cantidad_inicial)
            VALUES (?, ?, ?, ?)
        ''', (nombre, cantidad_inicial, precio, cantidad_inicial))

        conn.commit()
        conn.close()

        return True
    except sqlite3.Error as e:
        print(f'Error al insertar o actualizar el producto: {str(e)}')
        return False


def actualizar_producto_bd(nombre, cantidad, precio):
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE inventario 
            SET cantidad = ?,
                precio = ?
            WHERE nombre = ?
        ''', (cantidad, precio, nombre))

        conn.commit()
        conn.close()

        return True
    except sqlite3.Error as e:
        print(f'Error al actualizar el producto: {str(e)}')
        return False

def eliminar_producto(nombre):
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM inventario WHERE nombre = ?
        ''', (nombre,))

        conn.commit()
        conn.close()

        return True
    except sqlite3.Error as e:
        print(f'Error al borrar el producto: {str(e)}')
        return False

def consultar_todos_productos():
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM inventario')
        productos = cursor.fetchall()

        conn.close()

        return {row[0]: {'cantidad': row[1], 'precio': row[2], 'cantidad_inicial': row[3]} for row in productos}
    except sqlite3.Error as e:
        print(f'Error al consultar todos los productos: {str(e)}')
        return {}

def calcular_costo_total():
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute('SELECT SUM(cantidad * precio) FROM inventario')
        total = cursor.fetchone()[0] or 0  

        conn.close()

        return total
    except sqlite3.Error as e:
        print(f'Error al calcular el costo total del inventario: {str(e)}')
        return 0
