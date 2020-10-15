import socket
import sys
import re
import time

# loopback
HOST = '127.0.0.1'

# my ip addr
# HOST = '192.168.0.192'

# csug cycle1's ipv4 address
# HOST = '128.151.69.85'

CHOICES = ['r', 'p', 's']


class ArgumentMismatchException(Exception):
    """ custom Exception for argument mismatch """
    def __init__(self, message='Argument Mismatch'):
        self.message = message
        super().__init__(self.message)


class RPS:
    """ RPS class. """

    # initialize a RPS object
    def __init__(self, type, name, port):
        super(RPS, self).__init__()
        self.type = type
        self.name = name
        self.port = port

        # split client argv's third argument into addr and port
        if type == 'client':
            self.port = port.split(':')[1]
            self.addr = port.split(':')[0]

    def __str__(self):
        return "--------------------\n" \
                "[Player Info]\n" \
                f"TCP Type: {self.type}\n" \
                f"TCP Name: {self.name}\n" \
                f"TCP Port: {self.port}\n" \
                "--------------------"

    def server(self):

        # run a TCP server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            # set the socket at 30-second timeout
            s.settimeout(30.0)

            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, int(self.port)))
            s.listen()

            # accepting connection from client
            connection, address = s.accept()

            # when received connection from client
            with connection:
                print('Server is being connected by', address)

                # protocol specifics #2
                connection.sendall(bytes("I'm waiting on a worthy opponent!", 'utf-8'))

                # protocol specifics #3
                data = connection.recv(1024)
                print('\nClient said:', data.decode())

                # protocol specifics #4
                data = connection.recv(1024)
                print('\nClient said:', data.decode())

                # protocol specifics #5
                name = input('\nPlease enter your name to acknowledge the player: ').strip()
                c_name = re.findall(r'^My name is (.+),', data.decode())[0]
                send = f'Hi {c_name}, and my name is {name}. Let\'s play the game!'
                print(f'\nYou sent: \"{send}\"')
                connection.sendall(bytes(send, 'utf-8'))
                print('\n====================')
                print(f'{name} vs. {c_name}')
                print('====================')

                print('\n[Rules]\nRock-Paper-Scissor Game Started.\nR > S, P > R, S > P.\nChoose one: [r, p, s]')

                # begin playing RPS (stargin protocoal specifics #6)
                while True:

                    # prompt user to input a choice
                    prompt = input('\n> ').strip().lower()
                    choice = self._full_name(prompt)

                    if choice:

                        # protocol specifics #7
                        print(f'\nAre you sure [{choice}] is your choice? Enter [yes] to confirm or [no] to select a different choice.')
                        confirm = input('\n> ')

                        # protocol specifics #8
                        if confirm.strip().lower() == 'yes':
                            connection.sendall(bytes(prompt, 'utf-8'))
                            print('\nWaiting for the opponent...')
                            data = connection.recv(1024)
                            print('\nReceived! The result will display in')

                            # protocol specifics #9
                            print('\n3')
                            time.sleep(1)
                            print('\n2')
                            time.sleep(1)
                            print('\n1')
                            time.sleep(.995)

                            # display result
                            self._result(prompt, data.decode(), name, c_name)
                            s.close()
                            break
                        else:
                            print('\nPlease enter your choice [r, p, s].')
                            continue

                    else:
                        print('\nInput mismatch. Please try again.')


    def client(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            # connect to an existing TCP with specified port number
            s.connect((self.addr, int(self.port)))

            # protocol specifics #2
            data = s.recv(1024)
            print('\nServer said:', data.decode())

            # protocol specifics #3
            s.sendall(bytes('Hello from client!', 'utf-8'))

            # protocol specifics #4
            name = input('\nPlease enter your name to initiate the communication: ').strip()
            send = f'My name is {name}, and what\'s your name?'
            print(f'\nYou sent: \"{send}\"')
            s.sendall(bytes(send, 'utf-8'))

            # protocol specifics #5
            data = s.recv(1024)
            s_name = re.findall(r'my name is (.+). Let', data.decode())[0]
            print('\nServer said:', data.decode())
            print('\n====================')
            print(f'{name} vs. {s_name}')
            print('====================')

            print('\n[Rules]\nRock-Paper-Scissor Game Started.\nR > S, P > R, S > P.\nChoose one: [r, p, s]')

            # begin playing RPS (starting protocol specifics #6)
            while True:

                # prompt user to input a choice
                prompt = input('\n> ').strip().lower()
                choice = self._full_name(prompt)

                if choice:

                    # protocol specifics #7
                    print(f'\nAre you sure [{choice}] is your choice? Enter [yes] to confirm or [no] to select a different choice.')
                    confirm = input('\n> ')

                    # protocol specifics #8
                    if confirm.strip().lower() == 'yes':
                        s.sendall(bytes(prompt, 'utf-8'))
                        print('\nWaiting for the opponent...')
                        data = s.recv(1024)
                        print('\nReceived! The result will display in')

                        # protocol specifics #9
                        print('\n3')
                        time.sleep(1)
                        print('\n2')
                        time.sleep(1)
                        print('\n1')
                        time.sleep(.995)

                        # display result
                        self._result(prompt, data.decode(), name, s_name)
                        s.close()
                        break
                    else:
                        print('\nPlease enter your choice [r, p, s].')
                        continue
                else:
                    print('\nInput mismatch. Please try again.')


    def _full_name(self, acc):
        if acc in CHOICES:
            if acc == 'r':
                return 'Rock'
            elif acc == 'p':
                return 'Paper'
            else:
                return 'Scissor'
        else:
            return 0


    # identify who wins the game and display to console
    def _result(self, me, other, my_name, other_name):
        print(f'\nYour move: [{self._full_name(me)}]')
        print(f'\n{other_name}\'s move: [{self._full_name(other)}]')
        win = False
        tie = False
        if me == other:
            tie = True
        elif me == 'r' and other == 's':
            win = True
        elif me == 'p' and other == 'r':
            win = True
        else:
            if other == 'p':
                win = True

        if tie:
            print('\nIt is a tie!\n')
        elif win:
            print(f'\nCongratulation! You, {my_name}, win the game!\n')
        else:
            print(f'\nSorry! Your opponent, {other_name}, win the game!\n')



def main():

    # find csug ip
    # print(socket.gethostbyaddr('cycle1.csug.rochester.edu'))

    try:
        assert(len(sys.argv) == 4)

        NAME = sys.argv[1]
        TYPE = sys.argv[2]
        PORT = sys.argv[3]

        # varify user input is correct
        if TYPE != 'server' and TYPE != 'client':
            raise ArgumentMismatchException()

    except AssertionError:
        print('Incorrect number of arguments.')
        print('Arguments should have [player_name] [TCP_type] [port_number]')
        print('Please try again')
        quit()
    except ArgumentMismatchException as e:
        print('Argument Mismatch Occurred.')
        print('Second argument should be either \"server\" or \"client\".')
        print('Please try agiain')
        quit()


    player = RPS(type=TYPE, name=NAME, port=PORT)
    print(player)

    # check which tcp type should be created
    if TYPE == 'server':
        print('Running as server')
        player.server()
    else:
        print('Running as client')
        player.client()


if __name__ == '__main__':
    main()
