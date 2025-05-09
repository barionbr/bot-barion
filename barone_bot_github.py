
from datetime import datetime
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import random

# Substitua pelo seu token do Bot do Telegram
TOKEN = 'COLE_SEU_TOKEN_AQUI'

# Dicionário para armazenar os números de cada usuário
usuarios = {}

# Comando /add para registrar números
def adicionar(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    numeros = [n for n in context.args if n.isdigit()]

    if not numeros:
        update.message.reply_text("Envie números válidos após o comando, separados por espaço.")
        return

    if chat_id not in usuarios:
        usuarios[chat_id] = set()

    usuarios[chat_id].update(numeros)
    update.message.reply_text(f"Números salvos: {', '.join(numeros)}")

# Comando /sortear para gerar um número aleatório e verificar
def sortear(update: Update, context: CallbackContext):
    sorteado = str(random.randint(1000000, 9999999))
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    chat_id = update.effective_chat.id

    if chat_id in usuarios and sorteado in usuarios[chat_id]:
        msg = f"{data_hora}\nNúmero sorteado: {sorteado}\nVocê ganhou!"
    else:
        msg = f"{data_hora}\nNúmero sorteado: {sorteado}\nNão foi dessa vez."

    update.message.reply_text(msg)

# Comando /meusnumeros para mostrar os números do usuário
def meus_numeros(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id in usuarios:
        numeros = ', '.join(sorted(usuarios[chat_id]))
        update.message.reply_text(f"Seus números: {numeros}")
    else:
        update.message.reply_text("Você ainda não cadastrou números. Use /add seguido dos seus números.")

# Inicializa o bot
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("add", adicionar))
    dp.add_handler(CommandHandler("sortear", sortear))
    dp.add_handler(CommandHandler("meusnumeros", meus_numeros))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
