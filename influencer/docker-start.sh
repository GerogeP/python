#!/bin/bash  
  
is_service_running() {  
    local service_name="$1"  
    local container_id=$(docker ps -q --filter "name=$service_name")  
    if [ -n "$container_id" ]; then  
        return 0 # 服务正在运行  
    else  
        return 1 # 服务没有运行  
    fi  
}  
  
SERVICE_NAME=$1

# 检查服务是否正在运行  
if ! is_service_running "$SERVICE_NAME"; then  
    echo "Service $SERVICE_NAME is not running, starting it..."  
    docker-compose up -d "$SERVICE_NAME"  
else  
    echo "Service $SERVICE_NAME is already running, restart it..."  
    docker-compose restart "$SERVICE_NAME"  
fi