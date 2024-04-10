# Blast From the Past Writeup

Points: 300<br>
Challenge Author: syreal

Description:<br>
The judge for these pictures is a real fan of antiques. Can you age this photo to the specifications? Set the timestamps on this picture to 1970:01:01 00:00:00.001+00:00 with as much precision as possible for each timestamp. In this example, +00:00 is a timezone adjustment. Any timezone is acceptable as long as the time is equivalent. As an example, this timestamp is acceptable as well: 1969:12:31 19:00:00.001-05:00. For timestamps without a timezone adjustment, put them in GMT time (+00:00). The checker program provides the timestamp needed for each.<br>
Submit your modified picture here: nc -w 2 mimas.picoctf.net 63073 < original_modified.jpg<br>
Check your modified picture here: nc mimas.picoctf.net 57947

Hint:<br>
Exiftool is really good at reading metadata, but you might want to use something else to modify it.

## Solution

After downloading the picture, let's make a copy in case we mess up:<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/43e1bdb9-0fe5-453a-b63a-afb85c06b238)

Let's try to update all the timestamps to the required value using exiftools and check if that's enough to pass:<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/fdecde5e-2345-45a4-9509-55e792b523e9)

Unfortunately, we don't pass the last check! After a bit of googling, I found that exiftools cannot change that tag (https://exiftool.org/TagNames/Samsung.html#Trailer). I also couldn't find any other program that could, so the only solution I could come up with was to open the file in a hex editor (I used wxHexEditor) and change the value directly. Knowing that the relevant tag is in the trailer of the file, we can start checking the end - and there it is, an epoch timestamp that definitely isn't 1970.<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/610f3e22-e2af-4dab-970c-520b24ab2261)

So, we change that value to ```0000000000001``` save the file, and try again.<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/be75aae9-e93b-49fd-9395-071e64ac92ea)

![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/6dd86c49-9c73-4a1f-bda0-14ffc5b9f78a)

It worked, there is our flag:<br>
```picoCTF{71m3_7r4v311ng_p1c7ur3_a4f2b526}```<br>
