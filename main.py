import customtkinter as ctk
from gui import initialize_gui
from firebase_admin import credentials, initialize_app
from firebase_config import DATABASE_URL

cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred, {"databaseURL": DATABASE_URL})

app = ctk.CTk()
app.title("Cigi Paste")
app.geometry("600x400")

client_frame = initialize_gui(app)
client_frame.pack(fill="both", expand=True, padx=10, pady=10)

app.mainloop()
