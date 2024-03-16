from dotenv import load_dotenv
import os

if load_dotenv():
    print("Environment variables loaded successfully.")
else:
    print("Could not load environment variables.")

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

print(f"Client ID: {client_id}")
print(f"Client Secret: {client_secret}")