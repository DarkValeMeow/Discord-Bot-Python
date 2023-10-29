import disnake
from disnake.ext import commands
from disnake.ui import Button
import datetime

class Tickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot #Referencia al bot
        self.tickets = {} 
        
    @commands.command()
    async def ticket(self, ctx):
        embed = disnake.Embed(
            title=f'Crear un ticket',
            description=f'Hola, {ctx.author.mention}! ¿Deseas abrir un ticket? ¡Simplemente selecciona el tipo de ticket que deseas abrir!', 
            color=0x00ff00
        )
        embed.set_footer(text=f'Pedido por {ctx.author}', icon_url=ctx.author.avatar.url) 
        embed.set_thumbnail(url=ctx.author.avatar.url)
        
        buttons = [ #Creacion de botones
            Button(label='Dudas'),
            Button(label='Soporte')
        ]

        await ctx.send(embed=embed, components=[disnake.ui.ActionRow(*buttons)])

        res = await self.bot.wait_for('button_click') #Esperamos que elijan

        if res.component.label in ['Dudas', 'Soporte']:
            username = ctx.author.name
            ticket_type = res.component.label.lower()
            channel = await ctx.guild.create_text_channel(f'ticket-{ticket_type}-{username}') #Creamos canal

            embed = disnake.Embed(
                title='Tu ticket ha sido creado!',
                description=f'{ctx.author.mention} cuéntanos qué duda o soporte necesitas! Ve a {channel.mention}',
                color=0x00ff00,
                timestamp=datetime.datetime.now()
            )
            embed.set_footer(text=f'Pedido por by {ctx.author}', icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url=ctx.author.avatar.url)
            
            await ctx.author.send(embed=embed) #Enviamos MD al usuario

            embed = disnake.Embed(
                title=f'Bienvenido a {ctx.guild.name}, ¿en qué podemos ayudarte?',
                description=f'Gracias por contactar al soporte de {ctx.guild.name}. Por favor explica tu problema o preocupación mientras esperas a que alguien del staff venga a asistirte.',
                color=0x00ff00
            )
            embed.set_footer(text=f'Pedido {ctx.author}', icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url=ctx.author.avatar.url)
            button = Button(label="Cerrar ticket")
            
            await channel.send(embed=embed, components=[[button]]) #Enviamos mensaje en el canal

    @commands.Cog.listener()
    async def on_button_click(self, res):
        if res.component.label == 'Cerrar ticket':
            await res.channel.send('Cerrando ticket...', delete_after=5)  
            await res.channel.delete() #Cerramos ticket
            
    async def cog_load(self):
     print("El cog ticket cargó correctamente!")
     
def setup(bot):
    bot.add_cog(Tickets(bot))