from flask import Flask, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

url = "https://mjxwrvgemzlgomliwmwr.supabase.co"
publishable_key = "sb_publishable_dg4lCzwM1mdoH16HRmbjKw_ouDEDlHe"

supabase = create_client(url, publishable_key)




if __name__ == '__main__':
    print("Starting PetBuddy API...")
    app.run(debug=True)