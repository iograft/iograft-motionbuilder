# iograft for Autodesk MotionBuilder

This repository contains scripts and nodes for running iograft within Autodesk MotionBuilder. It includes the iograft Subcore for MotionBuilder, and a few example nodes.

## A Note on Running MotionBuilder in Batch

MotionBuilder has a complicated history when it comes to executing Python scripts in a "batch" or headless mode. Since iograft relies on the ability to start applications in batch to execute nodes, we must address this history.

### MotionBuilder 2018-2020
Prior to version 2022, the Python interpreter (mobupy) did not have access to the MotionBuilder API. This complicates executing MotionBuilder scripts in batch because we have to launch the full MotionBuilder application, but it is still possible.

The [`bin/iogmobu_subcore.bat`](bin/iogmobu_subcore.bat) script is used for executing the iograft subcore in this case. It launches MotionBuilder and passes in a Python script to be executed at launch:

```
motionbuilder.exe -batch -console -verbosePython subcore_script.py
```

In this example, the `subcore_script.py` file will be executed when MotionBuilder launches. Unfortunately, this script cannot take any external arguments so in order to pass the "core-address" argument that the subcore needs to connect to, we must create a temporary Python script file and "bake" in the core-address argument.

This is taken care of automatically in the [`bin/iogmobu_subcore.bat`](bin/iogmobu_subcore.bat) script. The [`bin/iogmobu_subcore_template.py`](bin/iogmobu_subcore_template.py) file defines a Python script template that we bake the "core-address" argument into.

**Note:** In MotionBuilder 2018, there is no `-batch` mode available, so the UI will be launched when the subcore is run. However, the UI will be "frozen" as it is executing the Python script, and when the subcore script finishes, the UI will automatically close.

### MotionBuilder 2022:
In MotionBuilder 2022, Autodesk upgraded the `mobupy` executable with full access to the MotionBuilder API. This makes running the iograft Subcore much easier as we can simply invoke the `mobupy` executable as a regular Python interpreter and easily pass in arguments.

The [`bin/iogmobupy_subcore.bat`](bin/iogmobupy_subcore.bat) script should be used as the Subcore Launch Command when using MotionBuilder 2022 to take advantage of the availability of `mobupy`.

## Getting Started with a MotionBuilder Environment

Below are the steps required to setup a new environment in iograft for executing nodes in MotionBuilder. A similar guide for Autodesk Maya (with a similar setup to MotionBuilder) is also available in the
iograft [Environment Quick Start Guide](https://docs.iograft.com/getting-started/guides/creating-a-new-environment):

1. Clone the iograft-motionbuilder repository.
2. Open the iograft Environment Manager and create a new environment for MotionBuilder (i.e. "mobu2020").
3. Update the **Plugin Path** to include the "nodes" directory of the iograft-motionbuilder repository.
4. Update the **Subcore Launch Command** to "iogmobu_subcore" (or if using MotionBuilder 2022, use "iogmobupy_subcore"). Note: On Windows this will automatically resolve to the "iogmobu_subcore.bat" script.
5. Update the **Path** to include the "bin" directory of the iograft-motionbuilder repository.
6. Update the **Path** to include the directory containing the MotionBuilder executable (and the mobupy executable in MotionBuilder 2022).
7. Depending on the version of MotionBuilder, update the **Python Path** entry for `...\iograft\python39` by switching "python39" to the directory for the correct version of Python. (For MotionBuilder 2018/2020: "python27"; for MotionBuilder 2022: "python37").
8. Save the environment, use the Environment menu to switch to the MotionBuilder environment just created, and start creating MotionBuilder nodes.

## MotionBuilder Subcore for iograft

The MotionBuilder Subcore for iograft (`iogmobupy_subcore`/`iogmobu_subcore_template.py`) defines an iograft Subcore for executing nodes in the MotionBuilder environment.

The main component of the MotionBuilder Subcore is that it uses the `iograft.MainThreadSubcore` class to ensure that all nodes are executed in the main thread.
