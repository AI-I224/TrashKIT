'''
*****************************************************************************/

File: osc_test.py
Author: Andrew Ize-Iyamu
Date: 2024-11-26
Description: Test file to ensure that OSC client communication has been
properly set up between computer and Bela board

*****************************************************************************/

References:

*****************************************************************************/
*    Title: python-osc 1.9.0
*    Author: PyPI
*    Date: 2024
*    Code version: 1.9.0
*    Availability: https://pypi.org/project/python-osc/
*****************************************************************************/
'''

from pythonosc import udp_client, dispatcher, osc_server
import random


# Set IP and Ports
bela_ip = "192.168.7.2"  # Replace with Bela's actual IP
bela_port = 7562          # Bela's localPort
laptop_port = 7563        # Laptop's listening port

# OSC Client to send messages to Bela
client = udp_client.SimpleUDPClient(bela_ip, bela_port)

# OSC Message Handler
def osc_test_handler(address, *args):
    print(f"Received: {address} {args}")
    client.send_message("/osc-test-reply", [42, 3.14])

# Dispatcher for receiving OSC
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/osc-test", osc_test_handler)


# Example of sending a message to Bela
if __name__ == "__main__":
    client.send_message("/osc-test", [random.randrange(1,10), 6.2])