import sys
from time import sleep

from shairportmetadatareader import AirplayListener, AirplayCommand, DEFAULT_SOCKET

# python2 support
input = raw_input if sys.version_info.major <= 2 else input

# list of all possible commands
allowed_cmds = [cmd.value for cmd in AirplayCommand]


def on_track_info(listener, info):
    """
    Print the current track information.
    :param lis: listener instance
    :param info: track information
    """
    print(info)


listener = AirplayListener()
listener.bind(track_info=on_track_info)
listener.start_listening(socket_addr=DEFAULT_SOCKET)  # this method is not blocking

# wait till all data to create an airplay remote is available
while not listener.has_remote_data:
    sleep(1)

# get an airplay remote instance ... this might take some time
print("Waiting for active connection...")
remote = listener.get_remote()
print("Connected to device: {0}".format(remote.hostname))

# show the user a list with available commands
print("Available commands:")
for i, cmd in enumerate(allowed_cmds, 1):
    print("{0}.\t{1}".format(i, cmd))

# read and process the user input
while True:
    cmd = input("Enter command number: ").strip()

    # stop user input
    if cmd == "exit":
        listener.stop_listening()
        break

    # send command
    try:
        cmd = int(cmd)
        if not (1 <= cmd <= len(allowed_cmds)):
            print("Illegal command: {0}".format(cmd))
        else:
            # you should catch exceptions thrown by this function, in case the remote connection is lost
            remote.send_command(allowed_cmds[cmd-1])
    except Exception as e:
        print(e)
        print("Illegal command: {0}".format(cmd))
