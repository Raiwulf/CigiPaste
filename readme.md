# CigiPaste - A Simple Firebase-Powered Note Management App

CigiPaste is a GUI-based note-taking app that allows users to create, edit, delete, and copy notes directly to the clipboard. It uses **Firebase Realtime Database** to store notes and provides an easy interface to manage them. The app features a log system that records actions in real-time and displays them in the GUI.

## Table of Contents

- [Features](#features)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Setting up Firebase and Getting DATABASE_URL](#setting-up-firebase-and-getting-database_url)
  - [Obtaining `serviceAccountKey.json`](#obtaining-serviceaccountkeyjson)
  - [Install Dependencies](#install-dependencies)
- [Running the App](#running-the-app)
- [Usage](#usage)

---

## Features

- **Create, edit, delete, and view notes**: Manage notes through an intuitive GUI.
- **Clipboard integration**: Copy note content directly to the clipboard with a single click.
- **Firebase integration**: Notes are stored and retrieved from Firebase Realtime Database.
- **Logging**: All actions are logged in real-time and displayed in the log tab for easy tracking.
- **Session-based logging**: Logs are stored in files named based on the session start time.

---

## Setup and Installation

### Prerequisites

1. **Python 3.10+**: Ensure you have Python installed.

   - You can download it from the official [Python website](https://www.python.org/downloads/).

2. **Firebase Project**: You will need a Firebase project to store your notes.

---

### Setting up Firebase and Getting `DATABASE_URL`

1. **Create a Firebase Project**:

   - Go to the [Firebase Console](https://console.firebase.google.com/).
   - Click "Add Project" and follow the steps to create a new project.

2. **Enable Realtime Database**:

   - In your Firebase project dashboard, go to "Build" > "Realtime Database".
   - Click "Create Database" and set the location, then start in "Test Mode" for development.

3. **Get the `DATABASE_URL`**:

   - After enabling the Realtime Database, go to the Realtime Database section in the Firebase Console.
   - Copy the database URL, which typically looks like this: `https://your-project-id.firebaseio.com`.

4. **Add your `DATABASE_URL` to your project**:

   - Create a file called `firebase_config.py` and add the following content:

     ```python
     DATABASE_URL = "https://your-project-id.firebaseio.com"
     ```

---

### Obtaining `serviceAccountKey.json`

1. **Generate a Service Account Key**:

   - In the Firebase Console, go to "Project Settings" > "Service Accounts".
   - Click "Generate new private key" and a file named `serviceAccountKey.json` will be downloaded.

2. **Add `serviceAccountKey.json` to your project**:
   - Place the `serviceAccountKey.json` file in the root directory of your project.

---

### Install Dependencies

1. Clone the project repository or copy the provided files to your local directory.
2. Install the required Python dependencies using the `requirements.txt` file. Run the following command in your terminal:

   ```bash
   pip install -r requirements.txt
   ```

   **Dependencies**:

   - `customtkinter`
   - `firebase-admin`
   - `pyperclip`

   If you don't have the `requirements.txt`, manually install the libraries:

   ```bash
   pip install customtkinter firebase-admin pyperclip
   ```

---

## Running the App

Once you've set up your Firebase project, obtained the `DATABASE_URL`, and added the `serviceAccountKey.json` file, you can run the app with the following command:

```bash
python main.py
```

---

## Usage

### Main GUI Features

1. **Notes Tab**:

   - View all saved notes from Firebase.
   - Click on any note to edit it, or select and delete multiple notes.
   - The "Add" button allows you to create a new note.
   - Click on a note to copy its content to the clipboard.

2. **Log Tab**:
   - View real-time logs of app actions, including note creation, deletion, and Firebase errors.
   - Logs are also saved in the `logs` folder under filenames based on the app launch time.

### Notes Management

- **Add a new note**:

  - Click the "+" button to create a new note.
  - Enter the note's content and click "Save".

- **Edit a note**:

  - Click on a note's content to open it in edit mode.
  - Make your changes and click "Save" to update it in Firebase.

- **Delete a note**:
  - Select a note using the checkbox and click the "-" button to delete it from Firebase.

### Logs

All user actions and errors are logged in real-time. You can monitor them in the "Log" tab within the app, and the logs are also saved to a file in the `logs` folder.

---

## Troubleshooting

- **Firebase Permission Denied**:

  - Ensure that your Firebase Realtime Database is in "Test Mode" or adjust the security rules for the database in production.

- **Missing `serviceAccountKey.json`**:
  - Make sure that the file is present in the root of your project and has the correct permissions.

---

Enjoy using **CigiPaste** for managing your notes efficiently!
