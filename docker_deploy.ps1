# 配置
$privateKeyPath = "C:\Users\ASUS\Downloads\AI-key.pem"
$remoteHost = "root@47.236.204.213"
$imageName = "registry.cn-zhangjiakou.aliyuncs.com/other1/efflux-backend:1.0.3"

# 构建 Docker 镜像
Write-Output "Building Docker image..."
docker build -t $imageName .

# 登录阿里云容器镜像服务
echo "Logging into Alibaba Cloud Container Registry..."
docker login --username=yourusername --password=yourpassword registry.cn-zhangjiakou.aliyuncs.com

# 推送镜像
Write-Output "Pushing Docker image to Alibaba Cloud Container Registry..."
docker push $imageName

# 使用SSH在远程服务器上拉取并运行镜像
Write-Output "Deploying to remote server..."

ssh -i ${privateKeyPath} ${remoteHost} "docker pull ${imageName}"
# 停止并删除正在运行的容器（如果存在）
ssh -i ${privateKeyPath} ${remoteHost} "docker ps -q --filter ancestor=$imageName | xargs -r docker stop"
ssh -i ${privateKeyPath} ${remoteHost} "docker ps -a -q --filter ancestor=$imageName | xargs -r docker rm"
ssh -i ${privateKeyPath} ${remoteHost} "docker run -d --restart unless-stopped -p 8000:8000 ${imageName}"
Write-Output "Deployment completed."