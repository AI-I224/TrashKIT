'''
*****************************************************************************/

File: consumer.py
Author: Andrew Ize-Iyamu
Date: 2024-11-26
Description: Consumer thread that recieves the gesture ID sent by the
producer.py file in the queue, and then sends the recieved ID to the Bela
board via OSC client communication

*****************************************************************************/

References:

*****************************************************************************/
*    Title: An Intro to Threading in Python
*    Author: Anderson, J
*    Date: 2019
*    Code version: N/A
*    Availability: https://realpython.com/intro-to-python-threading/
****************************************************************************/

*****************************************************************************/
*    Title: Multithreading - Producer and Consumer with Queue
*    Author: Hong, K
*    Date: 2020
*    Code version: N/A
*    Availability: https://www.bogotobogo.com/python/Multithread/python_multithreading_Synchronization_Producer_Consumer_using_Queue.php
****************************************************************************/

*****************************************************************************/
*    Title: python-osc 1.9.0
*    Author: PyPI
*    Date: 2024
*    Code version: 1.9.0
*    Availability: https://pypi.org/project/python-osc/
****************************************************************************/
'''

# Import required library
from pythonosc import udp_client

# Setup for Bela IP and port
bela_ip = "192.168.7.2"
bela_port = 7562

# OSC client to send messages to Bela
client = udp_client.SimpleUDPClient(bela_ip, bela_port)

def consumer(queue):
    '''
    Consumer logic that takes the gesture ID produced by the producer logic
    as an input and sends to Bela via OSC message
    '''
    # Used cited resources by J. Anderson & K. Hong 
    # to learn and understand how to create and structure 
    # consumer logic

    # Used python-osc documentation to establish 
    # OSC sender client in pure python

    while True:
        # Collects gesture IDs from threading queue
        gesture_ID = queue.get()

        # Stops code if gesture ID is None to prevent
        # logic from breaking
        if gesture_ID is None:
            break
        else:
            # Sends the gesture ID to Bela using OSC communication
            client.send_message("/osc-test", [gesture_ID, 6.2])

            # Prints sent gesture ID to terminal for debugging
            print(f"Sent gesture ID {gesture_ID} to Bela")
