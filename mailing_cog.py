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
        members = role.members
        notifyted_members = ""
        fail_notify = ""
        for member in members:
            try:
                notifyted_members += member.display_name + "\n"
                await member.send(message_text)
            except Exception as ex:
                fail_notify += member.display_name + f"Причина: {ex} " + "\n"

        await ctx.respond(f"Готово, сообщения отосланы:\n {notifyted_members}" + (
                          f"Сообщения не отосланы: {fail_notify}" if len(fail_notify) > 0 else ""), ephemeral=True)

    @commands.slash_command(name="notify_with_subscribe", description="Уведомить подписавшихся "
                                                                      "участников через определенное время.")
    async def notify_with_subscribe(self, ctx: discord.ApplicationContext, message_to_subscribe:
    Option(str, description="Сообщение для подписки на рассылку."),
                                    message_to_member: Option(str, description="Сообщение рассылки."),
                                    channel: Option(discord.TextChannel,
                                                    description="Канал для сообщения подписки на рассылку."),
                                    time_to_notify: Option(float, description="Время до рассылки в секундах.")):

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
                    channel_dm = subscriber.dm_channel
                    await channel_dm.send(
                        f"**Вы были подписаны на уведомление. Текст уведомления:** \n{message_to_member}\n")
                except:
                    pass
            await message.clear_reactions()

    @commands.slash_command(name="remindme", description="Уведомить себя через указанное время.")
    async def remindme(self, ctx: discord.ApplicationContext, message: Option(str, description="Сообщение."),
                       time: Option(float, "Время до отправки в секундах.")):
        await ctx.respond(f"Готово. Сообщение будет отослано через: {time}сек.")
        await asyncio.sleep(time)
        try:
            await ctx.author.send(message)
        except Exception as ex:
            await ctx.channel.send(f"{ctx.author.mention}, уведомление не было отослано по причине: {ex}.")
