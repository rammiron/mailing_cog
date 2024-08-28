from .mailing_cog import MailingCog


def setup(bot):
    bot.add_cog(MailingCog(bot))
