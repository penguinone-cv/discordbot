#!/usr/bin/env python
# coding: utf-8
# インストールした discord.py を読み込む
import discord
import os
import random
import csv
import time
from spla import *
from util import *

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'ODYzMDM4NTgzMDY1NDExNjI0.YOhFUA.DTlIjYTzGp3Xz2ECRDXb00iaXlg'

# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # コマンド解析
    command = full_half_translate(message.content).split()

    # 「/neko」と発言したら「にゃーん」が返る処理
    if command[0] == '/neko' and len(command) == 1:
        await message.channel.send('にゃーん')

    if command[0] == 'RF' and len(command) == 1:
        await message.channel.send(f"{message.author.mention}がんばれー")
    
    if command[0] == 'FB' and len(command) == 1:
        await message.channel.send(f"{message.author.mention}がんばれー")

    # ヘルプメッセージを表示
    if message.content == '/help' and len(command) == 1:
        send_message = "**ペンギノンのDiscordコンシェルジュ ヘルプメッセージです！**\n"
        send_message = send_message + "コマンド一覧\n"
        send_message = send_message + "\t詳細はリファレンス( http://www.penguinone-sandbox.net/homepage/pages/discordbot.html )を参照してください\n"
        send_message = send_message + "`/neko` 「にゃーん」と言うだけ\n"
        send_message = send_message + "`/theme`\n\t用意されている会話デッキの中から1つを抽選し、現在参加しているボイスチャンネルの参加者からランダムに1人を選び指定する\n"
        send_message = send_message + '`/req "募集タイトル"`\n\t指定したタイトルのメンバーを募集する　特定のワード指定(リファレンス参照)で少しふるまいが変わる\n'
        send_message = send_message + "`リグマ〇〇` リーグマッチの予定を表示\n"
        await message.channel.send(send_message)

    # 会話デッキとしゃべる人を抽選
    if "/theme" == command[0]:
        # コマンド入力者がボイスチャンネルに接続していなかったらリジェクト
        if message.author.voice is None:
            await message.channel.send(f"{message.author.mention}このコマンドを使用するにはまずボイスチャンネルに接続してください！")
            return

        # サーバー固有の会話デッキのパス
        server_deck_path = "./conversation_deck/" + str(message.guild.id) + ".csv"

        # サーバー固有会話デッキの生成
        if len(command) > 1:
            if "-make" == command[1]:
                # 既に存在する場合は上書きしない
                if not os.path.exists(server_deck_path):
                    await message.channel.send("サーバー固有会話デッキの生成を行います\nカードの追加を適宜行ってください(初期状態では何も入っていません)")
                    deck = open(server_deck_path, "w")
                    deck.close()

            # デッキリセット
            if "-reset" == command[1]:
                await message.channel.send("サーバー固有会話デッキのリセットを行います\nカードの追加を適宜行ってください(初期状態ではデフォルトデッキが入っています)")
                deck = open(server_deck_path, "w", encoding="utf-8-sig")
                default_deck = open("./conversation_deck/default.csv", "r", encoding="utf-8-sig")
                default_deck_reader = csv.reader(default_deck)
                add_data = [data for data in default_deck_reader]
                deck_writer = csv.writer(deck)
                deck_writer.writerow(add_data)
                deck.close()

            # 会話デッキにカードを追加
            if "-add" == command[1]:
                # -addの位置を探索
                add = command.index("-add")
                # 会話デッキを開く
                # aで追記と読み込みが可能なモードになる
                # encodingはutf-8-sigにすることで先頭の謎文字ロードを避ける
                deck = open(server_deck_path, "a", encoding="utf-8-sig", newline="")

                # -addの後ろに何も入力されていない場合リジェクト
                if len(command) <= add+1:
                    await message.channel.send("`-add`の後ろには追加する話題か`default`を指定してください")
                    return

                # デフォルトデッキを追加
                if command[add+1] == "default":
                    # デフォルトデッキの読み込み
                    default_deck = open("./conversation_deck/default.csv", "r", encoding="utf-8-sig")
                    default_deck_reader = csv.reader(default_deck)
                    add_data = [data for data in default_deck_reader]
                    default_deck.close()

                # -addの後ろに指定された文を追加
                else:
                    add_data = [command[add+1]]

                # 会話デッキに追記
                deck_writer = csv.writer(deck)
                deck_writer.writerow(add_data)
                deck.close()

            # 会話デッキのカードリストを表示
            if "-list" == command[1]:
                deck = open(server_deck_path, "r", encoding="utf-8-sig")
                deck_reader = csv.reader(deck)
                line = ""
                for data in deck_reader:
                    for card in data:
                        line = line + card + "\n"
                await message.channel.send("**会話デッキリスト**\n" + line)

        # サーバー固有の会話デッキがある場合はそれを使用、ない場合はデフォルトデッキを使用
        if os.path.exists(server_deck_path):
            path = server_deck_path
        else:
            path = "./conversation_deck/default.csv"

        # /themeのみが入力された場合抽選開始
        if len(command) == 1:
            deck = open(path, "r", encoding="utf-8-sig")
            deck_reader = csv.reader(deck)
            card_list = [card for card in deck_reader]
            card_list = card_list[0]
            # メッセージ送信者の参加しているボイスチャンネルに接続しているメンバーリストを取得
            guild = message.guild
            member_list = [member for member in guild.members if member.id in message.author.voice.channel.voice_states.keys()]

            await message.channel.send(f"{random.choice(member_list).mention}さんは「" + random.choice(card_list).replace("['", "").replace("']", "") + "」について話してください！")
            deck.close()

    # サモンぐーてむ
    if command[0] == "/summon":
        if message.author.voice is None:
            await message.channel.send(f"{message.author.mention}このコマンドを使用するにはまずボイスチャンネルに接続してください！")
            return

        await message.author.voice.channel.connect()

    if command[0] == "/dc":
        if message.guild.voice_client is None:
            await message.channel.send(f"{message.author.mention}どのボイスチャンネルにも接続されていませんよ？")
            return

        await message.guild.voice_client.disconnect()
    
    if command[0] == "/soundtest":
        if message.guild.voice_client is None:
            await message.channel.send(f"{message.author.mention}どのボイスチャンネルにも接続されていませんよ？")
            return
        
        message.guild.voice_client.play(discord.FFmpegPCMAudio("nc2003.mp3"))
        time.sleep(10)
        message.guild.voice_client.stop()

    # タイマーコマンド
    if command[0] == "/timer":
        # botがボイスチャンネルに接続しているか
        if message.guild.voice_client is None:
            await message.channel.send(f"{message.author.mention}どのボイスチャンネルにも接続されていませんよ？")
            return

        # 時間が指定されているか
        if len(command) == 1:
            await message.channel.send(f"{message.author.mention}時間が指定されていませんよ？")
            return
        mode = ""
        mintime = 0
        sectime = 0
        if "m" in command[1]:
            mode = "minute"
            mintime = float(re.search(r"^[0-9]+", command[1]).group())
            if float(math.floor(mintime)) < mintime:
                sectime = 60*mintime - float(math.floor(mintime))
            command[1] = re.sub(r"^[0-9]+", "", command[1])
            command[1] = command[1].replace("m", "")
        if "s" in command[1]:
            if mode == "":
                mode = "second"
            sectime = int(re.search(r"^[0-9]+", command[1]).group())
        if mode == "":
            await message.channel.send(f"{message.author.mention}時間が正しく指定されていませんよ？")
            return

        notificate_time = []
        start = 2
        if len(command) >= 3:
            if command[2] == "-s":
                start = 3
            for i in range(start, len(command)):
                n_mintime = 0
                n_sectime = 0
                if "m" in command[i]:
                    n_mintime = int(re.search(r"^[0-9]+", command[i]).group())
                    command[i] = re.sub(r"^[0-9]+", "", command[i])
                    command[i] = command[1].replace("m", "")
                if "s" in command[i]:
                    n_sectime = int(re.search(r"^[0-9]+", command[i]).group())
                notificate_time.append(n_mintime*60 + n_sectime)
            print(notificate_time)
        settime = mintime*60 + sectime
        txt= "{}：{}\n"
        revmsg = txt.format(mintime, sectime)
        msg = await message.channel.send(revmsg)
        nowtime = time.perf_counter()
        thres = 1.
        if len(command) >= 3:
            if command[2] == "-s":
                message.guild.voice_client.play(discord.FFmpegPCMAudio("Fue01.mp3"))
                time.sleep(1)
                message.guild.voice_client.stop()
        while True:
            diff = time.perf_counter() - nowtime
            if diff >= thres:
                nowtime = time.perf_counter()
                thres = 2.0 - diff
                settime = settime - 1
                if settime in notificate_time:
                    message.guild.voice_client.play(discord.FFmpegPCMAudio("hato.mp3"))
                if mode == "minute":
                    mintime = settime // 60
                    sectime = settime - mintime*60
                else:
                    sectime = settime
                await msg.edit(content = txt.format(mintime, sectime))
                if settime == 0:
                    message.guild.voice_client.play(discord.FFmpegPCMAudio("Alarm.mp3"))
                    time.sleep(5)
                    message.guild.voice_client.stop()
                    await msg.delete()
                    return

    # 募集コマンド
    if command[0] == "/req":
        await message.channel.send("募集モード" + "\t" + message.content.replace("/req", "").replace("-spla2", "").replace(" ", ""))

        if command[1] == "-spla2":
            rule, stageA_name, stageA_img, stageB_name, stageB_img, date, start_time, end_time = get_request(message.content.replace("/req", "").replace("-spla2", "").replace(" ", ""))

            #if rule == "ナワバリバトル":
            #    color = discord.Colour.from_rgb(26, 216, 26)    #ナワバリ
            #elif rule == "ガチエリア" or rule == "ガチヤグラ" or rule == "ガチホコ" or rule == "ガチアサリ":
            #    color = discord.Colour.from_rgb(246, 74, 16)    #ガチマ
            if rule == "ガチエリア" or rule == "ガチヤグラ" or rule == "ガチホコ" or rule == "ガチアサリ":
                color = discord.Colour.from_rgb(239, 46, 125)   #リグマ

            if end_time == 1:
                date_tmp = date.split("/")
                date_tmp[1] = str(int(date_tmp[1] + 1))
                end_date = date_tmp[0] + "/" + date_tmp[1]
            else:
                end_date = date
            description = date + " " + start_time + "時 ～ " + end_date + " " + end_time + "時\n"
            description = description + "\n"
            description_concat = "\n" + stageA_name + "\n" + stageB_name + "\n"

            embed = discord.Embed(title=rule, description=description+description_concat, color=color)



            # 募集人数は3人(募集者含め4人)確定(3発売後にアップデート予定)
            mcount = int(3)
            text= "あと{}人 募集中\n"
            revmsg = text.format(mcount)
            # friend_list 押した人のList
            friend_list = []
            msg = await message.channel.send(embed=embed)

            # 投票の欄
            await msg.add_reaction('\u21a9')
            await msg.add_reaction('⏫')
            await msg.add_reaction('❌')
            await msg.pin()

            while len(friend_list) < int(3):
                target_reaction = await client.wait_for("reaction_add")

                # リアクションした人と募集をかけた人が違う場合のみカウント
                if not target_reaction[1].name == message.author.name:
                    # 押された絵文字が既存の物だった場合削除
                    if target_reaction[0].emoji == '\u21a9':
                        # ⇦の絵文字が押されたらfriend_listを確認し、同じ名前があった場合リストから削除
                        if target_reaction[1].name in friend_list:
                            # リストから削除
                            friend_list.remove(target_reaction[1].name)
                            mcount += 1
                            # 表示されている参加者リストから名前を削除
                            embed = discord.Embed(title=rule, description=description + "募集中\n参加者：" + '\t'.join(friend_list) + description_concat, color=color)
                            await msg.edit(embed = embed)

                        else:
                            pass

                    elif target_reaction[0].emoji == '⏫':
                        if target_reaction[1].name in friend_list:
                            pass

                        else:
                            # リストに追加
                            friend_list.append(target_reaction[1].name)
                            mcount = mcount - 1
                            embed = discord.Embed(title=rule, description=description + "募集中\n参加者：" + '\t'.join(friend_list) + description_concat, color=color)
                            await msg.edit(embed = embed)

                elif target_reaction[0].emoji == '❌':
                    embed = discord.Embed(title=rule, description=description + "募集終了\n参加者：" + '\t'.join(friend_list) + description_concat, color=color)
                    await msg.edit(embed = embed)
                    await msg.unpin()
                    break
                await msg.remove_reaction(target_reaction[0].emoji, target_reaction[1])
            else:
                embed = discord.Embed(title=rule, description=description + "募集終了\n参加者：" + '\t'.join(friend_list) + description_concat, color=color)
                await msg.edit(embed = embed)
                await msg.unpin(msg)


        # 通常募集モード
        else:
            
            mcount = int(command[2].replace("@", ""))
            text= "あと{}人 募集中\n"
            revmsg = text.format(mcount)
            # friend_list 押した人のList
            friend_list = []
            msg = await message.channel.send(revmsg)

            # 投票の欄
            await msg.add_reaction('\u21a9')
            await msg.add_reaction('⏫')
            await msg.add_reaction('❌')
            await msg.pin()

            while len(friend_list) < int(command[2].replace("@", "")):
                target_reaction = await client.wait_for("reaction_add")#, message=msg)

                # リアクションした人と募集をかけた人が違う場合のみカウント
                #print(msg.author.name)
                if not target_reaction[1].name == message.author.name:
                    # 押された絵文字が既存の物だった場合削除
                    if target_reaction[0].emoji == '\u21a9':
                        # ⇦の絵文字が押されたらfriend_listを確認し、同じ名前があった場合リストから削除
                        if target_reaction[1].name in friend_list:
                            # リストから削除
                            friend_list.remove(target_reaction[1].name)
                            mcount += 1
                            # 表示されている参加者リストから名前を削除
                            await msg.edit(content = text.format(mcount) + '\n'.join(friend_list))

                        else:
                            pass

                    elif target_reaction[0].emoji == '⏫':
                        if target_reaction[1].name in friend_list:
                            pass

                        else:
                            # リストに追加
                            friend_list.append(target_reaction[1].name)
                            mcount = mcount - 1
                            await msg.edit(content = text.format(mcount) + '\n'.join(friend_list))

                elif target_reaction[0].emoji == '❌':
                    await msg.edit(content = '募集終了\n' + '\n'.join(friend_list))
                    await msg.unpin()
                    break
                await msg.remove_reaction(target_reaction[0].emoji, target_reaction[1])
            else:
                await msg.edit(content = '募集終了\n' + '\n'.join(friend_list))
                await msg.unpin(msg)

    if command[0] == "/sch":
        rule, stageA_name, stageA_img, stageB_name, stageB_img, date, start_time, end_time = get_request(message.content.replace("/sch", "").replace(" ", ""))
        if rule == "ナワバリバトル":
            color = discord.Colour.from_rgb(26, 216, 26)    #ナワバリ
        #elif rule == "ガチエリア" or rule == "ガチヤグラ" or rule == "ガチホコ" or rule == "ガチアサリ":
        #    color = discord.Colour.from_rgb(246, 74, 16)    #ガチマ
        elif rule == "ガチエリア" or rule == "ガチヤグラ" or rule == "ガチホコ" or rule == "ガチアサリ":
            color = discord.Colour.from_rgb(239, 46, 125)   #リグマ

        if end_time == 1:
            date_tmp = date.split("/")
            date_tmp[1] = str(int(date_tmp[1] + 1))
            end_date = date_tmp[0] + "/" + date_tmp[1]
        else:
            end_date = date
        description = date + " " + start_time + "時 ～ " + end_date + " " + end_time + "時\n"
        description = description + "\n"
        description_concat = "\n" + stageA_name + "\n" + stageB_name + "\n"

        embed = discord.Embed(title=rule, description=description+description_concat, color=color)
        await message.channel.send(embed=embed)

    if check_rule(message.content):
        rule, stageA_name, stageA_img, stageB_name, stageB_img, date, start_time, end_time = get_request(message.content[:re.search(r"[0-9]{1,2}", message.content).end()])
    #if message.content == "テスト":
    #    rule, stageA_name, stageA_img, stageB_name, stageB_img, start_time, end_time = test()
    #    await message.channel.send(rule)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)