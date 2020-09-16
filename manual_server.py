from telegram_bot import TelegramBot


bot = TelegramBot()
update_id = None
while True:
    print('loading')
    updates = bot.check_message(offset=update_id)
    updates = updates['result']
    print(updates)
    if updates:
        for item in updates:
            update_id = item['update_id']
            try:
                msg = item['message']['text']
            except:
                msg = None
            from_ = item['message']['from']['id']
            reply = bot.make_reply(msg)

            bot.send_message(reply, from_)
