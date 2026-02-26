import discord
from discord.ext import commands
import datetime
import yt_dlp
import random

# Intents
intents = discord.Intents.default()
intents.message_content = True

# Crear bot con prefijo $
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f'Hemos iniciado sesión como {bot.user}')

@bot.command()
async def hello(ctx):
        await ctx.send("Hola!")

@bot.command()
async def bye(ctx):
        await ctx.send("Adiós 🙂")

@bot.command()
async def como_estas(ctx):
        await ctx.send("Bien, gracias por preguntar.")

@bot.command()
async def joke(ctx):
    await ctx.send("¿Por qué los carpinteros nunca se estresan? Porque siempre encuentran una solución a mano")


@bot.command()
async def extra(ctx, category):
    if category.lower() == "joke":
        await ctx.send("¿Por qué los carpinteros nunca se estresan? Porque siempre encuentran una solución a mano")
    elif category.lower() == "adivinanza":
        await ctx.send(
            "Soy pequeño pero poderoso,\n"
            "si me olvidás todo se rompe,\n"
            "voy al final de muchas líneas\n"
            "y en algunos lenguajes soy obligatorio.\n"
            "Respuesta: El punto y coma."
        )
    else:
        await ctx.send("Actividad no reconocida. Prueba con 'joke' o 'adivinanza'.")

@bot.command()
async def time(ctx):
    now = datetime.datetime.now()
    hora = now.strftime("%H:%M:%S")
    await ctx.send(f"La hora actual es: {hora}")

@bot.command()
async def video(ctx, *, busqueda: str):
    opciones = {
        "quiet": True,
        "default_search": "ytsearch1",
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(busqueda, download=False)

        if not info or "entries" not in info or len(info["entries"]) == 0:
            await ctx.send(
                "❌ No encontré resultados 😕\n"
                "👉 Prueba con algo como:\n"
                "tutorial python desde cero\n"
                "explicación física fluidos"
            )
            return

        video = info["entries"][0]
        await ctx.send(f"🎬 **Encontré esto:**\n{video['webpage_url']}")

@bot.command()
async def ppt(ctx):
    await ctx.send("¿Piedra, papel o tijera? Escribe tu opción: 🪨 📄 ✂️")

    # Lista de opciones válidas
    opciones = ['piedra', 'papel', 'tijera']

    def check(m):
        # Verifica que sea el mismo autor y una opción válida
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in opciones

    # El bot espera la respuesta del usuario (sin tiempo límite)
    msg = await bot.wait_for('message', check=check)
    
    user_choice = msg.content.lower()
    bot_choice = random.choice(opciones)

    # Lógica de quién gana
    if user_choice == bot_choice:
        await ctx.send(f"Empate. Ambos elegimos **{bot_choice}**. 🤝")
    
    elif (user_choice == 'piedra' and bot_choice == 'tijera') or \
         (user_choice == 'papel' and bot_choice == 'piedra') or \
         (user_choice == 'tijera' and bot_choice == 'papel'):
        await ctx.send(f"¡Ganaste! Yo elegí **{bot_choice}**. 🏆")
    
    else:
        await ctx.send(f"Perdiste. Yo elegí **{bot_choice}**. 👻")

@bot.command()
async def duelo(ctx):
    await ctx.send("✨ **¡Duelo Mágico!** ✨\nElige tu movimiento: `hechizo`, `escudo` o `varita`")

    opciones = ['hechizo', 'escudo', 'varita']

    def check(m):
        return m.author == ctx.author and m.content.lower() in opciones

    msg = await bot.wait_for('message', check=check)
    user_choice = msg.content.lower()
    bot_choice = random.choice(opciones)

    # Diccionario de emojis para que se vea genial
    iconos = {'hechizo': '🔥', 'escudo': '🛡️', 'varita': '🪄'}

    if user_choice == bot_choice:
        await ctx.send(f"Los dos lanzaron {iconos[user_choice]}. ¡Los hechizos chocaron y explotaron! 💥")
    
    elif (user_choice == 'hechizo' and bot_choice == 'varita') or \
         (user_choice == 'varita' and bot_choice == 'escudo') or \
         (user_choice == 'escudo' and bot_choice == 'hechizo'):
        await ctx.send(f"Tu {iconos[user_choice]} venció a mi {iconos[bot_choice]}. ¡Eres un gran mago! 🏆")
    
    else:
        await ctx.send(f"Mi {iconos[bot_choice]} destruyó tu {iconos[user_choice]}. ¡A estudiar más magia! 🔮")

@bot.command()
async def guess(ctx):
    answer = random.randint(1, 20) # Rango actualizado a 20
    intentos = 0
    await ctx.send('He pensado un número entre **1 y 20**. ¡Intenta adivinarlo! 🧐')

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

    while True:
        guess_msg = await bot.wait_for('message', check=check)
        intentos += 1 # Sumamos un intento cada vez que responde
        guess_int = int(guess_msg.content)

        if guess_int == answer:
            await ctx.send(f'¡Felicidades! 🎉 El número era **{answer}**. Lo lograste en **{intentos}** intentos.')
            break # El 'break' detiene el bucle cuando acierta
        elif guess_int < answer:
            await ctx.send('Es **mayor**... ¡Sigue intentando! ⬆️')
        else:
            await ctx.send('Es **menor**... ¡Casi lo tienes! ⬇️')

