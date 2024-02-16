import pika
import sys
import json

class Youtuber:
    def __init__(self, host):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=pika.PlainCredentials('shrugal', 'shrugal01')))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='youtuber_requests')

    def publish_video(self, youtuber, video_name):
        """
        Publishes a video request to RabbitMQ queue.
        
        Args:
            youtuber (str): The name of the youtuber.
            video_name (str): The name of the video.
        """
        # Create a request object
        request = json.dumps({
            "youtuber": youtuber,
            "video": video_name
        })
        try:
            # Publish the request to RabbitMQ queue
            self.channel.basic_publish(exchange='', routing_key='youtuber_requests', body=request)
            print("SUCCESS")
        except Exception as e:
            print(f"Failed to publish request: {e}")

if __name__ == '__main__':
    youtuber_name = sys.argv[1]
    video_name = ' '.join(sys.argv[2:])
    # Replace 'localhost' with the IP address of the Google Cloud instance
    youtuber = Youtuber('35.223.32.92')
    youtuber.publish_video(youtuber_name, video_name)