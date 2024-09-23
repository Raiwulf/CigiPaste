import customtkinter as ctk
from firebase_admin import db
import random
from logger import log_event


class Note:
    def __init__(self, value, note_id=None):
        self.id = note_id if note_id else self.generate_id()
        self.value = value

    def generate_id(self):
        existing_ids = self._load_existing_ids()
        while True:
            note_id = f"Note_{random.randint(1000, 9999)}"
            if note_id not in existing_ids:
                return note_id

    @staticmethod
    def _load_existing_ids():
        try:
            notes_ref = db.reference("notes")
            notes = notes_ref.get()
            return {note_id for note_id in notes} if notes else set()
        except Exception as e:
            log_event(f"Error loading existing note IDs: {e}")
            return set()

    def save_to_firebase(self):
        try:
            note_data = {"id": self.id, "value": self.value}
            db.reference(f"notes/{self.id}").set(note_data)
            log_event(f"Saved note {self.id} to Firebase.")
        except Exception as e:
            log_event(f"Error saving note to Firebase: {e}")

    def update_in_firebase(self):
        try:
            db.reference(f"notes/{self.id}").update({"value": self.value})
            log_event(f"Updated note {self.id} in Firebase.")
        except Exception as e:
            log_event(f"Error updating note in Firebase: {e}")

    def __repr__(self):
        return f"Note(id={self.id}, value={self.value})"


class NoteDialog(ctk.CTkToplevel):
    def __init__(self, parent, note=None, on_close_callback=None):
        super().__init__(parent)

        self.on_close_callback = on_close_callback

        if note:
            self.title(f"Edit Note {note['id']}")
            self.note = Note(value=note["value"], note_id=note["id"])
        else:
            self.title("New Note")
            self.note = Note(value="")

        self.id_label = ctk.CTkLabel(self, text="ID:")
        self.id_label.grid(row=0, column=0, padx=10, pady=10)

        self.id_entry = ctk.CTkEntry(self)
        self.id_entry.insert(0, self.note.id)
        self.id_entry.grid(row=0, column=1, padx=10, pady=10)
        self.id_entry.configure(state="readonly")

        self.value_label = ctk.CTkLabel(self, text="Note Value:")
        self.value_label.grid(row=1, column=0, padx=10, pady=10)

        self.value_entry = ctk.CTkEntry(self, width=200)
        self.value_entry.insert(0, self.note.value)
        self.value_entry.grid(row=1, column=1, padx=10, pady=10)

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_note)
        self.save_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def save_note(self):
        self.note.value = self.value_entry.get()
        if self.note.id:
            self.note.update_in_firebase()
        else:
            self.note.save_to_firebase()
        self.on_close()

    def on_close(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()
