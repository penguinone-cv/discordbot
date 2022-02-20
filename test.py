import discord
import os
import random
import csv
import time
from spla import *
from util import *
from discord.ext import commands

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'ODYzMDM4NTgzMDY1NDExNjI0.YOhFUA.DTlIjYTzGp3Xz2ECRDXb00iaXlg'

# 起動準備
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='')

# コマンドプレフィックス
prefix = '/'

@bot.command(name=prefix+'test')
async def test(ctx):
    await ctx.send("できたやで")

@bot.command(name=prefix+'help')
async def help(ctx):
    send_message = "**ペンギノンのDiscordコンシェルジュ ヘルプメッセージです！**\n"
    send_message = send_message + "コマンド一覧\n"
    send_message = send_message + "\t詳細はリファレンス( http://www.penguinone-sandbox.net/homepage/pages/discordbot.html )を参照してください\n"
    send_message = send_message + "`/neko` 「にゃーん」と言うだけ\n"
    send_message = send_message + "`/theme`\n\t用意されている会話デッキの中から1つを抽選し、現在参加しているボイスチャンネルの参加者からランダムに1人を選び指定する\n"
    send_message = send_message + '`/req "募集タイトル"`\n\t指定したタイトルのメンバーを募集する　特定のワード指定(リファレンス参照)で少しふるまいが変わる\n'
    send_message = send_message + "`リグマ〇〇` リーグマッチの予定を表示\n"
    await ctx.send(send_message)

@bot.command(name=prefix+'theme')
async def theme(ctx, *args):
    if ctx.author.voice is None:
        await ctx.send(f"{ctx.author.mention}このコマンドを使用するにはまずボイスチャンネルに接続してください！")
        return

    server_deck_path = "./conversation_deck/" + str(ctx.guild.id) + ".csv"

    if len(args) > 0:
        if args[0] == '-make':
            # 既に存在する場合は上書きしない
            if not os.path.exists(server_deck_path):
                await ctx.send("サーバー固有会話デッキの生成を行います\nカードの追加を適宜行ってください(初期状態では何も入っていません)")
                deck = open(server_deck_path, "w")
                deck.close()

        # デッキリセット
        if args[0] == "-reset":
            await ctx.send("サーバー固有会話デッキのリセットを行います\nカードの追加を適宜行ってください(初期状態ではデフォルトデッキが入っています)")
            deck = open(server_deck_path, "w", encoding="utf-8-sig")
            default_deck = open("./conversation_deck/default.csv", "r", encoding="utf-8-sig")
            default_deck_reader = csv.reader(default_deck)
            add_data = [data for data in default_deck_reader]
            deck_writer = csv.writer(deck)
            deck_writer.writerow(add_data)
            deck.close()

        if args[0] == "-add":
            # 会話デッキを開く
            # aで追記と読み込みが可能なモードになる


bot.run(TOKEN)