#AvocodeARv1.1.01

###`AvocodeAR - основная программа`

#####`chromedriver.exe - основная библиотека`

####Параметры запуска:

* mail - один из сервисов (emailfake)

    * *emailfake - https://emailfake.com*					

- duration=(int) - время ожидания подтверждения регистрации (**в сек**)

- path=(string) - путь сохранения `access.txt`

- hide=(bool) - отображает окно браузера

- wfile=(bool) - отключает создание и запись в `access.txt`

- wdpath=(string) - путь до `webdriver.exe`, по умолчанию подключается из той же директории что и сама программа

####Пример:
`C:\AvocodeARv.exe hide=true path=H:\ wfile=false wdpath=C:\WebLib mail=emailfake`

#####Примечание

> После запуске программы открывается chrome, и далее работы выполняется по сценарию.

> После завершения работы полученные данные копируются в буфер.
