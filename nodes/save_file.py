# Copyright 2021 Fabrica Software, LLC

import iograft
import iobasictypes


class SaveFileMobu(iograft.Node):
    """
    Create a new file in Motion Builder (FILE > NEW).
    """
    filename = iograft.InputDefinition("file", iobasictypes.String())
    out_filename = iograft.OutputDefinition("filename", iobasictypes.String())

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("save_file_mobu")
        node.AddInput(cls.filename)
        node.AddOutput(cls.out_filename)
        return node

    @staticmethod
    def Create():
        return SaveFileMobu()

    def Process(self, data):
        import pyfbsdk

        filename = str(iograft.GetInput(self.filename, data))

        # Run the save command.
        result = pyfbsdk.FBApplication().FileSave(filename)
        if not result:
            raise iograft.NodeProcessException(
                            "Failed to save file to: {}".format(filename))

        # Pass through the save filename.
        iograft.SetOutput(self.out_filename, data, filename)


def LoadPlugin(plugin):
    node = SaveFileMobu.GetDefinition()
    plugin.RegisterNode(node, SaveFileMobu.Create)