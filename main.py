import discord
import random
import string
from discord.ui import Button, View
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import pytz
import os
from threading import Thread  # เพิ่มการนำเข้า Thread เพื่อใช้งานกับ server_no

# ฟังก์ชัน server_no ที่คุณสร้างไว้เอง
def server_no():
    t = Thread(target=reu)  # ใช้ target=reu แทน Tarhrt=run
    t.start()

# ฟังก์ชันการเริ่มเซิร์ฟเวอร์
def reu():
    app.run(host='0.0.0.0', port=8080)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

MYGUILD = discord.Object(id=1320391859322753075)  # ใส่ ID เซิร์ฟเวอร์ของคุณที่นี่

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MYGUILD)
        await self.tree.sync(guild=MYGUILD)

intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Streaming(name='ระบบปลอมสลิปวอเล็ท', url='https://www.twitch.tv/toey.monifire'))

class slipwallet_discord(discord.ui.Modal, title="SLIPWALLET"):
    name_user = discord.ui.TextInput(label="USERNAME", placeholder="ชื่อผู้โอนจ่าย", required=True, max_length=50, style=discord.TextStyle.short)
    name_me = discord.ui.TextInput(label="NAME", placeholder="ชื่อผู้รับเงิน", required=True, max_length=50, style=discord.TextStyle.short)
    phone_me = discord.ui.TextInput(label="PHONE", placeholder="เบอร์โทรศัพท์ผู้รับ", required=True, max_length=10, style=discord.TextStyle.short)
    money = discord.ui.TextInput(label="MONEY", placeholder="จำนวนเงิน", required=True, max_length=4, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        name_user_id = self.name_user.value 
        name_me_id = self.name_me.value
        phone_me_id = self.phone_me.value
        money_id = self.money.value

        # สร้างหมายเลขการทำธุรกรรมแบบสุ่ม (Transaction ID)
        transaction_id = ''.join(random.choices(string.digits, k=16))

        thailand_timezone = pytz.timezone('Asia/Bangkok')
        current_time_thailand = datetime.now(thailand_timezone)  # แก้ไขจาก datetime.datetime.now()
        time = current_time_thailand.strftime("%H:%M:%S")
        day = current_time_thailand.strftime("%d")
        month = current_time_thailand.strftime("%m")
        year = current_time_thailand.strftime("%Y")

        image = Image.open("truemoney.png")
        draw = ImageDraw.Draw(image)

        font_size_money = 87
        font_size_user = 48
        font_size_me = 48
        font_size_phone = 47
        font_size_time = 46
        font_size_order = 46  # ขนาดฟอนต์สำหรับหมายเลขการทำธุรกรรม

        font_path_money = "Lato-Heavy.ttf"
        font_path_user = "Kanit-ExtraLight.ttf"

        font_money = ImageFont.truetype(font_path_money, font_size_money)
        font_user = ImageFont.truetype(font_path_user, font_size_user)
        font_me = ImageFont.truetype(font_path_user, font_size_me)
        font_phone = ImageFont.truetype(font_path_user, font_size_phone)
        font_time = ImageFont.truetype(font_path_user, font_size_time)
        font_order = ImageFont.truetype(font_path_user, font_size_order)

        phone = phone_me_id
        text_money = f"{money_id}.00"
        text_name_user = name_user_id
        text_name_me = name_me_id
        text_name_phone = f"{phone[:3]}-xxx-{phone[6:]}"
        text_name_time = f"{day}/{month}/{year} {time}"
        text_name_order = transaction_id  # แสดงหมายเลขการทำธุรกรรมที่นี่

        text_position_money = (560, 270)
        text_position_user = (302, 485)
        text_position_me = (302, 648)
        text_position_phone = (302, 720)
        text_position_time = (690, 880)
        text_position_order = (772, 945)

        text_color_money = (44, 44, 44)
        text_color_user = (0, 0, 0)
        text_color_me = (0, 0, 0)
        text_color_phone = (80, 80, 80)
        text_color_time = (45, 45, 45)
        text_color_order = (45, 45, 45)  # สีของหมายเลขการทำธุรกรรม

        draw.text(text_position_money, text_money, font=font_money, fill=text_color_money)
        draw.text(text_position_user, text_name_user, font=font_user, fill=text_color_user)
        draw.text(text_position_me, text_name_me, font=font_me, fill=text_color_me)
        draw.text(text_position_phone, text_name_phone, font=font_phone, fill=text_color_phone)
        draw.text(text_position_time, text_name_time, font=font_time, fill=text_color_time)
        draw.text(text_position_order, text_name_order, font=font_order, fill=text_color_order)

        image.save("truemoney_with_text.png")
        
        file = discord.File('truemoney_with_text.png')

        # ส่งรูปไปยัง DM ของผู้ใช้
        user = interaction.user
        try:
            await user.send(file=file)
            await interaction.response.send_message("สลิปวอเล็ทของคุณถูกส่งไปยัง DM เรียบร้อยแล้ว!", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("ไม่สามารถส่ง DM ได้ กรุณาตรวจสอบการตั้งค่าความเป็นส่วนตัวของคุณ", ephemeral=True)

@client.tree.command(description="ปลอมสลิปทรูมันนี่วอเล็ท")
async def slip_wallet(interaction: discord.Interaction):
    guild_server = interaction.guild.icon.url
    username = interaction.user.name
    button = Button(label="สลิปวอเล็ท", style=discord.ButtonStyle.grey, emoji="📃")

    async def button_callback(interaction: discord.Interaction):
        await interaction.response.send_modal(slipwallet_discord())

    button.callback = button_callback
    view = View(timeout=None)
    view.add_item(button)

    embed = discord.Embed(title="\nSLIPWALLET", description=f"**บริการปลอมสลิปวอเล็ท !**", color=0x000000)
    embed.set_author(name=username, icon_url=guild_server, url="https://discord.com/channels/@me/" + username)
    embed.add_field(name="- 📄 __EXAMPLE ( ตัวอย่าง )__", value="กรอกข้อมูลปลอมเเปลงที่คุณต้องการที่จะกรอกลงไหนช่องกรอก ผู้ใช้จ่ายเงิน,ผู้รับเงิน,เบอร์ผู้รับเงิน,จำนวนเงิน\nเวลากรอกชื่อให้เว้นวรรคชื่อเเละนามสกุลของคุณด้วย ", inline=False)
    embed.set_image(url="https://images-ext-1.discordapp.net/external/4xDKAnuLeOoeFUhHfaFgDap5SgjCx_SlpQdtjMAPhqU/https/media.giphy.com/media/fecTAVKVVA2fSzg21J/giphy.gif")
    await interaction.response.send_message(embed=embed, view=view)

# เรียกใช้ server_no() ที่คุณสร้างเอง
server_no() 

client.run(os.getenv('TOKEN'))
