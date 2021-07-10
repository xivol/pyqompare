# pyqompare

An attempt to implement plagiarized code detection.
Ran out of time and ideas TBH.

Several comparators were made:
 - Bag Of Words [simple_comp/bow.py](/simple_comp/bow.py)
 - Levenstain Distance [simple_comp/levenstain.py](/simple_comp/levenstain.py)
 - Abstrax Sintax Trees [xast/comparator.py](/xast/comparator.py)
 
Interface made with PyQT5.

# RUS {🇷🇺}

Простое приложение для сравнения двух файлов на python. 
Пытается определить в них наличие плагиата.
 
### Информация для проверяющих

Проект - многострадальный. Начат еще в ноябре с желанием сдать в первую волну.
В результате, пока занимался перебором методов сравнения файлов с кодом, вышли все сроки.

Проект не претендует на 100 баллов. Был собран в работающий билд за вечер последнего дня.

Есть окно с двумя половинками, куда можно загружать текстовые .py файлы.
По нажатию кнопки `Compare` запускается проверка и подвсечиваются файлы красным или зеленым.

В проекте много неиспользуемого кода, который был создан для других типов сравнений.
~~Идея проверки на плагиат через хэширование синтаксических деревьев меня не отпускает~~

С интерфейсом пришлось помучаться: uic не хочет собирать интерфейс с внешними зависимостями, как я не пытался - гугл не помог.
Поэтому правая и левая панели генерируются в коде. 

Ещё есть файл с ресурсами, который содержит иконки приложения. При его подключении uic смотрит в текущую рабочую директорию, поэтому пришлось положить его рядом с main.

Вообще про uic можно отдельную лекцию читать - там много подводных камней.

__Как собрать проект:__

По идее все собирается само из-под PyCharm. Если нет, то нужно просто сделать 
```
pip install -r requirements.txt
python main.py
```
Есть исполняемый exe файл в папке [dist](/dist/pyqompare.exe).