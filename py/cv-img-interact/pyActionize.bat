1>NUL prompt ImageVision v6: 
1>NUL  Echo off
echo %1% %2%
REM cls
echo activating the ImageVision v6 environment...
call conda activate ImageVision
REM echo %~d0

%~d0
1>NUL cd\
1>NUL cd %~dp0
1>NUL cd

REM call python %~dp0capturesnap.py %1 %~dp0%2
call python %~dp0actionize_handler.py %1 %2
echo %~dp0%2
call conda deactivate
prompt
REM 1>NUL echo on
1>NUL exit
