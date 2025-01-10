import os
import discord
from discord.ext import commands

from myserver import server_on



#ปิดใช้งาน Intents
intents = discord.Intents.default()
intents.members = True  # เปิดการติดตามสมาชิก
intents.voice_states = True  # เปิดการติดตามสถานะห้องเสียง

#สร้าง Client ของบอท
bot = commands.Bot(command_prefix="!", intents=intents)

#แจ้งเมื่อบอทพร้อมทำงาน
@bot.event
async def on_ready():
    print(f"บอท {bot.user} พร้อมทำงานแล้ว!")

#แจ้งเตือนเมื่อมีคนเข้า/ออกห้องเสียง
@bot.event
async def on_voice_state_update(member, before, after):
    # ตั้งค่าช่องข้อความที่ใช้แจ้งเตือน
    channel = discord.utils.get(member.guild.text_channels, name="୧⚡•เช็คคนเข้าออกห้องˎˊ˗")  # เปลี่ยน "general" เป็นชื่อห้องที่ต้องการ

    # ตรวจสอบว่าช่องข้อความมีอยู่
    if channel is None:
        print("ไม่พบช่องข้อความที่ระบุ")
        return

    # กรณีเข้าห้องเสียง
    if before.channel is None and after.channel is not None:
        embed = discord.Embed(
            title="🎙️ เข้าห้องเสียง",
            description=f"{member.mention} ได้เข้าห้องเสียง {after.channel.name}",
            color=discord.Color.green()
        )
        await channel.send(embed=embed)

    # กรณีออกจากห้องเสียง
    elif before.channel is not None and after.channel is None:
        embed = discord.Embed(
            title="🎧 ออกจากห้องเสียง",
            description=f"{member.mention} ได้ออกจากห้องเสียง {before.channel.name}",
            color=discord.Color.red()
        )
        await channel.send(embed=embed)

    # กรณีย้ายห้องเสียง
    elif before.channel != after.channel:
        embed = discord.Embed(
            title="🔄 ย้ายห้องเสียง",
            description=f"{member.mention} ได้ย้ายจากห้อง {before.channel.name} ไปยัง {after.channel.name}",
            color=discord.Color.blue()
        )
        await channel.send(embed=embed)


server_on()

bot.run(os.getenv('TOKEN'))

