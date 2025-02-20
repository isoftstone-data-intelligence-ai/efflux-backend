#!/bin/bash

# 配置
privateKeyPath="~/Documents/AI-key.pem"
remoteHost="root@47.236.204.213"
imageName="registry.cn-zhangjiakou.aliyuncs.com/other1/efflux-backend:1.0.0"

# 登录阿里云容器镜像服务
#echo "Logging into Alibaba Cloud Container Registry..."
#docker login --username=<your-aliyun-id> registry.cn-hangzhou.aliyuncs.com

# 构建 Docker 镜像
echo "Building Docker image..."
docker build -t $imageName .

# 推送镜像
echo "Pushing Docker image to Alibaba Cloud Container Registry..."
docker push $imageName

# 通过 SSH 在远程服务器上拉取并运行镜像
echo "Deploying to remote server..."
ssh -i ${privateKeyPath} ${remoteHost} << 'EOF'
docker pull $imageName
docker stop $(docker ps -q --filter ancestor=$imageName) || true && docker rm $(docker ps -a -q --filter ancestor=$imageName) || true
docker run -d -p 8001:8001 $imageName
EOF

echo "Deployment completed."