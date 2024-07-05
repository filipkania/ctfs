#!/bin/bash

# generated from solve.py
guess_secret="a42165856bd618589aa0e89d85f86633306238656366613464396463626265623631343038353139323536396462343732393636633634326139633331353530636434653836303262353866373261333036373464373737626633633834303132336161303830373965396332643063343637393035313966633036393666336236343363663365633930363136"
enc_flag="U2FsdGVkX1/ECcB1o6sPHGSDIow+uCwIap1wb1D6duq1ngeg5gdl3LvGcSNi2Sqrl61P/4bdkpX1eT3mMKnC+GTzO0NfUdR8gZewxSryNNA="

secret=`echo -n "$guess_secret" | head -c 28 | xxd -r -p`

echo -n "$secret" > ./guessed_secret.bin
echo -n "$enc_flag" > ./flag.txt.enc

enc_aes=`openssl enc -d -aes-256-cbc -pbkdf2 -iter 1000001 -salt -a -A -kfile ./guessed_secret.bin -in ./flag.txt.enc`
echo $enc_aes
