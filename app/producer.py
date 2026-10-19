import json
import time
import random
from kafka import KafkaProducer

# Connect to Kafka
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("🚀 Producer started. Sending events to Kafka...")

actions = ["purchase", "view", "add_to_cart"]

try:
    while True:
        event = {
            "user_id": random.randint(1, 1000),
            "action": random.choice(actions),
            "amount": round(random.uniform(10.0, 500.0), 2) if random.choice(actions) == "purchase" else 0.0
        }
        
        # Send to the 'user-events' topic
        producer.send('user-events', value=event)
        producer.flush()
        
        print(f"📡 Sent: {event}")
        time.sleep(1) # Send 1 event per second
        
except KeyboardInterrupt:
    print("\n🛑 Producer stopped.")