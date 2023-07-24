#!/bin/sh
openssl genpkey -algorithm RSA -out intermediate_ca.key
openssl req -new -key intermediate_ca.key -out intermediate_ca.csr
openssl x509 -req -in intermediate_ca.csr -CA ./certs/root_ca.crt -CAkey ./secrets/root_ca_key -CAcreateserial -out intermediate_ca.crt -days 1825 -sha256 -extfile intermediate_ca.conf -extensions v3_intermediate_ca
