from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/')
def index():
    #return "Hello World"
    return "<h1>Hello World</h1>"


@app.route('/hello')  # по умолчанию роут представляет тип запроса GET, чтобы изменить тип запроса, необходимо это
        # прописать следующим обпазом: @app.route('/hello', method=['POST']) изменен на POST-запрос. Если нужно, можно
        # прописать сразу несколько типов запросов: @app.route('/hello', method=['GET', 'POST'])
def hello():
    return 'Hello World', 200  # к возвращаемым данным можно также добавить код, например: 200 или 404
    ### создание кастомного респонса
    # resp = make_response()
    # resp.status_code = 202
    # resp.headers['content-type'] = 'application/octet-stream'
    # return resp  # для проверки запускать в терминале с флагом I


@app.route('/hi', methods=['GET', 'POST'])
def hi():
    if request.method == 'GET':  # условный блок устанавливает какому типу запрос срабатывать
        return 'you made a GET-request'
    elif request.method == 'POST':
        return 'you made a POST-request'
    else:
        return 'you made neither GET-request nor POST-request'



@app.route('/greet/<name>')  # создается ендпоинт, часть которого, name - является переменной и она передается в
    # функцию и в теле функции с ней можно выполнять манипуляции
def greet(name):
    return f'Hello {name}'


@app.route('/add/<int:number1>/<int:number2>')  # int - указывает на то, что указанные части ендпоинта являются числами
def add(number1, number2):
    return f'{number1} + {number2} = {number1 + number2}'


@app.route('/handle_url_params')  # за данной частью url можно поставить ? и за тем данные в виде ключа-значения, элементы
        # между собой должны быть разделены &
def handle_params():
    # return str(request.args)  # атрибут args представляет из себя пустой словарь
    if 'greeting' in request.args.keys() and 'name' in request.args.keys():  # проверка что соответствующие ключи для ендпоинта существуют
        greeting = request.args['greeting']  # прописываются какие ключи будут в ендпоинте, значения же этих ключей
                # прописываются в самом ендпоинте следующим образом: greeting=hi
        name = request.args['name']
        return f'{greeting}, {name}'
    else:
        return 'some parameters are missing. Check the code!'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)

"""
Для запуска этого кода в терминале:
    curl http://127.0.0.1:5555/some_endpoint
для вызова с указанием типа запроса:
    curl -X POST http://127.0.0.1:5555/some_endpoint
    если вместо или вместе с флагом X использовать I(ай) можно получить HEADER-информацию
"""