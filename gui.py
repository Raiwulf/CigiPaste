import customtkinter as ctk
import pyperclip
from firebase_admin import db
from note import NoteDialog
from logger import log_event, initialize_logging

client_status_label = None
log_textbox = None


def initialize_gui(app):
    global client_status_label, log_textbox, notes_frame

    initialize_logging()

    client_frame = ctk.CTkFrame(app)
    tab_frame = ctk.CTkFrame(client_frame)
    tab_frame.pack(fill="both", expand=True, padx=10, pady=10)
    status_frame = ctk.CTkFrame(client_frame)
    status_frame.pack(side="bottom", fill="x", padx=10, pady=10)

    tab_view = ctk.CTkTabview(tab_frame)
    tab_view.pack(fill="both", expand=True)
    tab_view.add("Notes")
    tab_view.add("Log")

    notes_tab = tab_view.tab("Notes")
    log_tab = tab_view.tab("Log")

    log_textbox = ctk.CTkTextbox(log_tab, height=10)
    log_textbox.pack(fill="both", expand=True, padx=10, pady=10)

    client_status_label = ctk.CTkLabel(status_frame, text="Status: Ready")
    client_status_label.pack(pady=10)

    notes_frame = ctk.CTkFrame(notes_tab)
    notes_frame.pack(fill="x", padx=10, pady=(10, 0))

    load_notes(app)

    button_frame = ctk.CTkFrame(notes_tab)
    button_frame.pack(side="bottom", pady=10)

    add_button = ctk.CTkButton(
        button_frame,
        text="+",
        command=lambda: NoteDialog(
            app, note=None, on_close_callback=lambda: load_notes(app)
        ),
    )
    add_button.grid(row=0, column=0, padx=5)

    remove_button = ctk.CTkButton(
        button_frame, text="-", command=lambda: remove_selected_notes(app)
    )
    remove_button.grid(row=0, column=2, padx=5)

    refresh_button = ctk.CTkButton(
        button_frame, text="↻", command=lambda: load_notes(app)
    )
    refresh_button.grid(row=0, column=3, padx=5)

    return client_frame


def load_notes(app):
    global notes_frame

    for widget in notes_frame.winfo_children():
        widget.destroy()

    try:
        notes_ref = db.reference("notes")
        notes = notes_ref.get()

        if notes:
            for idx, note_id in enumerate(notes):
                note_value = notes[note_id].get("value", "")

                note_checkbox = ctk.CTkCheckBox(notes_frame, text=note_id)
                note_checkbox.grid(row=idx, column=0, padx=5, pady=5, sticky="w")
                note_checkbox.bind(
                    "<ButtonRelease-1>",
                    lambda e, note_value=note_value: copy_to_clipboard(note_value),
                )

                note_label = ctk.CTkLabel(notes_frame, text=note_value)
                note_label.grid(row=idx, column=1, padx=5, pady=5, sticky="w")

                note_data = {"id": note_id, "value": note_value}

                note_label.bind(
                    "<Button-1>",
                    lambda e, n=note_data: NoteDialog(
                        app, note=n, on_close_callback=lambda: load_notes(app)
                    ),
                )
        else:
            log_event("No notes found in Firebase.", log_textbox)
    except Exception as e:
        log_event(f"Error loading notes from Firebase: {e}", log_textbox)


def remove_selected_notes(app):
    for checkbox in notes_frame.winfo_children():
        if isinstance(checkbox, ctk.CTkCheckBox) and checkbox.get():
            note_id = checkbox.cget("text")
            try:
                db.reference(f"notes/{note_id}").delete()
                log_event(f"Deleted note: {note_id}", log_textbox)
            except Exception as e:
                log_event(f"Error deleting note from Firebase: {e}", log_textbox)
    load_notes(app)


def copy_to_clipboard(note_value):
    try:
        pyperclip.copy(note_value)
        log_event(f"Copied note to clipboard: {note_value}")
    except Exception as e:
        log_event(f"Failed to copy to clipboard: {e}")
