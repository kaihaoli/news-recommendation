import json
import pika

class CloudAMQPClient:
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(cloud_amqp_url)
        self.params.socket_timeout = 3
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def sendMessage(self, message):
        # Basic Send Message to MQ
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=json.dumps(message))
        print "[X] Sent messages to %s: %s" % (self.queue_name, message)

    def getMessage(self):
        # Basic Get message From MQ
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name)

        # Whether received Message ?
        if method_frame is not None:
            print "[O] Received message from %s: %s" % (self.queue_name, body)
            # Announcement : Had Received Message from YOU !!!
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
        else:
            print "No message returned"
            return None

    def sleep(self, seconds):
        # Why not System sleep?
        # Keep heart beat with Cloud AMQP
        self.connection.sleep(seconds)

if __name__ == '__main__':
    CLOUDAMQP_URL = "amqp://bddugymf:6Vf5lxc4tfV8HHP1MSPJO3yzhl_iGlVR@eagle.rmq.cloudamqp.com/bddugymf"
    TEST_QUEUE_NAME = 'test'
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)
    sentMsg = {'test':'demo'}
    client.sendMessage(sentMsg)
    client.sleep(10)
    receivedMsg = client.getMessage()
    assert sentMsg == receivedMsg
    print 'test_basic passed!'