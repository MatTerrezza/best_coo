import threading
import bot


if __name__ == "__main__":
    # Запуск бота в отдельном потоке
    bot_thread = threading.Thread(target=bot.run_bot)
    bot_thread.start()

    # Можно также запустить main напрямую, если нужно
    # main.main()
