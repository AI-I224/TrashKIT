'''
*****************************************************************************/

File: main.py
Authors: Andrew Ize-Iyamu
Date: 2024-11-26
Description: Main execution of producer and consumer threads
from consumer.py and producer.py files

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
*    Title: The Producer-Consumer Problem in Python
*    Author: Andreson, S. D.
*    Date: N/A
*    Code version: N/A
*    Availability: https://cs.wellesley.edu/~cs304flask/readings/threads/producer-consumer.html
****************************************************************************/
'''

# Import required libraries
from multiprocessing import Process, Queue
import producer
import consumer

if __name__ == "__main__":
    # Used the cited resources above to learn and understand
    # how to create and structure pipelines 
    # to run multiple python files simultaneously

    # Creates a shared queue for communication
    # between the producer logic and consumer logic
    queue = Queue()

    # Creates processes for each logic
    producer_process = Process(target=producer.producer, args=(queue,))
    consumer_process = Process(target=consumer.consumer, args=(queue,))

    # Starts the main threads for each logic
    producer_process.start()
    consumer_process.start()
    print("Starting consumer thread...", flush=True)

    # Blocks main threads until all worker threads are finished
    producer_process.join()
    consumer_process.join()
