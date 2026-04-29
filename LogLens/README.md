=======================
 LogLens Installation
=======================

Thank you for installing LogLens – your automated system log parsing and analysis toolkit powered by Python and LLaMA 3.2.

----------------------------------------
 WHAT'S INCLUDED
----------------------------------------
Python (auto-installed if missing)  
Ollama (for running LLaMA locally)  
LogLens Scripts:
   - fetching.py
   - processing.py
   - analysis.py
launch_menu.ps1 to begin your journey!

----------------------------------------
 HOW TO USE
----------------------------------------
1. Run the installer: `LogLensInstaller.exe`
2. The installer will:
   - Install Python (silent)
   - Install Ollama (silent)
   - Launch the LogLens PowerShell script

3. If the Ollama model (`llama3.2`) fails to install automatically:
   Open PowerShell and run:
      `ollama pull llama3.2`
   This is required for the LogLens AI assistant to function.

4. Once everything is installed, you’ll see the LogLens Menu in PowerShell.

----------------------------------------
 SUCCESS INDICATORS
----------------------------------------
- Python/Ollama install messages shown 
- PowerShell launch menu opens 
- Model downloaded or user manually pulled 
- Ready to analyze logs 

----------------------------------------
IF SOMETHING FAILS
----------------------------------------
- PowerShell doesn't launch:
   - Check if PowerShell execution is allowed:
     Run `Set-ExecutionPolicy RemoteSigned` as Admin.

-  Model install fails:
   - Manually run `ollama pull llama3.2`

-  No logs detected:
   - Make sure your input files are ready.
   - Check `fetching.py` and `processing.py` for logs.

----------------------------------------
INSTALLATION LOCATION
----------------------------------------
All files are placed in:  
`C:\Program Files\LogLens`

----------------------------------------
SUPPORT
----------------------------------------
For help, contact your administrator or open an issue on the LogLens project repo.
Or reach out to the Devs !

Happy log hunting and query analysis for scalability Devs!
– Team LogLens
