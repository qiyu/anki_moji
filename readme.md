## 发布
1. 修改manifest.json的version为新的版本
2. 修改manifest.json的mod为当前时间，计算方法为 
   datetime.datetime.now().timestamp()
3. 执行命令
```bash
./deploy.sh
```