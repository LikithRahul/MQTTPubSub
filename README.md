Setup MQTT Broker using docker compose 

1 -> Update the below two line in mosquitto.conf file to look like below
        #password_file /mosquitto/passwd_file
        allow_anonymous true
        
2 -> Bring up the docker container : docker compose up --build

3 -> Setup username and password
     Run the following command once broker is up : docker exec -it  -u 1883 <container_name> sh
     Then enter the following command : mosquitto_passwd -c /mosquitto/passwd_file <username>
     You'll be prompted to enter password. Choose your password and exit.
     Below is how the terminal looks following the above steps
     
likithrahulk@Likiths-MacBook-Air mosquitto % docker exec -it  -u 1883 mosquitto-mosquitto-1 sh
/ $ mosquitto_passwd -c /mosquitto/passwd_file likith
Password: 
Reenter password: 
/ $ exit

4 -> Update the below two line in mosquitto.conf file to look like below
        password_file /mosquitto/passwd_file
        allow_anonymous false

Ensure you have the following dependencies before you start publisher and subscriber
pip3 uninstall requests charset_normalizer chardet -y
pip3 install requests
pip3 install paho-mqtt

5 -> Start the publisher and subscriber using commands
      python3 publisher.py
      python3 subscriber.py
