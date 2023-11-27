# XSStrap-master (BETA) 🐍
[Discord](https://discord.gg/upNDjFqkBp)

First and foremost, Cross-Site Scripting (XSS) is a vulnerability that allows the execution of JavaScript commands on a website, enabling various malicious activities such as cookie theft and fake login screens.

XSStrap-master is a tool designed to scan XSS security vulnerabilities on a website (currently only active for URLs). It operates on both Windows, Kali Linux and Termux carrying a substantial payload for testing purposes.

Disclaimer: We do not accept responsibility for any misuse!
# Kali Linux
![kaliTrap](https://github.com/SenselessDNS/XSStrap-master/assets/100872213/12ac0448-9a0c-443f-9a10-d2804043eb74)
# Windows
![winTrap](https://github.com/SenselessDNS/XSStrap-master/assets/100872213/bde86e04-b9bb-4dac-ab44-1302aed9769d)
# Termux
![Screenshot_2023_1127_013545_com termux](https://github.com/SenselessDNS/XSStrap-master/assets/100872213/de8bc8b7-9d3a-4822-92b4-43c3fccd06e2)

# How to use?
```main.py -u "http://www.example.com/index.php?param=1"```
**Performs an XSS vulnerability scan on the site**

```main.py -u "http://www.example.com/index.php?param=1" --user-agent```
**Sends requests with a random user agent**

```main.py -u "http://www.example.com/index.php?param=1` --Level=1```
**Conducts more thorough scans based on the given level; valid values are 1-5 (default is 1)**

```main.py -u "http://www.example.com/index.php?param=1" --sleep-second=5```
**Avoids spam by scanning within the specified time interval**

```main.py -u "http://www.example.com/index.php?param=1" --Cookie="PHPSESSID:QWE123..."```
**Logs in with the specified cookie**

```main.py -u "http://www.example.com/index.php?param=1" --trap-backdoor```
**Creates a backdoor; cookies are extracted via the generated link (this feature is in development)**

# How to install?
```Kali Linux```
1. git clone https://github.com/SenselessDNS/XSStrap-master.git
2. cd XSStrap-master
3. pip3 install -r requirements.txt
4. python3 main.py

```Windows```
1. install XSStrap-master
2. cd XSStrap-master
3. pip install -r requirements.txt
4. python main.py

```Termux```
1. git clone https://github.com/SenselessDNS/XSStrap-master.git
2. cd XSStrap-master
3. pip3 install -r requirements.txt
4. python3 main.py

Note: Mobile data and hotspot must be enabled to use the backdoor feature.
