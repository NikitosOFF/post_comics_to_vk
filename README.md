# Публикация комиксов
Публикация рандомного комикса с сайта [xkcd.com/](https://xkcd.com/) в вашей группе ВКонтакте

## Как установить
1. Зарегистрируйтесь на сайте [vk.com](https://vk.com/feed) . Создайте свою группу ВК и приложение 
(ссылка [https://vk.com/apps?act=manage](https://vk.com/apps?act=manage)). \
2.Получите ```client_id``` созданного приложения и сохраните его в .env ```VK_APP_CLIENT_ID=""``` \
3.Перейдите по ссылке 
https://oauth.vk.com/authorize/?client_id=YOUR_CLIENT_ID&scope=photos,groups,wall,offline&response_type=token
, где YOUR_CLIENT_ID - ваш ```client_id``` , который вы получили в прошлом шаге. В адресной строке вы увидите 
```access_token=```, сохраните его в .env ```VK_ACCESS_TOKEN=""``` \
4.Сохраните ```group_id``` в .env ```VK_GROUP_ID=""```

Python3 должен быть уже установлен. Затем используйте ```pip``` (или ```pip3```, есть конфликт с ```Python2```) для установки зависимостей:

```pip install -r requirements.txt```
### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).