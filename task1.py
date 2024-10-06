import sqlite3

from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)


class DatabaseTask:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Branch (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            custom_num INTEGER NOT NULL,
                            ar_name TEXT,
                            ar_desc TEXT,
                            en_name TEXT,
                            en_desc TEXT,
                            note TEXT,
                            address TEXT
                          )''')

        self.conn.commit()
        self.conn.close()

    def add_record(self, custom_num, ar_name, ar_desc, en_name, en_desc, note, address):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO Branch (custom_num, ar_name, ar_desc, en_name, en_desc, note, address)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (custom_num, ar_name, ar_desc, en_name, en_desc, note, address))

        self.conn.commit()
        self.conn.close()

    def edit_record(self, branch_id, custom_num, ar_name, ar_desc, en_name, en_desc, note, address):
        cursor = self.conn.cursor()

        cursor.execute('''UPDATE Branch 
                          SET custom_num = ?, ar_name = ?, ar_desc = ?, en_name = ?, en_desc = ?, note = ?, address = ?
                          WHERE id = ?''',
                       (custom_num, ar_name, ar_desc, en_name, en_desc, note, address, branch_id))

        self.conn.commit()
        self.conn.close()

    def get_all_data(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * from Branch')
        rows = cursor.fetchall()
        self.conn.close()
        return rows

    def get_data_by_id(self, branch_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Branch WHERE id = ?", (branch_id,))
        record = cursor.fetchone()
        self.conn.close()
        return record

    def get_count(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM Branch')
        count = cursor.fetchone()[0]
        self.conn.close()
        return count


with app.app_context():
    DatabaseTask().create_table()


@app.route('/')
@app.route('/<int:b_id>', methods=['GET'])
def main_route(b_id=None):
    branches_count = DatabaseTask().get_count()
    if b_id is None:
        return redirect('/1')
    else:
        record = DatabaseTask().get_data_by_id(b_id)
        if record:
            return render_template('main_screen.html',
                                   branches_count=branches_count, record=record)
        else:
            if b_id == 1:
                return render_template('main_screen.html',
                                       branches_count=0, record=None)
            return jsonify({"error": "Record not found"}), 404


@app.route('/data', methods=['POST'])
def data():
    b_id = request.json.get('id')
    record = DatabaseTask().get_data_by_id(b_id)
    return jsonify(record)


@app.route('/add', methods=['POST'])
def add_branch():
    DatabaseTask().add_record(0, '', '', '', '', '', '')
    return redirect(f'/{DatabaseTask().get_count()}')


@app.route('/edit', methods=['POST'])
def edit_branch():
    b_id = request.form['id']
    custom_num = request.form['custom_num']
    ar_name = request.form['ar_name']
    ar_desc = request.form['ar_desc']
    en_name = request.form['en_name']
    en_desc = request.form['en_desc']
    note = request.form['note']
    address = request.form['address']
    DatabaseTask().edit_record(b_id, custom_num, ar_name, ar_desc, en_name, en_desc, note, address)
    return redirect(url_for('main_route'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5051)
