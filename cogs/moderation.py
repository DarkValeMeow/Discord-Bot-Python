import disnake
from disnake.ext import commands, tasks  
import subprocess
import config
import asyncio
import json

class Moderation(commands.Cog):

  def __init__(self, bot):
    self.bot = bot #Guardamos una referencia al bot
    self.bad_words = ["fresafresa", "gatogato", "rosarosa"]  #Lista de palabras prohibidas
    self.strikes = {} #Diccionario para llevar cuenta de strikes
    self.mute_role_id = 1167817963798286456 #ID del rol de mute

    self.load_strikes() #Cargamos strikes al iniciar

  def load_strikes(self):
    try:
      with open('DB/strikes.json') as f:
        self.strikes = json.load(f) #Cargamos strikes desde archivo
    except FileNotFoundError:  
      pass #Manejamos error si no existe archivo

  def save_strikes(self):
    with open('DB/strikes.json', 'w') as f:
       json.dump(self.strikes, f) #Guardamos strikes en archivo

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot:
      return #Ignoramos mensajes de bots
    
    content = message.content.lower()
        
    for word in self.bad_words:
      if word in content:
        await self.process_violation(message.author, message.channel, word) #Procesamos violación si detectamos palabra prohibida

  async def process_violation(self, member, channel, word):
    if member.id not in self.strikes: #Si no tiene strikes, lo inicializamos
      self.strikes[member.id] = 0
    
    self.strikes[member.id] += 1 #Sumamos 1 strike

    if self.strikes[member.id] == 3: #Al llegar a 3 strikes
      role = disnake.Object(id=self.mute_role_id)  #Obtenemos rol de mute  
      await member.add_roles(role) #Asignamos rol para mutear
      await channel.send(f"{member.mention} fue muteado por 1 hora.")
            
      await asyncio.sleep(3) #Esperamos 1 hora
      await member.remove_roles(role) #Quitamos rol de mute
      await channel.send("Has sido desmuteado.")  
      del self.strikes[member.id] #Reseteamos strikes

    else:
      await channel.send(f"{member.mention} has recibido {self.strikes[member.id]} strikes, ten cuidado, al llegar a 3 strikes serás muteado.")

    self.save_strikes() #Guardamos strikes
    
    async def cog_load(self):
     print("El cog moderation cargó correctamente!")
        
def setup(bot):
    bot.add_cog(Moderation(bot))