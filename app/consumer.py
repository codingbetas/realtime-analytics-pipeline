import json
from kafka import KafkaConsumer
from app.database import init_db, SessionLocal, MetricLog
from datetime import datetime

# Ensure the database table exists
init_db()

print("👂 Consumer started. Listening to Kafka...")

consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Keep a running total in memory for fast aggregation
total_purchases = 0
total_revenue = 0.0

for message in consumer:
    event = message.value
    print(f"📥 Received: {event}")
    
    if event["action"] == "purchase":
        total_purchases += 1
        total_revenue += event["amount"]
        
        # Save a snapshot to the database every time a purchase happens
        # (In a real system, you would batch these, but for our dashboard, real-time is cool)
        db = SessionLocal()
        metric = MetricLog(
            event_type="purchase",
            total_events=total_purchases,
            total_amount=total_revenue,
            timestamp=datetime.utcnow()
        )
        db.add(metric)
        db.commit()
        db.close()