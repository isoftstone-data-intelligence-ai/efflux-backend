#!/bin/bash

# 配置
privateKeyPath="~/Documents/AI-key.pem"
remoteHost="root@47.236.204.213"
imageName="registry.cn-zhangjiakou.aliyuncs.com/other1/efflux-backend:1.0.3"

# 登录阿里云容器镜像服务
#echo "Logging into Alibaba Cloud Container Registry..."
docker login --username=yourusername --password=yourpassword registry.cn-hangzhou.aliyuncs.com

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
docker ps -q --filter ancestor=$imageName | xargs -r docker stop
docker ps -a -q --filter ancestor=$imageName | xargs -r docker rm
docker run -d --name efflux-backend --restart unless-stopped -p 8000:8000 ${imageName}
EOF

echo "Deployment completed."