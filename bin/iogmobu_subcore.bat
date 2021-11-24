@echo off

:: MotionBuilder requires a .py file to be executed as script and it
:: cannot take additional args from the command line. In order to pass
:: the iograft core address into the Subcore, we must create a
:: temporary Python script that has baked in the subcore address.

:: Create a temporary file for the python script.
:: TODO: This "random" name generation is not guaranteed to be unique.
::       And the random-ness is based on time, so collisions are possible.
::       However, for our purposes it is probably good enough.
set TMPFILE=%TMP%\iogmobu_subcore-%RANDOM%-%TIME:~6,5%.py

:: Write the passed in args into the tmp file.
echo ARGS_STR = '%*' > %TMPFILE%

:: Write the subcore python script into the temporary Python file.
for /f "tokens=* delims=" %%l in (%~dp0\iogmobu_subcore_template.py) do (
    echo %%l >> %TMPFILE%
)
echo Wrote MotionBuilder Subcore script to: %TMPFILE%

:: Get the full path to the motionbuilder executable. For some reason,
:: MotionBuilder doesn't like being launched from a Batch script with
:: a relative path. Interestingly, the motionbuilder.exe is found,
:: but it exits immediately. Calling with the full path works as expected.
for /f "delims=" %%i in ('where motionbuilder.exe') do set MB_PATH=%%i

:: Launch MotionBuilder in batch mode and execute the subcore python
:: script.
"%MB_PATH%" -batch -console -verbosePython %TMPFILE%

:: Check the return code and if all was good, delete the subcore's
:: temporary Python script.
if %ERRORLEVEL% EQU 0 (
    del %TMPFILE%
)
