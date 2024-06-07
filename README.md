# Environment and Credentials Setup

1. Create a virtual environment

```shell
# Mac/Linux
python3 -m venv venv
. venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate.bat
```

2. Install required packages

```shell
pip install -r requirements.txt
```

3. Change the filename of `.env` and replace `your-key-here` with your corresponding API key, authtoken, etc. for each line. **Make sure to not share this file with anyone or upload it to GitHub**. You will need:
    1. An [AssemblyAI API Key](https://www.assemblyai.com/dashboard/signup) with funds added to access realtime transcription
  

# Run the application

Execute `python main.py` or `python3 main.py` in the project directory to start the application. Then, call your Twilio phone number and begin speaking. You will see your speech transcribed in the console.