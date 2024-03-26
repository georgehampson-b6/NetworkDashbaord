@echo off
Setlocal EnableDelayedExpansion
powershell write-host -fore Red This Script Will Open Bolt6 Internet Testing in your Web Browser...
powershell write-host -fore Red ---
powershell write-host -fore Red ---
powershell write-host -fore Red ---

streamlit run StreamlitBolt6Tests.py

pause