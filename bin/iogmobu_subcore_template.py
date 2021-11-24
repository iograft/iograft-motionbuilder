# Copyright 2021 Fabrica Software, LLC

# This subcore TEMPLATE for MotionBuilder is used to build a Python
# file that has all args baked into the file since executing a Python
# script in MotionBuilder from the command line can accept no arguments.

import argparse
import iograft
import shlex
import pyfbsdk


def parse_args():
    parser = argparse.ArgumentParser(
            description="Start an iograft subcore to process in Motion Builder")
    parser.add_argument("--core-address", dest="core_address", required=True)
    arg_list = shlex.split(ARGS_STR)
    return parser.parse_args(arg_list)


def StartSubcore(core_address):
    # Initialize iograft.
    iograft.Initialize()

    # Create the Subcore object and listen for nodes to be processed. Use
    # the MainThreadSubcore to ensure that all nodes are executed in the
    # main thread.
    subcore = iograft.MainThreadSubcore(core_address)
    subcore.ListenForWork()

    # Uninitialize iograft.
    iograft.Uninitialize()


# Start the subcore.
args = parse_args()
StartSubcore(args.core_address)

# Close MotionBuilder
pyfbsdk.FBApplication().FileExit()
