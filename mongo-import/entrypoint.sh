#!/bin/bash

sleep 30

cd  /opt/drainware/data/ddi/
for i in $(ls /opt/drainware/data/ddi/)
do
    echo "FILE: $i";
	mongoimport --host mongo --db ddi --collection $i --file $i;
done

cd  /opt/drainware/data/sandbox/
for i in $(ls /opt/drainware/data/sandbox/)
do
    echo "FILE: $i";
        mongoimport --host mongo --db atp --collection $i --file $i;
done

cd  /opt/drainware/data/dwdlprules/
for i in $(ls /opt/drainware/data/dwdlprules/)
do
    echo "FILE: $i";
	mongoimport --host mongo --db dlp --collection $i --file $i;
done

while true; do sleep 2; done
