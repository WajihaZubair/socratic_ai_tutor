To save memory on computer, the project is split into two halves:
1. The Remote Server (Google Colab): Runs the heavy AI model using a cloud GPU.
2. The Local Interface (Your Computer): Runs a simple webpage where you can type your questions. 
3. The Bridge(ngrok): Safely connects your computer to the cloud server.


Step 1: Set Up the Remote Cloud Server
1. Open Google Colab and switch the runtime to T4 GPU
2. Run all the cells. In cell 2, upload the 'cleaned_train.jsonl' and 'cleaned_valid.jsonl' files. 
3. The Networking Tunnel has my ngrok token. If it doesn't work for you, sign up for a free account at ngrok.com, copy your personal authtoken, and replace mine in the code.
4. Once the server script is running, copy the generated ngrok URL link (https://xyz.ngrok-free.dev).

Step 2: Set Up Your Computer
1. Download or clone the project folder into pycharm.
2. Run the 'pip install -r requirements.txt' command to download all the necessary libraries.
3. In the 'inference.py' file, find the 'colab_URL' variable (line 6) and paste the copied ngrok link into it. Add '/generate' at the end of the link.
4. Run the 'app.py' file and open the local web link displayed in the terminal to start using the Socratic chat system.
