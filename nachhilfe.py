from flask import Flask, request, jsonify
from supabase import create_client, Client
import sqlite3

app = Flask(__name__)

url = "https://mtjpvnnqmnehapcvifdv.supabase.co"
publishable_key = "sb_publishable_db9KPKVXQn6IB5uqAas28Q_98UA5fXn"
 

supabase = create_client(url, publishable_key)

conn = sqlite3.connect('faecher.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS faecher
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')
conn.commit()
conn.close()

faecher = []

class Faecher:
    def __init__(self, name):
        self.name = name
        conn = sqlite3.connect('faecher.db')
        c = conn.cursor()
        c.execute("INSERT INTO faecher (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()

@app.route('/show_faecher', methods=['GET'])
def show_faecher():
    conn = sqlite3.connect('faecher.db')
    c = conn.cursor()
    c.execute("SELECT name FROM faecher")
    faecher = c.fetchall()
    conn.close()
    return {'faecher': [f[0] for f in faecher]}

@app.route('/add_fach', methods=['POST'])
def add_fach():

    data = request.get_json(force=True, silent=True)

    print(data)   # DEBUG

    if data is None or not isinstance(data, dict):
        return {'message': 'Invalid JSON received'}, 400

    name = data.get('name')

    if not name:
        return {'message': 'Name is required'}, 400

    Faecher(name)

    return {'message': 'Fach added successfully'}, 201

@app.route('/update_fach/<int:id>', methods=['PUT'])
def update_fach(id):

    data = request.get_json()

    if not data:
        return {'message': 'No JSON data provided'}, 400

    new_name = data.get('name')

    if not new_name:
        return {'message': 'New name is required'}, 400

    conn = sqlite3.connect('faecher.db')
    c = conn.cursor()

    c.execute(
        "UPDATE faecher SET name = ? WHERE id = ?",
        (new_name, id)
    )

    conn.commit()

    if c.rowcount == 0:
        conn.close()
        return {'message': 'Fach not found'}, 404

    conn.close()

    return {'message': 'Fach updated successfully'}


@app.route('/delete_fach/<int:id>', methods=['DELETE'])
def delete_fach(id):
    conn = sqlite3.connect('faecher.db')
    c = conn.cursor()

    c.execute(
        "DELETE FROM faecher WHERE id = ?",
        (id,)
    )
    conn.commit()
    if c.rowcount == 0:
        conn.close()
        return {'message': 'Fach not found'}, 404
    conn.close()
    return {'message': 'Fach deleted successfully'}
# ──────────────────────────────────────────────
# Lehrer-Routen
# ──────────────────────────────────────────────

@app.route('/lehrer_hinzufuegen', methods=['POST'])
def lehrer_hinzufuegen():
    data    = request.json
    name    = data['name']
    faecher = data['faecher']
    email   = data['email']

    response = supabase.table('lehrer').insert({
        "name":    name,
        "faecher": faecher,
        "email":   email
    }).execute()

    if response.data:
        return jsonify({"message": f"Lehrer {name} wurde hinzugefügt."}), 201
    else:
        return jsonify({"message": "Fehler beim Hinzufügen."}), 400


@app.route('/lehrer_anzeigen', methods=['GET'])
def lehrer_anzeigen():
    response = supabase.table('lehrer').select("*").execute()

    return jsonify(response.data), 200


# ──────────────────────────────────────────────
# Start
# ──────────────────────────────────────────────

if __name__ == '__main__':
    print("Starting Nachhilfe API...")
    app.run(debug=True)