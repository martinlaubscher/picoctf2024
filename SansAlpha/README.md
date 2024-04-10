# SansAlpha Writeup

Points: 400<br>
Challenge Author: syreal

Description:<br>
The Multiverse is within your grasp! Unfortunately, the server that contains the secrets of the multiverse is in a universe where keyboards only have numbers and (most) symbols.

Hint:<br>
Where can you get some letters?

## Solution

In this challenge, we are presented with the task to find the flag using a shell where we can't enter any letters (also no backslash \), so we need to find some way to get characters otherwise. However, we can use symbols such as ```*```.<br>
After some googling, I found this post that how we can redirect an error message to std out and use the characters to build a command:<br>
https://www.commandlinefu.com/commands/view/11698/launch-bash-without-using-any-letters

The string we are working with is ```bash: -: command not found: command not found```.<br>
Looking at the letters, we can see that it contains the letters for two very useful commands: ```cd``` and ```cat```.<br>

Using string slicing (and since the ```*``` symbol is allowed), we can build a ```cat *``` command to see what's in the directory we're at:
```"$(- 2>&1)";${_:9:1}${_:1:1}${_:19:1} *```<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/b2c357d6-415f-4681-afbe-bb4384c24d1d)

We get a lovely text but no flag. We also see that there is a directory, blargh. Let's check that directory! But we don't have the characters... Luckily, we can use wildcards. Since there is no other directory, we can use ```??a*``` (since we have an ```a``` in our string).<br>
With this, we can now change to the blargh directory:<br>
```"$(- 2>&1)";${_:9:1}${_:15:1} ??${_:1:1}*```<br>
And run cat * again, as before:<br>
```"$(- 2>&1)";${_:9:1}${_:1:1}${_:19:1} *```<br>
And there it is, our dear flag:<br>
```picoCTF{7h15_mu171v3r53_15_m4dn355_8b3d83ad}```<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/9ebdb40f-ec8a-437a-8995-97dd0682a42d)

