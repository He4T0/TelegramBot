 admin =  """
  Полный список команд:
        
        Отправка сообщений
        /all [msg] - разослать всем пользователям из своей группы сообщение
        /mult [msg] - разослать сообщения всем пользователям УЦ Мультидвижок
        /penta [msg] - разослать сообщения всем пользователям УЦ Pentaschool
        /psy [msg] - разослать сообщения всем пользователям УЦ PSY
        /spo [msg] - разослать сообщения всем пользователям в подписанным на ОСЭК
        Работа с подписками 
        /out_subscr - посмотреть свои подписки
        /subscribe - подписаться на рассылки
        /unsubscribe - отписаться от рассыл0чки
        Другое
        /leave - покинуть группу
        /help - вывод справки
        /change_group - сменить группу
        """

general = """
        Полный список команд:
        *Отправка сообщений*
        /all [msg] - разослать всем пользователям из своей группы сообщение
        /mult [msg] - разослать сообщения всем пользователям УЦ Мультидвижок
        /penta [msg] - разослать сообщения всем пользователям УЦ Pentaschool
        /psy [msg] - разослать сообщения всем пользователям УЦ PSY
        /spo [msg] - разослать сообщения всем пользователям в подписанным на ОСЭК
        Вы можете отправлять текст, изображение, видео. При отправке всех видов сообщений должна быть введена любая из вышеперечисленных команд
        *Работа с подписками*
        /subscribe - подписаться на рассылки
        /out_subscr - посмотреть свои подписки
        /unsubscribe - отписаться от рассылки
      
       *Другое*
        /start - активировать чат-бота
        /help - вывод справки
        /rules - правила бойцовского клуба
        /leave - покинуть группу
        /users - посмотреть всех пользователей в моей группе
        """

guest= """
        Полный список команд:
        /start - активировать чат-бота
        /help - вывод справки
        /enstance [pswd]- вход
        """

dick_help = {'0':admin, '1':general, '2':general, '3':guest}