from flask import Flask
appObj = Flask(__name__)  # Переменная __name__ , передаваемая классу Flask, является предопределенной переменной Python,
                            # которой присваивается имя модуля, в котором она используется

from flask_mega_tutorial.C1_first_app.microblog.app import routes  # модуль routes импортируется внизу, а не сверху как в большинстве
                                                        # случаев, чтобы избежать циклический импорт
