import discord
import datetime
import psutil
import platform
import requests
from discord.ext import commands
from discord import app_commands

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

start_time = datetime.datetime.now()

@bot.event
async def on_ready():
    print('bot is running!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("SERVER"))
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    await channel.send(f"welcome {member.mention}")

@bot.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    await channel.send(f"goodbye {member.mention}")


@bot.tree.command(name="ping", description="show latency")
async def self(interaction: discord.Interaction):
    # Create an embed object
    embed = discord.Embed(title='Pong!', color=0x00ff00)
    embed.add_field(name='Latency', value=f"{round(bot.latency * 1000)}ms", inline=True)

    # Send the embed to the channel
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="uptime", description="show bot's uptime")
async def self(interaction: discord.Interaction):
    # Calculate the elapsed time
    elapsed_time = datetime.datetime.now() - start_time

    # Format the elapsed time into a human-readable string
    elapsed_time_str = str(elapsed_time).split('.')[0]

    # Create an embed object
    embed = discord.Embed(title='Uptime', color=0x00ff00)
    embed.add_field(name='Elapsed Time', value=elapsed_time_str, inline=True)

    # Send the embed to the channel
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="info", description="show system info")
async def self(interaction: discord.Interaction):
    # Get system information using psutil
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent

    # Get the CPU temperature using psutil
    # cpu_temp = psutil.sensors_temperatures()['cpu-thermal'][0].current

    # Create an embed object
    embed = discord.Embed(title='System Information', color=0x00ff00)
    embed.add_field(name='CPU Usage', value=f'{cpu_percent}%', inline=True)
    embed.add_field(name='Memory Usage', value=f'{memory_percent}%', inline=True)
    embed.add_field(name='Disk Usage', value=f'{disk_percent}%', inline=True)
    # embed.add_field(name='CPU Temperature', value=f'{cpu_temp:.1f}°C', inline=True)

    # Send the embed to the channel
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="spec", description="show system spec")
async def self(interaction: discord.Interaction):
    # Get system information using platform and psutil
    operating_system = platform.system()
    processor = platform.processor()
    memory = psutil.virtual_memory().total // (1024**2)  # Convert bytes to megabytes
    disk = psutil.disk_usage('/').total // (1024**2)  # Convert bytes to gigabytes

    # Create an embed object
    embed = discord.Embed(title='System Specifications', color=0x00ff00)
    embed.add_field(name='Operating System', value=operating_system, inline=True)
    embed.add_field(name='Processor', value=processor, inline=True)
    embed.add_field(name='Memory', value=f'{memory} MB', inline=True)
    embed.add_field(name='Disk', value=f'{disk} GB', inline=True)

    # Send the embed to the channel
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="weather", description="shows weather")
async def self(interaction: discord.Interaction, location:str):
    print(location)
    # Retrieve the current weather conditions and temperature using the OpenWeatherMap API
    api_key = 'YOUR API KEY'
    api_url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}'
    response = requests.get(api_url)
    data = response.json()
    print(data)

    # Extract the necessary information from the API response
    conditions = data['weather'][0]['description']
    temperature = data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
    temperature = round(temperature, 1)  # Round to one decimal place
    city = data['name']

    # Create an embed object
    embed = discord.Embed(title=f'Weather for {city}', color=0x00ff00)
    embed.add_field(name='Conditions', value=conditions, inline=True)
    embed.add_field(name='Temperature', value=f'{temperature}°C', inline=True)

    # Send the embed to the channel
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="time", description="shows time")
async def self(interaction: discord.Interaction, location:str):
    # Make a request to the TimeZoneDB API to get the timezone for the specified location
    API_KEY = "YOUR API KEY"
    r = requests.get(f"http://api.timezonedb.com/v2.1/get-time-zone?key={API_KEY}&format=json&by=zone&zone={location}")
    data = r.json()
    print(data)

    # Check if the request was successful
    if data['status'] == 'OK':
        # Extract the time and timezone from the API response
        time = data['formatted']
        timezone = data['zoneName']

        # Create an embed message with the time and timezone information
        embed = discord.Embed(title=f"Time in {location}:", description=f"{time}\n{timezone}", color=0x00ff00)
        await interaction.response.send_message(embed=embed)
    else:
        # If the request was not successful, send an error message
        embed = discord.Embed(title=f"Time", description=f"Sorry, I couldn't find the time for that location.", color=0x00ff00)
        await interaction.response.send_message(embed=embed)


bot.run('YOUR TOKEN')


