# Stream data to Coinbase, process with Docker, Kafka and Python

## To begin, you need to install

* Docker and Docker-compose
* Python 3.x
* Python libraries, specified in the requirements.txt file

## Steps to follow

To use the project, you only need to do three things.

### 1) Init docker-compose

Run `docker-compose up -d` to start two Docker containers: one with Zookeeper and another with Kafka. The docker-compose file automatically creates a Kafka topic named `crypto_price`.

### 2) Execute the producer

Run `get_data_coinbase.py` in the terminal. This initiates consuming data from Coinbase, specifically data from each trade.

### 3) Execute the consumer

Run `crypto_dash.py` in another terminal. This initiates the dashboard to update every five seconds.

The brigde in producer and consumer, is topic `crypto_price`.

Finally, you to go in your browser `http://localhost:8050/`, and view the dashbord.

![Captura desde 2024-10-02 20-59-07](https://github.com/user-attachments/assets/c709d88d-2853-4f98-a7da-52b8ef873e85)
