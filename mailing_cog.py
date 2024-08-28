import asyncio
import discord
from discord.ext import commands
from discord.commands import Option


class MailingCog(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.slash_command(name="notify_role", description="Уведомить участников с заданной ролью.")
    async def notify_role(self, ctx: discord.ApplicationContext,
                          message_text: Option(str, description="Текст сообщения рассылки."),
                          role: Option(discord.Role, description="Роль, участников с которой добавить к рассылке.")):
        members = ctx.guild.members
        notifyted_members = ""
        for member in members:
            if role not in member.roles:
                continue
            await member.create_dm()
            notifyted_members += member.display_name + "\n"
            await member.send(message_text)
        await ctx.respond(f"Готово, сообщение отосланы:\n {notifyted_members}", ephemeral=True)

    @commands.slash_command(name="notify_with_subscribe", description="Уведомить подписавшихся "
                                                                      "участников через определенное время.")
    async def notify_with_subscribe(self, ctx: discord.ApplicationContext, message_to_subscribe:
    Option(str, description="Сообщение для подписки на рассылку."),
                                    message_to_member: Option(str, description="Сообщение рассылки."),
                                    channel: Option(discord.TextChannel,
                                                    description="Канал для сообщения подписки на рассылку."),
                                    time_to_notify: Option(float, description="Время до рассылки.")):

        message = await channel.send(message_to_subscribe)
        await ctx.respond("Успешно. Рассылка объявлена.", ephemeral=True)
        subscribers = set()
        await message.add_reaction("➕")
        reactions = (await channel.fetch_message(message.id)).reactions
        reaction = None
        await asyncio.sleep(time_to_notify)
        for react in reactions:
            if react.emoji == "➕":
                reaction = react
                break
        if reaction is not None:
            async for user in reaction.users():
                subscribers.add(user)
            for subscriber in subscribers:
                try:
                    await subscriber.create_dm()
                    channel = subscriber.dm_channel
                    await channel.send(
                        f"**Вы были подписаны на уведомление. Текст уведомления:** \n{message_to_member}\n")
                except:
                    pass
            await message.clear_reactions()

