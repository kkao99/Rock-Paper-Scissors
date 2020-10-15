# Rock-Paper-Scissors
A simple network-based game.


## Getting Started

### Requirement
* python `3.5 +`


### Build and Run
* There is a Makefile, simply type `$ make server` to create a TCP server and `$ make client` to create a TCP client.

* For arbitrary player name and port number, follow the format below:
```bash
$ python3 [player_name_1] server [port_number]
$ python3 [player_name_2] client [address]:[port_number]
```

## Implementation
1. Server started.
2. Client make connection.
3. Server greets client and tells client "I'm waiting on a worthy opponent!"
4. Client greets server and tells server "Hello from client!"
5. Client player is prompted to provide his/her name.
6. Client sends his/her name to server.
7. Server acknowledge the client and sends back server player's name.
8. Once both client and server complete the handshake, display
	- [player_name] vs. [player_name]
   on both terminal windows. Then the game begins.

## Features
* Use TCP as the transport layer protocol.
* The program is able to identify invalid input and re-prompt.
* Details are commented in the source code.
