## The following Cron jobs are running on the log server:

* \* \* \* \* \* python <path-to-script-folder>/json_server_side.py
* \* \* \* \* \* rsync -avz --remove-source-files -e ssh rsync@X.X.X.X:/home/iperf /home
* \* \* \* \* \* ( sleep 10; rsync -avz --remove-source-files -e ssh rsync@X.X.X.X:/home/iperf /home )
* \* \* \* \* \* ( sleep 20; rsync -avz --remove-source-files -e ssh rsync@X.X.X.X:/home/iperf /home )
* \* \* \* \* \* ( sleep 30; rsync -avz --remove-source-files -e ssh rsync@X.X.X.X:/home/iperf /home )
* \* \* \* \* \* ( sleep 40; rsync -avz --remove-source-files -e ssh rsync@X.X.X.X:/home/iperf /home )
* \* \* \* \* \* ( sleep 50; rsync -avz --remove-source-files -e ssh rsync@X.X.X.X:/home/iperf /home )

X.X.X.X will correspond to the IPerf servers address. The multiple rsync jobs are used to run the jobs every 10 seconds.
