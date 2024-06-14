from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from database import crear_tabla, insertar_actualizar_producto, actualizar_producto_bd, eliminar_producto, consultar_todos_productos, calcular_costo_total

#Da la bienvenida y muestra los comandos que tiene el bot de telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    commands_list = "\n".join([
        "/insertar <nombre_producto> <cantidad_inicial> <precio> - Para añadir un nuevo producto.",
        "/actualizar <nombre_producto> <cantidad> - Para actualizar la cantidad de un producto.",
        "/borrar <nombre_producto> - Para borrar un producto del inventario.",
        "/cercaacabarse - Para saber qué producto está cerca de acabarse.",
        "/costototal - Para conocer el costo total del inventario.",
        "/listarproductos - Para ver todos los productos en el inventario."
    ])
    await update.message.reply_text(f'Bienvenida doña Rosa al inventario!\n\nLista de comandos disponibles:\n\n{commands_list}')

#Logica para que al momento de realizar el CRUD se guarde en database.py
async def insertar_producto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        nombre = context.args[0]
        cantidad_inicial = int(context.args[1])
        precio = float(context.args[2])

        if insertar_actualizar_producto(nombre, cantidad_inicial, precio):
            await update.message.reply_text(f'Producto {nombre} añadido con cantidad {cantidad_inicial} y precio {precio}.')
        else:
            await update.message.reply_text(f'Error al añadir el producto {nombre}.')
    except (IndexError, ValueError):
        await update.message.reply_text('Uso: /insertar <nombre_producto> <cantidad_inicial> <precio>')


async def actualizar_producto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        nombre = context.args[0]
        cantidad = int(context.args[1])
        precio = float(context.args[2])

        if actualizar_producto_bd(nombre, cantidad, precio):
            await update.message.reply_text(f'Producto {nombre} actualizado. Nueva cantidad: {cantidad}, nuevo precio: {precio}.')
        else:
            await update.message.reply_text(f'Error al actualizar el producto {nombre}.')
    except (IndexError, ValueError):
        await update.message.reply_text('Uso: /actualizar <nombre_producto> <cantidad> <precio>')


async def borrar_producto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        nombre = context.args[0]

        if eliminar_producto(nombre):
            await update.message.reply_text(f'Producto {nombre} borrado.')
        else:
            await update.message.reply_text(f'Error al borrar el producto {nombre}.')
    except IndexError:
        await update.message.reply_text('Uso: /borrar <nombre_producto>')


async def producto_cerca_acabarse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    productos_cerca_acabarse = []

    productos = consultar_todos_productos()

    for nombre, info in productos.items():
        if info['cantidad'] < 20:
            productos_cerca_acabarse.append(f'{nombre}: Cantidad actual {info["cantidad"]}')

    if productos_cerca_acabarse:
        mensaje = "\n".join(productos_cerca_acabarse)
        await update.message.reply_text(f'Productos cerca de acabarse:\n\n{mensaje}')
    else:
        await update.message.reply_text('No se encontraron productos cerca de acabarse.')


async def costo_total_inventario(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    costo_total = calcular_costo_total()
    await update.message.reply_text(f'El costo total del inventario es {costo_total}.')


async def listar_productos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    productos = consultar_todos_productos()

    if productos:
        lista_productos = "\n".join([
            f"{nombre}: Cantidad: {info['cantidad']}, Precio: {info['precio']}"
            for nombre, info in productos.items()
        ])
        await update.message.reply_text(f'Productos en el inventario:\n\n{lista_productos}')
    else:
        await update.message.reply_text('El inventario está vacío.')

# Crea las tabla(iniciando la bd) se agrega el token del bot, y se indican la funcionalidad de los comandos
def main() -> None:
    crear_tabla()
    token = "7427694417:AAHpt696AsIOM2g37LLfm6UWSfxQwqaliYQ"
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("insertar", insertar_producto))
    application.add_handler(CommandHandler("actualizar", actualizar_producto))
    application.add_handler(CommandHandler("borrar", borrar_producto))
    application.add_handler(CommandHandler("cercaacabarse", producto_cerca_acabarse))
    application.add_handler(CommandHandler("costototal", costo_total_inventario))
    application.add_handler(CommandHandler("listarproductos", listar_productos))

    application.run_polling()


if __name__ == '__main__':
    main()
