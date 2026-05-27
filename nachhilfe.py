from flask import Flask, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

url = "https://mtjpvnnqmnehapcvifdv.supabase.co"
publishable_key = "sb_publishable_db9KPKVXQn6IB5uqAas28Q_98UA5fXn"
 

supabase = create_client(url, publishable_key)


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