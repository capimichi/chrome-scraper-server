import time
from typing import List, Dict, Optional

from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedError

from chromescraperserver.Enum.ConnectionTypeEnum import ConnectionTypeEnum
from chromescraperserver.Enum.OperationEnum import OperationEnum
from chromescraperserver.Model.IdentifyMessage import IdentifyMessage
from chromescraperserver.Model.OperationMessage import OperationMessage
from chromescraperserver.Model.ResponseMessage import ResponseMessage
from chromescraperserver.Model.TaskMessage import TaskMessage
from chromescraperserver.Model.WebSocketProfile import WebSocketProfile


class WebSocketHandler:
    # Declare class variables for storing WebSocket profiles and tasks
    web_socket_profiles: Dict[str, WebSocketProfile]
    tasks: Dict[str, TaskMessage]

    def __init__(self):
        # Initialize the WebSocket profiles and tasks as empty dictionaries
        # Set the timeout value to 10
        self.web_socket_profiles = {}
        self.tasks = {}

    def get_timeout(self):
        # Getter method for the timeout value
        return self.timeout

    def set_timeout(self, timeout: int):
        # Setter method for the timeout value
        self.timeout = timeout

    async def handle(self, websocket: WebSocketServerProtocol):
        # This method is called when a new WebSocket connection is established
        # It logs the connection, creates a WebSocketProfile for it, and adds it to the list of profiles
        # Then it identifies the type of connection and handles it accordingly
        # TODO: Consider breaking this method down into smaller functions

        print(f"New connection from {websocket.remote_address}")

        # Create a new WebSocketProfile for the new connection
        web_socket_profile = WebSocketProfile(websocket)
        # Get the connection key for the new WebSocketProfile
        web_socket_key = web_socket_profile.get_connection_key()
        # Add the new WebSocketProfile to the list of profiles
        self.web_socket_profiles[web_socket_key] = web_socket_profile

        # Identify the type of connection and handle it accordingly
        await self.identify(web_socket_profile)
        await self.handle_connection(web_socket_profile)

    async def close_connection(self, web_socket_profile: WebSocketProfile):
        # This method is called to close a WebSocket connection
        # It removes the WebSocketProfile from the list and closes the WebSocket

        # Get the WebSocket from the WebSocketProfile
        web_socket = web_socket_profile.get_websocket()
        # Get the connection key for the WebSocketProfile
        key = web_socket_profile.get_connection_key()
        # If the connection key is in the list of profiles, remove it
        if key in self.web_socket_profiles:
            del self.web_socket_profiles[key]
        # Close the WebSocket
        await web_socket.close()
        # Log the closure of the connection
        print(f"Connection from {web_socket.remote_address} closed")

    async def get_worker_connections(self) -> List[WebSocketProfile]:
        # Initialize an empty list to store worker connections
        worker_connections = []
        # Iterate over all the keys in the web_socket_profiles dictionary
        for key in self.web_socket_profiles:
            # Get the WebSocketProfile associated with the current key
            web_socket_profile = self.web_socket_profiles[key]
            # If the type of the current WebSocketProfile is WORKER_TYPE
            if(web_socket_profile.get_type() == ConnectionTypeEnum.WORKER_TYPE):
                # Add the current WebSocketProfile to the worker_connections list
                worker_connections.append(web_socket_profile)
        # Return the list of worker connections
        return worker_connections

    async def identify(self, web_socket_profile: WebSocketProfile):
        # Receive a message from the WebSocket associated with the given WebSocketProfile
        identify_message_content = await web_socket_profile.get_websocket().recv()
        # Validate the received message and convert it into an IdentifyMessage object
        identify_message = IdentifyMessage.model_validate_json(identify_message_content)
        # Get the type of the IdentifyMessage object
        web_socket_type = identify_message.get_type()
        # Set the type of the given WebSocketProfile to the type of the IdentifyMessage object
        web_socket_profile.set_type(web_socket_type)

        # Print a message indicating the connection key and type of the given WebSocketProfile
        print(f"Connection from {web_socket_profile.get_connection_key()} identified as {web_socket_type}")

    async def handle_connection(self, web_socket_profile):
        # This method handles a WebSocket connection based on its type
        # It prints a message indicating the connection key and type of the WebSocketProfile
        # If the type of the WebSocketProfile is WORKER_TYPE, it calls handle_worker_connection
        # If the type of the WebSocketProfile is API_TYPE, it calls handle_api_connection
        # TODO: Consider refactoring this to use a strategy pattern or similar

        print(f"Handling connection from {web_socket_profile.get_connection_key()} of type {web_socket_profile.get_type()}")

        if(web_socket_profile.get_type() == ConnectionTypeEnum.WORKER_TYPE):
            await self.handle_worker_connection(web_socket_profile)
        elif(web_socket_profile.get_type() == ConnectionTypeEnum.API_TYPE):
            await self.handle_api_connection(web_socket_profile)

    async def handle_worker_connection(self, web_socket_profile):
        # This method handles a WebSocket connection of type WORKER_TYPE
        # It gets the WebSocket from the WebSocketProfile
        # Then it continuously receives messages from the WebSocket and handles them

        websocket = web_socket_profile.get_websocket()

        while True:
            message = await websocket.recv()
            await self.handle_worker_message(web_socket_profile, message)

    async def handle_worker_message(self, web_socket_profile: WebSocketProfile, message: str):
        # This method handles a message from a WebSocket connection of type WORKER_TYPE
        # It validates the received message and converts it into a TaskMessage object
        # It gets the task ID from the TaskMessage object
        # Then it gets the task associated with the task ID
        # If the task exists, it sets the result of the task to the result of the TaskMessage object
        # It also sets the task to completed
        # Finally, it updates the task in the tasks dictionary
        # TODO: Consider refactoring this to use a strategy pattern or similar

        task_message = TaskMessage.model_validate_json(message)
        task_id = task_message.get_task_id()

        print(f"Received task response: {task_id}")

        self.tasks[task_id] = task_message

        # result_task = await self.get_task(task_id)
        # if result_task is not None:
        #     result_task.set_result(task_message.get_result())
        #     result_task.set_completed(True)
        #     self.tasks[task_id] = result_task


    async def handle_api_connection(self, web_socket_profile):
            # This method handles a WebSocket connection of type API_TYPE
            # It gets the WebSocket from the WebSocketProfile
            # Then it continuously receives messages from the WebSocket and handles them
            # TODO: Consider refactoring this to use a strategy pattern or similar

            websocket = web_socket_profile.get_websocket()

            while True:
                # Receive a message from the WebSocket
                message = await websocket.recv()
                # Handle the received message
                await self.handle_api_message(web_socket_profile, message)

    async def handle_api_message(self, web_socket_profile: WebSocketProfile, message: str):
        # This method handles a message from a WebSocket connection of type API_TYPE
        # It validates the received message and converts it into an OperationMessage object
        # Depending on the operation of the OperationMessage object, it calls the appropriate method to handle the operation

        operation_message = OperationMessage.model_validate_json(message)

        if(operation_message.get_operation() == OperationEnum.GET_WORKERS_OPERATION):
            # If the operation is GET_WORKERS_OPERATION, handle it
            await self.handle_get_workers_operation(web_socket_profile, operation_message)
        elif(operation_message.get_operation() == OperationEnum.GET_PAGE):
            # If the operation is GET_PAGE, handle it
            await self.handle_get_page_operation(web_socket_profile, operation_message)
        elif(operation_message.get_operation() == OperationEnum.GET_TASK):
            # If the operation is GET_TASK, handle it
            await self.handle_get_task_operation(web_socket_profile, operation_message)

    async def handle_get_task_operation(self, web_socket_profile, operation_message):
        arguments = operation_message.get_arguments()
        task_id = arguments["task_id"]
        task = await self.get_task(task_id)
        if task is not None:
            task_content = task.model_dump_json()
            await web_socket_profile.get_websocket().send(task_content)
        else:
            await web_socket_profile.get_websocket().send("{}")


    async def handle_get_workers_operation(self, web_socket_profile, operation_message):
        # This method handles a GET_WORKERS_OPERATION
        # It gets all worker connections
        # Then it creates a ResponseMessage object with the operation of the OperationMessage object and the number of worker connections as the result
        # It sends the ResponseMessage object to the WebSocket associated with the WebSocketProfile

        worker_connections = await self.get_worker_connections()
        response_message = ResponseMessage(
            operation=operation_message.get_operation(),
            result=str(len(worker_connections))
        )
        response_message_content = response_message.model_dump_json()
        await web_socket_profile.get_websocket().send(response_message_content)

    async def handle_get_page_operation(self, web_socket_profile, operation_message):
            # This method handles a GET_PAGE operation
            # It gets all worker connections
            # TODO: Consider breaking this method down into smaller functions

            worker_connections = await self.get_worker_connections()

            # Create a unique task id from a random hash based on current time
            task_id = str(hash(str(time.time())))
            # Create a new TaskMessage object with the unique task id and the operation message
            task_message = TaskMessage(
                task_id=task_id,
                operation=operation_message
            )
            # Add the new task to the tasks dictionary
            self.tasks[task_id] = task_message

            # Get a random worker connection
            worker_connection = worker_connections[0]
            # Convert the task message to JSON format
            task_message_content = task_message.model_dump_json()
            # Print the task message that is being sent to the worker
            print(f"Sending task message to worker: {task_message_content}")
            # Send the task message to the worker
            await worker_connection.get_websocket().send(task_message_content)

            print(f"Sending task message to api: {task_message_content}")
            # Send the task message to the api
            await web_socket_profile.get_websocket().send(task_message_content)




    async def get_task(self, task_id: str) -> Optional[TaskMessage]:
        # This method returns a task from the tasks dictionary based on the task id
        # If the task id exists in the tasks dictionary, it returns the task
        # If the task id does not exist in the tasks dictionary, it returns None

        if task_id in self.tasks:
            return self.tasks[task_id]
        return None