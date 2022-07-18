#!/usr/bin/env sh

var=${FLAG:-real_flag_here}

sed -i "s@real_flag_here@$var@g" /etc/nginx/conf.d/default.conf

nginx -g "daemon off;"
