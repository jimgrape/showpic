# showpic
一个weechat的小插件，用于直接打开图床的图片，或者通过Mojo-weixin发送过来的图片


## Install

```
	$ it clone git@github.com:jimgrape/showpic.git ~/.weechat/python/
	$ cd ~/.weechat/python/autoload
	$ ln -s ../script.py
```

## Usage

```
	需要安装feh。Archliunx/Manjaro：sudo pacman -S feh

	傻瓜式操作，收到Mojo-weixin或者vim-cn图床的图片，自动打开。

```

## Setting
```
	如果想要关闭这个功能，输入/showpic off。重新打开，输入/showpic on。

	图片默认显示的时间为3秒，如果设置其他时间，输入/showpic showtime X

	在irc中，如果highlight才显示，输入/showpic showall off。如果所有都显示，输入/showpic showall on(默认)。

```
	
## License

GPL3 © 
