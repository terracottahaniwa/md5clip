# md5clip
<p>
  put base64 encoded md5 digest to clipboard.<br>
  clipboard will cleared when after 10sec.<br>
</p>

<p>
  code is same as:<br>
  will be the same as the result of the command on linux:<br>
  read -s ; echo -n $REPLY | md5sum | awk '{printf $1}' | base64<br>
</p>

### build
<p>
  pyinstaller -w --icon=md5clip.ico md5clip.pyw
</p>

### install and usage:
<p>
  clone or download zip from this repo. (and decompress zip)<br>
  execute ./dist/md5clip/md5clip.exe<br>
  or command on console "python md5clip.pyw"<br>
</p>

### screenshot:
<p>
  
  ![screenshot1](screenshot/screenshot1.png "screenshot1")
  
  ![screenshot2](screenshot/screenshot2.png "screenshot2")
</p>

### icon's license:
<p>
  Creative Commons Attribution-Share Alike 4.0 International License<br>
  https://commons.wikimedia.org/wiki/File:Eo_circle_grey_hash.svg<br>
</p>
