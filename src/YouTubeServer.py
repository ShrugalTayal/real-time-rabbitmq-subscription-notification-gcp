import pika
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os

class YouTubeServer:
    def __init__(self, host):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='user_requests')
        self.channel.queue_declare(queue='youtuber_requests')

    def consume_requests(self):
        """
        Consumes requests from the user_requests queue and processes them.

        This method listens for incoming requests from the user_requests queue,
        processes each request, and performs appropriate actions based on the
        request type (e.g., login or subscription).
        """
        def consume_user_requests(ch, method, properties, body):
            """
            Callback function to handle received requests from the user_requests queue.

            Args:
                ch: Channel object.
                method: DeliveryTag object.
                properties: BasicProperties object.
                body: Request body containing JSON data.
            """
            # Parse the request body as JSON
            request = json.loads(body)

            # Process the request based on its action
            if request["action"] == "login":
                print(f"{request['username']} logged in")
            elif request["action"] == "subscription":
                print(f"{request['username']} {request['operation']} to {request['youtuber']}")
                
                # Prepare document for database insertion/update
                document = {'action': request["action"], 'username': request['username'], 'youtuber': request['youtuber'], 'operation': request['operation']}
                filter = {'action': request["action"], 'username': request['username'], 'youtuber': request['youtuber']}
                
                # Check if document already exists in the database
                existing_document = collection.find_one(filter)
                # If no existing document found, insert the new document
                if existing_document is None:
                    collection.insert_one(document)
                else:
                    # Update the existing document
                    collection.update_one(filter, {'$set': document})
                    
        def notify_users(self, youtuber, video_name, subscribers):
            """
            Notifies the subscribers of a youtuber about a new video.

            Args:
                youtuber (str): The name of the youtuber.
                video_name (str): The name of the new video.
                subscribers (list): A list of usernames (subscribers) to be notified.
            """
            # Iterate over each subscriber and send notification
            for user in subscribers:
                request = json.dumps({
                    "youtuber": youtuber,
                    "video": video_name
                })
                
                # Declare the queue for the user if it doesn't exist
                self.channel.queue_declare(queue=user)
                # Publish the notification to the user's queues
                self.channel.basic_publish(exchange='', routing_key=user, body=json.dumps(request))

        def consume_youtuber_requests(ch, method, properties, body):
            """
            Consumes requests for youtuber updates from the youtuber_requests queue.

            Args:
                ch: Channel object.
                method: DeliveryTag object.
                properties: BasicProperties object.
                body: Request body containing JSON data.
            """
            # Fetch subscribers of the given youtuber from the database or any storage
            # Parse the request body as JSON
            request = json.loads(body)
            print('{} uploaded {}'.format(request['youtuber'], request['video']))
            
            # Find matching documents (subscribers) from the database
            filter = {"action":"subscription", "youtuber":request["youtuber"],"operation":"subscribed"}
            matching_documents = collection.find(filter)
            
            # Extract usernames of subscribers
            subscribers = [document['username'] for document in matching_documents]

            # Notify subscribers about the uploaded video
            notify_users(self, request['youtuber'], request['video'], subscribers)

        # Set up a consumer to listen for requests from queues
        self.channel.basic_consume(queue='user_requests', on_message_callback=consume_user_requests, auto_ack=True)
        self.channel.basic_consume(queue='youtuber_requests', on_message_callback=consume_youtuber_requests, auto_ack=True)
        print(' [*] Waiting for requests. To exit press CTRL+C')
        self.channel.start_consuming()

if __name__ == '__main__':
    # Replace 'localhost' with the IP address of the Google Cloud instance
    load_dotenv()
    mongo_uri = os.getenv("mongo_uri")
    print(mongo_uri)
    client = MongoClient(mongo_uri)
    db = client.get_database('YT_RMQ_DB')
    collection = db.subscription_records
    youtube_server = YouTubeServer('localhost')
    youtube_server.consume_requests()