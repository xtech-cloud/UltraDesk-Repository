# 快速开始

运行link.bat建立Repository目录的软链接

安装以下python依赖包
 - colorlog
 - flask

运行以下脚本
```python
python run.py
```

访问 http://localhost/source_windows.json 获取源

# volume文件结构说明
```
|- volume
  |- applications
    |- {os}
      |- {Application}
        |- {Application}_{version}.7z
        |- meta.json
  |- source_{os}.json
```

{os}的值集合为[windows]
meta.json的内容，当前版本为空文件。

如果volume/source_{os}.json不存在，服务启动后会自动生成。
如果volume/applications目录下更新了Application，需要手动删除volume/source_{os}.json文件并重启服务重新生成。

例如添加一个Chrome的120.0.6099.130的版本，volume的结构如下
```
|- volume
  |- applications
    |- windows
      |- Chrome
        |- Chrome_120.0.6099.130.7z
        |- meta.json
```

# 同步到远程

## 七牛云

使用以下命令进行工具授权。

```
tools\qshell.exe account AK SK name
```

其中AK和SK从七牛云的个人中心>密钥管理中获取，name是当前账号的备注名。

在.qiniu文件夹下创建config.json文件，内容如下

```json
{
	"src_dir": "D:/UltraDesk-Repository/volume", 
	"bucket": "ultradesk-repository",
	"overwrite": true,
	"check_exists": true,
	"check_hash": true, 
	"rescan_local": true
}
```

src_dir填写volume的绝对路径，bucket填写七牛云中对应的存储桶。
配置文件的说明在 https://github.com/qiniu/qshell/blob/master/docs/qupload.md 。

运行SyncToQiniu.bat开始同步。
