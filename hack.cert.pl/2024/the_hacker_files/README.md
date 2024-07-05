# The Hacker Files - forensics

### Task

W zadaniu załączony jest memdump (Ubuntu 24.04 6.8.0-31-generic), który ma w sobie historie wygenerowania klucza do LUKS-encrypted dysku.

### Solution

Volatility (2 i 3) nie posiadają profili dla kernela w wersji 6.8.0-31, dlatego trzeba wygenerować profil dla [vol2](https://andreafortuna.org/2019/08/22/how-to-generate-a-volatility-profile-for-a-linux-system/) i vol3.

Klonując repo [volatility](https://github.com/volatilityfoundation/volatility), użyć trzeba PR'a który implementuje nową wersję dwarfa ([#854](https://github.com/volatilityfoundation/volatility/pull/854)):

```bash
$ git fetch origin pull/854/head:dwarf-5
$ git checkout dwarf-5
```

Używając pluginu `linux_bash` z *volatility3* dostajemy historię z basha:

```bash
(venv) root@vm:/home/user/volatility3# python3 vol.py -f /home/user/memory.elf linux.bash.Bash
Volatility 3 Framework 2.7.1
Progress:  100.00		Stacking attempts finished                  
PID	Process	CommandTime	Command

[...]
6427	bash	2024-06-18 09:16:46.000000 	sudo dpkg -i ~/Downloads/google-chrome-stable_current_amd64.deb
6427	bash	2024-06-18 09:16:49.000000 	sudo apt install irssi cryptsetup pwgen
6427	bash	2024-06-18 09:17:23.000000 	pwgen -s 32 1 > /dev/shm/secret.txt
6427	bash	2024-06-18 09:17:25.000000 	read -r -s pwd
6427	bash	2024-06-18 09:17:29.000000 	(echo $pwd; cat /dev/shm/secret.txt) | tr -d '\n' | sudo cryptsetup luksFormat /dev/vdb -
6427	bash	2024-06-18 09:17:51.000000 	(echo $pwd; cat /dev/shm/secret.txt) | tr -d '\n' | sudo cryptsetup luksOpen /dev/vdb crypt -
6427	bash	2024-06-18 09:18:01.000000 	pwd=""
6427	bash	2024-06-18 09:18:03.000000 	sudo mkfs.ext4 /dev/mapper/crypt
6427	bash	2024-06-18 09:18:06.000000 	sudo mount /dev/mapper/crypt /mnt
6427	bash	2024-06-18 09:18:08.000000 	sudo chown hacker: /mnt
6427	bash	2024-06-18 09:18:09.000000 	irssi
6427	bash	2024-06-18 09:22:13.000000 	rm /mnt/flag.txt
6427	bash	2024-06-18 09:22:14.000000 	sudo umount /mnt
6427	bash	2024-06-18 09:22:16.000000 	sudo dd if=/dev/zero of=/dev/vda bs=4M
```

Hacker postanawia wygenerować hasło i zapisać je do `/dev/shm`, który jest tmpfs'owym mountem, aby odzyskać to hasło, trzeba zpatchować plugin `linux_tmpfs`, żeby korzystał z nowych `hlist` ([linux_tmpfs.patch](./linux_tmpfs.patch)).

```bash
(venv) root@vm:/home/user/volatility# python2 vol.py --profile=LinuxUbuntu_6_8_0-31-generic_profilex64 -f ../memory.elf linux_tmpfs -L
Volatility Foundation Volatility Framework 2.6.1
WARNING : volatility.debug    : Overlay structure cpuinfo_x86 not present in vtypes
WARNING : volatility.debug    : Overlay structure cpuinfo_x86 not present in vtypes
1 -> /home
2 -> /usr/lib/x86_64-linux-gnu
3 -> /usr/lib/x86_64-linux-gnu
4 -> /usr/share
5 -> /usr/share
6 -> /dev/shm
7 -> /
8 -> /snap/snapd-desktop-integration/157
9 -> /run/lock
10 -> /run/user/1000
11 -> /
12 -> /snap/firefox/4173/data-dir/icons
13 -> /snap/firefox/4173/data-dir/themes
14 -> /dev
15 -> /dev
16 -> /dev
17 -> /snap/firefox/4173/data-dir/sounds
18 -> /dev
19 -> /usr/local/share
20 -> /dev
21 -> /dev
(venv) root@vm:/home/user/volatility# python2 vol.py --profile=LinuxUbuntu_6_8_0-31-generic_profilex64 -f ../memory.elf linux_tmpfs -D ./dump -S 6
Volatility Foundation Volatility Framework 2.6.1
WARNING : volatility.debug    : Overlay structure cpuinfo_x86 not present in vtypes
WARNING : volatility.debug    : Overlay structure cpuinfo_x86 not present in vtypes

[...omitted for brevity...]

('x', '.com.google.Chrome.8T5m61')
('x', [CType _linux_tmpfs__i_atime] @ 0xFFFF9FC84DB1F270)
.com.google.Chrome.8T5m61
('x', 'secret.txt')
('x', [CType _linux_tmpfs__i_atime] @ 0xFFFF9FC8425C4408)
secret.txt
^CInterrupted
(venv) root@vm:/home/user/volatility# cat ./dump/secret.txt 
Cwm5qGCIUqmMh1buogqNQq8RkvSj42yC
```

Aby odszyfrować dysk, potrzeba jeszcze zmienną `$pwd`, którą hacker postanowił wczytać z stdin.

Po zdumpowaniu pamięci basha (PID 6427), można wygenerować wszystkie możliwe klucze do zdecryptowania dysku:

```bash
(venv) root@vm:/home/user/volatility3# python vol.py -f ../memory.elf linux.proc.Maps --pid=6427 --dump
Volatility 3 Framework 2.7.1
Progress:  100.00		Stacking attempts finished                  
PID	Process	Start	End	Flags	PgOff	Major	Minor	Inode	File Path	File output

6427	bash	0x5f6b57658000	0x5f6b57688000	r--	0x0	253	2	262702	asdf	pid.6427.vma.0x5f6b57658000-0x5f6b57688000-1.dmp
[...]
6427	bash	0x7ffd7dfc1000	0x7ffd7dfc3000	r-x	0x0	0	0	0	asdf	pid.6427.vma.0x7ffd7dfc1000-0x7ffd7dfc3000-1.dmp
(venv) root@vm:/home/user/volatility3# strings -n 5 *.dmp | grep -i '^[A-Za-z0-9]*$' | sort | uniq | sed -e 's/$/Cwm5qGCIUqmMh1buogqNQq8RkvSj42yC/' > /tmp/brute.txt
```

Mając listę wszystkich potencjalnych kluczy, możemy je wszystkie przetestować używając [bruteforce-luks](https://github.com/glv2/bruteforce-luks):

```bash
root@vm:/home/user# losetup /dev/loop0 pendrive.img
root@vm:/home/user/bruteforce-luks# ./bruteforce-luks -t 4 -f /tmp/brute.txt -v 1 /dev/loop0
Warning: using dictionary mode, ignoring options -b, -e, -l, -m and -s.

Tried passwords: 0
Tried passwords per second: 0.000000
Last tried password: 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000Cwm5qGCIUqmMh1buogqNQq8RkvSj42yC

[...]

Tried passwords: 982
Tried passwords per second: 0.899408
Last tried password: iconvCwm5qGCIUqmMh1buogqNQq8RkvSj42yC

Password found: hunter2Cwm5qGCIUqmMh1buogqNQq8RkvSj42yC
root@vm:/home/user/bruteforce-luks# echo -n "hunter2Cwm5qGCIUqmMh1buogqNQq8RkvSj42yC" | cryptsetup luksOpen /dev/loop0 crypt
root@vm:/home/user/bruteforce-luks# extundelete --restore-all /dev/mapper/crypt
NOTICE: Extended attributes are not restored.
Loading filesystem metadata ... 1 groups loaded.
Loading journal descriptors ... 22 descriptors loaded.
Searching for recoverable inodes in directory / ... 
1 recoverable inodes found.
Looking through the directory structure for deleted files ... 
1 recoverable inodes still lost.
root@vm:/home/user/bruteforce-luks# cat RECOVERED_FILES/file.12 
                                                                _|  
                                          _|_|    _|  _|      _|    
  _|_|      _|_|_|    _|_|_|    _|_|_|  _|    _|  _|  _|      _|    
_|_|_|_|  _|        _|_|      _|            _|    _|_|_|_|  _|      
_|        _|            _|_|  _|          _|          _|      _|    
  _|_|_|    _|_|_|  _|_|_|      _|_|_|  _|_|_|_|      _|      _|    
                                                                _|  
                                                                    
                                                                        
_|      _|                                  _|_|    _|_|_|      _|_|_|  
  _|  _|    _|_|    _|    _|  _|  _|_|    _|    _|  _|    _|  _|        
    _|    _|    _|  _|    _|  _|_|        _|    _|  _|_|_|      _|_|    
    _|    _|    _|  _|    _|  _|          _|    _|  _|              _|  
    _|      _|_|      _|_|_|  _|            _|_|    _|        _|_|_|    
                                                                        
                                    _|_|_|_|_|                          
                                                                        
_|_|_|_|    _|_|_|        _|                                    _|      
_|        _|                    _|_|_|    _|_|_|      _|_|    _|_|_|_|  
_|_|_|    _|              _|  _|_|        _|    _|  _|    _|    _|      
_|        _|              _|      _|_|    _|    _|  _|    _|    _|      
_|_|_|_|    _|_|_|        _|  _|_|_|      _|    _|    _|_|        _|_|  
                                                                        
                _|_|_|_|_|          _|_|_|_|_|                          
                                                                      
                              _|                              _|      
            _|_|_|    _|_|        _|_|_|      _|_|_|        _|_|_|_|  
          _|    _|  _|    _|  _|  _|    _|  _|    _|          _|      
          _|    _|  _|    _|  _|  _|    _|  _|    _|          _|      
            _|_|_|    _|_|    _|  _|    _|    _|_|_|            _|_|  
                _|                                _|                  
_|_|_|_|_|  _|_|                              _|_|    _|_|_|_|_|      
                                                      _|  _|      
                  _|_|  _|                          _|      _|    
  _|_|          _|      _|  _|    _|            _|  _|      _|    
_|    _|      _|_|_|_|  _|  _|    _|                _|        _|  
_|    _|        _|      _|  _|    _|                _|      _|    
  _|_|          _|      _|    _|_|_|            _|  _|      _|    
                                  _|                  _|  _|      
      _|_|_|_|_|              _|_|    _|_|_|_|_|                  
root@vm:/home/user/bruteforce-luks# # ecsc24{Your_OPSEC_is_not_going_to_fly_:(}
```
