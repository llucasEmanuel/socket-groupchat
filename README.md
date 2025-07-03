# socket-groupchat
Group chat application built using Python's socket library, developed for the IF678 - Infraestrutura de Comunicação project.

---

## Running the project on Linux
1) **Open the terminal and clone the repository**
```bash
git clone https://github.com/llucasEmanuel/socket-groupchat.git
cd socket-groupchat
```
2) **Move the file you want to send to `client/files/` directory (only if you don't want to use the example files)**
```bash 
mv <your_file_name> client/files
```
3) **Open your favorite code editor in this directory and open `client/main.py` file**
```bash
vim client/main.py
```
4) **Change the `file_name` variable to your file name and close the editor**
```python
file_name = "<your_file_name>"
```
5) **In the same terminal, run the `run_server.sh` script**
```bash
bash run_server.sh
```
6) **Open another terminal, go to the `socket-groupchat` directory and run the `run_client.sh` script**
```bash
cd socket-groupchat
bash run_client.sh
```
7) **After running the client, if everything runs correctly, you will find a file named `recv_<your_file_name>` in server/files and another one named `recv_recv_<your_file_name>` in client/files**

**Well done! You've successfully run the client-server file sending program!!**