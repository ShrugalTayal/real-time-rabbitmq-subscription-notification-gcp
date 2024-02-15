import pika
import sys
import json
import ast

class User:
    def __init__(self, username, host):
        self.username = username
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='user_requests')

    def update_subscription(self, youtuber, subscribe=True):
        """
        Update subscription status for a youtuber.

        Args:
            youtuber (str): The name of the youtuber.
            subscribe (bool, optional): Whether to subscribe or unsubscribe. Default is True (subscribe).
        """

        # Create a request object        
        request = {
            "action": "subscription",
            "username": self.username,
            "youtuber": youtuber,
            "operation": "subscribed" if subscribe else "unsubscribed"
        }

        # Publish the request to RabbitMQ queue
        try:
            self.channel.basic_publish(exchange='', routing_key='user_requests', body=json.dumps(request))
            print("SUCCESS")
        except Exception as e:
            print(f"Failed to publish request: {e}")

    def receive_notifications(self):
        """
        Receive notifications for the user.

        This method starts consuming notifications from the RabbitMQ queue
        associated with the user's username. It also logs in the user before
        starting to receive notifications.

        Note: This method will continuously listen for notifications until the
        program is terminated.
        """

        def login(self):
            request = {
                "action": "login",
                "username": self.username
            }
            try:
                self.channel.basic_publish(exchange='', routing_key='user_requests', body=json.dumps(request))
            except Exception as e:
                print(f"Failed to publish request: {e}")

        def callback(ch, method, properties, body):
            response = json.loads(body)
            response = ast.literal_eval(response)
            print("New Notification: {} uploaded {}".format(response['youtuber'], response['video']))

        try:
            login(self)
            self.channel.basic_consume(queue=self.username, on_message_callback=callback, auto_ack=True)
            print(f' [*] Waiting for notifications for {self.username}. To exit press CTRL+C')
            self.channel.start_consuming()
        except Exception as e:
            print(f"Failed to receive notifications: {e}")

if __name__ == '__main__':
    username = sys.argv[1]
    # Replace 'localhost' with the IP address of the Google Cloud instance
    user = User(username, 'localhost')
    if len(sys.argv) > 2:
        action = sys.argv[2]
        youtuber = sys.argv[3]
        if action == 's':
            user.update_subscription(youtuber)
        elif action == 'u':
            user.update_subscription(youtuber, subscribe=False)
    else:
        user.receive_notifications()