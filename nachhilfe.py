from flask import Flask, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

SUPABASE_URL= "https://mtjpvnnqmnehapcvifdv.supabase.co"
SUPABASE_KEY= "sb_publishable_db9KPKVXQn6IB5uqAas28Q_98UA5fXn"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)




if __name__ == '__main__':
    print("Starting Nachhilfe API...")
    app.run(debug=True)