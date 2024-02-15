# video-sharing-rabbitmq-app
 
## **Title**: YouTube RabbitMQ Application

## **Description**:
This repository contains a Python application for managing user subscriptions to YouTube channels using RabbitMQ for messaging and MongoDB for data storage. The application consists of 3 main components: a server that handles: subscription requests, video upload requests, and a client that receives notifications about new videos uploaded by subscribed channels. The README provides instructions on how to set up and run the application.

## **Setup**:
To run the program successfully, follow these steps:

1. **Setup RabbitMQ Server**:
   - Install RabbitMQ on your local machine or any server.
   - Start the RabbitMQ server.
     ```
     pip install pika pymongo
     ```

2. **Install Dependencies**:
   - Make sure you have Python installed on your system.
   - Install the required Python packages using pip:
     ```
     rabbitmq-plugins enable rabbitmq_management
     rabbitmq-service.bat start
     ```

3. **Setup MongoDB Database**:
   - If you haven't already, sign up for a MongoDB Atlas account or set up MongoDB locally.
   - Create a new MongoDB database and note down the connection URI.

4. **Clone the Repository**:
   ```
   git clone https://github.com/ShrugalTayal/video-sharing-rabbitmq-app.git
   cd video-sharing-rabbitmq-app
   ```

5. **Update Configuration**:
   - Update the `MONGODB_URI` variable with the connection URI of your MongoDB database.

## **Scripting commands**:
1. **Run the Youtuber Script**:
   - Open a terminal and navigate to the directory containing the `youtuber.py` file.
   - Run the script using Python, providing the youtuber name and video name as arguments:
     ```
     python Youtuber.py <youtuber_name> <video_name>
     ```

2. **Run the User Script**:
   - Open another terminal and navigate to the directory containing the `user.py` file.
   - Run the script using Python, providing the username as an argument:
     ```
     python User.py <username>
     ```

3. **Subscribe/Unsubscribe from Youtuber**:
   - To subscribe to a youtuber, run the user script with additional arguments:
     ```
     python User.py <username> s <youtuber_name>
     ```
   - To unsubscribe from a youtuber, run the user script with additional arguments:
     ```
     python User.py <username> u <youtuber_name>
     ```

4. **Receive Notifications**:
   - If you didn't subscribe or unsubscribe, the user script will start receiving notifications for the provided username.

5. **Terminate the Programs**:
    - To stop receiving notifications or terminate any of the scripts, press `Ctrl + C` in the respective terminal.