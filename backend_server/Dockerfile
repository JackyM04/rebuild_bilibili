# 使用 Python 3.10.14 作为基础镜像
FROM python:3.10.14

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到容器的 /app 目录
COPY . .

# # 安装应用程序的依赖项
RUN pip install --no-cache-dir -r req.txt

# 暴露应用程序的端口
EXPOSE 8085

ENV API_PORT=8085
ENV ROOM_ID=27526833
ENV EXPIRATION_TIME=259200


# 设置容器启动时执行的命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8085"]
