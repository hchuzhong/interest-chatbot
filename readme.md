### Checking for existing chatbot.tar and remove it
rm -f ./chatbot.tar

### Building Docker image
docker build -t chatbot:latest .

### Saving Docker image to tar file
docker save -o ./chatbot.tar chatbot:latest

### Copying tar file to remote server
scp -i server_key_path -r ./chatbot.tar user_name@server_address:/home/azureuser/chatbot

### Loading Docker image on remote server
ssh -i server_key_path user_name@server_address "sudo docker load -i /home/azureuser/chatbot/chatbot.tar"

### Checking for existing container named 'chatbot_container' on remote server
ssh -i server_key_path user_name@server_address "sudo docker ps -a -q --filter name=chatbot_container | grep -q . && sudo docker rm -f chatbot_container

### Running Docker container on remote server
ssh -i server_key_path user_name@server_address "sudo docker run -d -p 5005:5005 --name chatbot_container chatbot:latest"

### To activate this environment, use

`conda activate venv`

### To deactivate an active environment, use

`conda deactivate`