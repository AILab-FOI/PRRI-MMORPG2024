set DBIP=localhost
set DBPORT=8100
set SERVER_PORT=6789

start "ZEO_TASK" "cmd /c runzeo -C zeo.conf"

AgeOfDogma_DedicatedServer.exe --port "%SERVER_PORT%" --dbhost "%DBIP%" --dbport "%DBPORT%"
pause
taskkill "ZEO_TASK"