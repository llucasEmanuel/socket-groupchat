# socket-groupchat
Group chat application built using Python's socket library, developed for the IF678 - Infraestrutura de Comunicação project.

### Group members
- Cleber Lucas Farias - `clfm`
- Maurício Andrey - `mfss2`
- Lucas Emanuel Sabino - `lessl`
- Rian Antony - `rama`
- Gabriel Alves - `gagm`
- Juliana Luiza de Andrade - `jlas2`

---

## Running the project locally on Windows

1) **Open PowerShell or Command Prompt and clone the repository**
```powershell
git clone https://github.com/llucasEmanuel/socket-groupchat.git
cd socket-groupchat
```

2) **In the same terminal, run the server batch file**
```powershell
.\run_server.bat
```

3) **Open another PowerShell/Command Prompt window, navigate to the project directory and run the client**
```powershell
cd path\to\socket-groupchat
.\run_client.bat
```

**Alternative method (using Python directly):**
```powershell
# Terminal 1 (Server)
python -m server.main

# Terminal 2 (Client)  
python -m client.main
```

## Running the project locally on Linux
1) **Open the terminal and clone the repository**
```bash
git clone https://github.com/llucasEmanuel/socket-groupchat.git
cd socket-groupchat
```

2) **In the same terminal, run the `run_server.sh` script**
```bash
bash run_server.sh
```
3) **Open another terminal, go to the `socket-groupchat` directory and run the `run_client.sh` script**
```bash
cd socket-groupchat
bash run_client.sh
```

## Running the project on different machines
1) **Go to `config/settings.py`and change the `SERVER_IP` variable to the IP address of the computer you chose as the server on every machine you want to use (server or client)**

2) **Run the server script on the server machine**

3) **Run the client script on every client machine** 

--- 


## Using the client application

After running the client script, the terminal will wait for a command to connect to the server. The command is `/ola <username>`. After sending this command, if no other connected client is using the username you entered, you will be able to connect to the server. The left arrow will then turn green, and a message from the server will appear, indicating that you have been added to the chat.

**Gongratulations!! You've succesfully connected to the server, and now you are able to send and receive messages to every other online client.**

You can also use various functionalities in the group chat, which are listed in the following table:

| **Command** | **Explanation** |
|:--------:|:------:|
| `/ola <username>`    |  Enters the chat     |
| `/tchau`        | Exits the chat      |
| `/list`        | Lists every online user      |
| `/friends`        | Lists your friends names      |
| `/add <username>`        | Adds `<username>` to your friend list   |
| `/rmv <username>`        | Removes `<username>` from your friend list       |
| `/ban <username>`        | Starts voting to ban `<username>` from chat      |
| `/vote <y or n>`        | Votes to ban (y) or to not ban (n) while at voting     |
| `/kill`        | Exits chat and closes client application     | 
| `/help`        | Lists every usable command      |

