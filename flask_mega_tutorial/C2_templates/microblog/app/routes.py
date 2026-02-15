# данный модуль относится к представлению (view)
from flask import render_template

from flask_mega_tutorial.C2_templates.microblog.app import appObj

@appObj.route('/')
@appObj.route('/simple_page')
def simpleHandler():  # в данном случае шаблон страницы вписан внутри функции просмотра. Так делать не рекомендуется
    user = {'username': 'Miguel'}
    return '''
      <html>
        <head>
          <title>Home Page - Microblog</title>
        </head>
        <body>
          <h1>Hello, ''' + user['username'] + '''!</h1>
        </body>
      </html>'''


@appObj.route('/page_with_template')
def handleTemplate():  # в данном случае шаблон прописан отдельно. В теле функции просмотра шаблон подключается с
                            # помощью функции render_template
    user = {'username': 'Irakli'}
    return render_template('index.html', title='Home', user=user)  # функция render_template делает
                            # рендеринг (преобразует шаблон в HTML-страницу). Эта функция принимает имя файла шаблона и
                            # переменный список аргументов шаблона и возвращает тот же шаблон, но со всеми заполнителями
                            # в нем, замененными фактическими значениями. Функция render_template() вызывает движок
                            # шаблонов Jinja, который поставляется в комплекте с фреймворком Flask. Jinja заменяет
                            # блоки {{ ... }} соответствующими значениями, заданными аргументами, приведенными в вызове
                            # render_template()


@appObj.route('/page_with_template_if_block')
def handleIfBlock():  # шаблон для данной страницы подготовлен с использованием условного блока, если в
                                    # функции render_template не прописан параметр title, то странице будет присвоен
                                    # заголовок прописанный в шаблоне по умолчанию
    user = {'username': 'Irakli'}
    return render_template('index_if.html', user=user)  # параметр title отсутствует


@appObj.route('/page_with_template_cycle_for')
def handleLoopFor():  # здесь шаблон прописан в отдельном файле (index_loop_for.html). Функция render_template подтягивает
                        # шаблон. В шаблоне прописан цикл for и цикл выполняется в нем, переменные для цикла передаются из функции
                        # просмотра (handleLoopFor)
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool'
        },
        {
            'author': {'username': 'Jack'},
            'body': 'I prefer Avatar'
        }
    ]  # mock-объект - список, в котором каждый элемент словарь. Каждый словарь в свою очередь состоит из двух элементов
        # - author - данные об авторе сообщения, и body - текст сообщения.

    # return render_template('index_loop_for.html', title='Home', user=user, posts=posts)

    # вариант с использованием унаследованного шаблона
    return render_template('inherited_from_base.html', title='Home', user=user, posts=posts)