from flask import Flask, request, jsonify

# Пример класса Database
class Database:
    def __init__(self):
        # Здесь можно инициализировать соединение с базой данных
        self.data = []

    def add_pass(self, data):
        # Здесь можно добавить логику для добавления данных в базу данных
        self.data.append(data)  # Добавление данных в список для примера
        return len(self.data)  # Возврат ID, который равен длине списка


app = Flask(__name__)
db = Database()


@app.route('/submitData', methods=['POST'])
def submit_data():
    data = request.json
    required_fields = ['beauty_title', 'title', 'user', 'coords', 'level', 'images']

    # Проверка на наличие необходимых полей
    for field in required_fields:
        if field not in data:
            return jsonify({"status": 400, "message": f"Missing field: {field}", "id": None}), 400

    try:
        # Добавление нового перевала в базу данных
        pass_id = db.add_pass(data)
        return jsonify({"status": 200, "message": None, "id": pass_id}), 200
    except Exception as e:
        return jsonify({"status": 500, "message": str(e), "id": None}), 500


if __name__ == '__main__':
    app.run(debug=True)

