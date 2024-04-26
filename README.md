# 启动
## python依赖包
colorlog
flask
## 本机
python run.py

# volume结构
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
启动服务后，会自动生成volume/source_windows.json
