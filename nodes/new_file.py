# Copyright 2022 Fabrica Software, LLC

import iograft
import iobasictypes


class NewFileMobu(iograft.Node):
    """
    Create a new file in Motion Builder (FILE > NEW).
    """
    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("new_file_mobu")
        node.SetMenuPath("MotionBuilder")
        return node

    @staticmethod
    def Create():
        return NewFileMobu()

    def Process(self, data):
        import pyfbsdk
        result = pyfbsdk.FBApplication().FileNew()
        if not result:
            raise iograft.NodeProcessException("Failed to create new file.")


def LoadPlugin(plugin):
    node = NewFileMobu.GetDefinition()
    plugin.RegisterNode(node, NewFileMobu.Create)
