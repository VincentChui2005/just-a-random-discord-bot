from discord.ext import commands
from PIL import Image
import os


bot = commands.Bot(command_prefix="-")
cmd = bot.command()
attachments = []


@bot.event
async def on_ready():
    print("OK")


@bot.event
async def on_error(error):
    if isinstance(error, commands.errors.BadArgument):
        pass
    elif isinstance(error, commands.errors.CommandNotFound):
        pass


@cmd
async def dl(ctx, number:int=1):  # Download {number} attachments, no matter what format, in ascending order of time.
    global attachments
    attachments = []
    c = 1
    while len(attachments) < number:
        att = (await ctx.channel.history(limit=c).flatten())[-1].attachments
        att.reverse()
        attachments.extend(att)
        c += 1
    while len(attachments) > number:
        attachments.pop(-1)
    attachments.reverse()
    for i, a in enumerate(attachments):
        filename = f"files/{i+1}." + a.filename.split(".")[-1]
        await a.save(fp=filename)


@cmd
async def dlpdf(ctx, number:int=1):  # Trigger download, then pack the images into a PDF file, then delete the photos. (Might err with non-photos, not tested)
    global attachments
    await dl(ctx, number)
    filenames = [f"files/{i+1}." + a.filename.split(".")[-1] for i, a in enumerate(attachments)]
    images = [Image.open(fp).convert("RGB").transpose(Image.ROTATE_270) for fp in filenames]
    images.pop(0).save(f"files/{len(attachments)}.pdf", save_all=True, append_images=images)
    [os.remove(fp) for fp in filenames]


bot.run(open("token.txt").read())
