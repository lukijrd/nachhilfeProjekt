from flask import Flask, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

SUPABASE_URL= "https://mtjpvnnqmnehapcvifdv.supabase.co"
SUPABASE_KEY= "sb_publishable_db9KPKVXQn6IB5uqAas28Q_98UA5fXn"
url = "https://mtjpvnnqmnehapcvifdv.supabase.co"
publishable_key = "sb_publishable_db9KPKVXQn6IB5uqAas28Q_98UA5fXn"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/schueler', methods=['GET'])
def get_schueler():
    schueler = supabase.table('schueler').select('*').execute()
    return jsonify(schueler.data)

@app.route('/schueler', methods=['POST'])
def add_schueler():
    data = request.get_json()
    name = data.get('name')
    geburtsdatum = data.get('geburtsdatum')
    email = data.get('email')
    faecher = data.get('faecher')

    if not name or not geburtsdatum or not email or not faecher:
        return jsonify({'error': 'Name, Geburtsdatum, E-Mail und Fächer sind erforderlich'}), 400

    new_schueler = {
        'name': name,
        'geburtsdatum': geburtsdatum,
        'email': email,
        'faecher': faecher
    }

    result = supabase.table('schueler').insert(new_schueler).execute()

    if result.status_code == 201:
        return jsonify({'message': 'Schüler erfolgreich hinzugefügt'}), 201
    else:
        return jsonify({'error': 'Fehler beim Hinzufügen des Schülers'}), 500

@app.route('/schueler/<name>', methods=['DELETE'])
def delete_schueler(name):
    result = supabase.table('schueler').delete().eq('name', name).execute()

    if result.status_code == 204:
        return jsonify({'message': 'Schüler erfolgreich gelöscht'}), 204
    else:
        return jsonify({'error': 'Fehler beim Löschen des Schülers'}), 500

@app.route('/schueler/<name>', methods=['PUT'])
def update_schueler(name):
    data = request.get_json()
    geburtsdatum = data.get('geburtsdatum')
    email = data.get('email')
    faecher = data.get('faecher')

    if not geburtsdatum and not email and not faecher:
        return jsonify({'error': 'Mindestens ein Feld (Geburtsdatum, E-Mail oder Fächer) muss aktualisiert werden'}), 400

    update_data = {}
    if geburtsdatum:
        update_data['geburtsdatum'] = geburtsdatum
    if email:
        update_data['email'] = email
    if faecher:
        update_data['faecher'] = faecher

    result = supabase.table('schueler').update(update_data).eq('name', name).execute()

    if result.status_code == 200:
        return jsonify({'message': 'Schüler erfolgreich aktualisiert'}), 200
    else:
        return jsonify({'error': 'Fehler beim Aktualisieren des Schülers'}), 500
    


if __name__ == '__main__':
    print("Starting Nachhilfe API...")
    app.run(debug=True)