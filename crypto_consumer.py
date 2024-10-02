from confluent_kafka import Consumer, TopicPartition , KafkaException
import time
import json

class CryptoConsumer:
    
    def __init__(self):

        #Conf to consumer
        conf = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'crypto_group',
            'auto.offset.reset': 'earliest'
        }

        # Create consumer with conf
        self.consumer = Consumer(conf)

        #manual assigment of topic, and partition
        partition = TopicPartition('crypto_price', 0)

        #Subscribe to the topic
        self.consumer.assign([partition])

        # === Accumulator vars

        #sizes
        self.btc_size = 0
        self.eth_size = 0
        self.sol_size = 0

        #transacted capital
        self.btc_capital = 0
        self.eth_capital = 0
        self.sol_capital = 0


        #counter messages
        self.count_message = 0


        #Count buy/sell
        self.btc_buy = 0
        self.btc_sell = 0
        self.eth_buy = 0
        self.eth_sell = 0
        self.sol_buy = 0
        self.sol_sell = 0



    #Goal: update vars 
    def update_vars(self):
        
        try: 
            #Consume to up 100 message for each second
            messages = self.consumer.consume(num_messages=100, timeout=1.0)

            #scroll through list looking for data
            for msg in messages:

                if msg is None:
                    print("Mensaje vacío")
                    continue

                else:
                    
                    #decode data
                    data = json.loads(msg.value().decode("utf-8"))
                    
                    print(data)
                    #detect and updte vars
                    if data['product_id'] == 'BTC-USD':
                        self.btc_size += data['last_size']
                        self.btc_capital += data['transacted_capital']

                        #Count buy/sell BTC
                        if data['side'] == 'sell':

                            self.btc_sell += data['last_size']

                        else:
                            self.btc_buy += data['last_size']
                        
                        
                    elif data['product_id'] == 'ETH-USD':
                        self.eth_size += data['last_size']
                        self.eth_capital += data['transacted_capital']

                        #Count buy/sell ETH
                        if data['side'] == 'sell':

                            self.eth_sell += data['last_size']

                        else:
                            self.eth_buy += data['last_size']

                    elif data['product_id'] == 'SOL-USD':
                        self.sol_size += data['last_size']
                        self.sol_capital += data['transacted_capital']
                        
                        #Count buy/sell SOL
                        if data['side'] == 'sell':

                            self.sol_sell += data['last_size']

                        else:
                            self.sol_buy += data['last_size']


                #Control errors
                if msg.error():
                    print(f"Error with message: {msg.error()}")
                    continue

                #Count message
                self.count_message += 1
                

            
            #Print message receive
            print(f"message received: {msg.value().decode('utf-8')}")



        except:
            pass

