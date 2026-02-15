from flask import Flask, render_template  # render_template нужно чтобы роут запускал HTML-файл


app = Flask(__name__, template_folder='templates')  # template_folder= это указание на директорию содержащую HTML-файл,
        # именно код из этого файл будет выводить ендпоинт. Эта директория должна находится в в одной с директории с
        # рабочим файлом


@app.route('/')
def index():
    variable1 = 'variable1'
    variable2 = 'variable2'
    my_list = [10, 20, 50, 40, 70, 30]
    return render_template('index.html', variable1=variable1, variable2=variable2, list=my_list)  # в риторне
            # необходимо указывать, какой файл запускается. Можно совмещать запускаемый файл вместе с переменными
            # прописанными в теле роута. Чтобы эти переменные сработали, их нужно также прописать в HTML-файле. В
            # HTML-файле название файла нужно прописывать как в риторне


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
