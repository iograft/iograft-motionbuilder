# Copyright 2021 Fabrica Software, LLC

import iograft
import iobasictypes


class ImportFileMobu(iograft.Node):
    """
    Import a file into Motion Builder.
    """
    filename = iograft.InputDefinition("filename", iobasictypes.String())
    match_models = iograft.InputDefinition("match_models", iobasictypes.Bool(),
                                           default_value=False)

    @classmethod
    def GetDefinition(cls):
        node = iograft.NodeDefinition("import_file_mobu")
        node.AddInput(cls.filename)
        node.AddInput(cls.match_models)
        return node

    @staticmethod
    def Create():
        return ImportFileMobu()

    def Process(self, data):
        import pyfbsdk

        filename = str(iograft.GetInput(self.filename, data))
        match_models = iograft.GetInput(self.match_models, data)

        # Run the import command.
        result = pyfbsdk.FBApplication().FileImport(filename, match_models)
        if not result:
            raise iograft.NodeProcessException(
                            "Failed to import file: {}".format(filename))


def LoadPlugin(plugin):
    node = ImportFileMobu.GetDefinition()
    plugin.RegisterNode(node, ImportFileMobu.Create)
