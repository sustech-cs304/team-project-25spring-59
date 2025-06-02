在``./``目录下运行以下指令启动后端
```shell
uvicorn backapp.main:app --host 0.0.0.0 --port 8000 --reload
```

访问 http://localhost:8000/docs 或者 http://localhost:8000/redoc 即可查看交互式API文档。