REM echo %1% %2%
REM python %~dp0img-interaction-handler.py %1 %~dp0%2


1>NUL prompt ImageVision v3: 
1>NUL  Echo off
REM cls
echo activating the ImageVision v3 environment...
call conda activate ImageVision
REM echo %~d0

%~d0
1>NUL cd\
1>NUL cd %~dp0
1>NUL cd

REM call python %~dp0capturesnap.py %1 %~dp0%2
call python %~dp0img-interaction-handler.py %1 %~dp0%2
echo %~dp0%2
call conda deactivate
prompt
REM 1>NUL echo on
1>NUL exit
