# KeyTypeUploadFile
用键盘将小数据传输到远程机器

经常在项目上遇到这样的问题，由于vpn或者防火墙限制远程连接到服务器时不能进行粘贴复制文本。本机改好的代码还需要在远程机上在敲一遍，并且不能传输文件，每次传输东西都要找管理员给传输文件很麻烦，所以想到了这样一个又蠢又灵活的办法进行粘贴复制，先说明本脚本不适合以下需求，如果有以下需求请直接跳过该文章去找更好的解决方案：

* 不适合传输大文件，如果文件超过100KB，该脚本不适合你,还是去找管理员进行传输
* 如果追求高效率，该脚本不适合
* 仅支持单向传输，即由本机传输到远程机，如果需要从远程机迁移数据到本机，请想其他办法

只适合以下几种情况

* 粘贴文字
* 传输极小的文件
* 单向传输，从本机到远程机

说下实现原理，当我们多层远程时，并且有防火墙或者vpn 限制时不能粘贴文件或者字符串，也无法实现网络穿透，远程过去我们只能用鼠标和键盘进行数据编辑。所以该脚本就是将要传输的数据用自动打字的方式进行传输的。说白一点，文件都是二进制0101组成的的，既然限制了传输文件。那干脆在远程机器用键盘自动敲出0101这些字符然后还原就好了，当然了敲0101这些字节码有点夸张但是我们可以打base64过去。所以这就限制了传输的文件不能太大，不然要敲到猴年马月，当然如果你有足够的耐心等待也是可以实现的，但是极其不建议这样做，非常容易出错中断，除非你是真没有办法了，可以尝试下。

**总而言之原理就是将文件转成base64字符串用键盘在远程机把数据敲出来，然后在进行还原，还原base64可以使用powershell脚本或者shell,python等**

该脚本使用python3 编写，请确保自己的机器上有python 并安装好，并且pip装好pynput
```python
   pip install pynput
```
功能

+ 该脚本可以直接传输文字，但是要注意文字不能中英文符号混合
+ 可以将要传输的文字保存在文件里然后传输过去
+ 可以开始或者暂停传输，可以自定义按键，默认是 **左Ctrl** 键开始或暂停
+ Esc 键退出程序


传入到远程电脑后如果是windows 可以用powershell 脚本（程序附带了一个小脚本，可以用type_str方法传到远程服务器）读取base64字符串将其转换成文件
# 使用方法
## 调用 type_file 方法传输文件，文件最好压缩下，能节省时间
```python
    src_file_path = 'testfile.zip'
    type_file(src_file_path, one_step_len=30, step_interval=0.2)
```
## 调用type_str 方法传输文字，切不可中英混合
```python
    instr = """test word """
    type_str(instr)
```
## 在远程机解码base64 字符串文件
liunx 下
```python

   b64str2file("frombase64str.txt", "origfile.zip")
```
windows 下使用PowerShellB4SFile.ps1 脚本将包含base64字符串的文件转化成原始文件，脚本内容如下
```powershell
$from_file  = "base64str.txt"
$to_file    =  "recoverfile.zip"
$b64        = Get-Content $from_file
$bytes      = [Convert]::FromBase64String($b64)
[IO.File]::WriteAllBytes($to_file, $bytes)
```
