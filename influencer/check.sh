#!/bin/bash

get_env_value() {
  # 检查是否存在 .env 文件
  if [ -f ".env" ]; then
    # 读取 .env 文件中指定键的值
    local key="$1"
    local value=$(grep "^$key=" .env | cut -d '=' -f 2-)
    
    # 如果找到键值对则返回值，否则返回空字符串
    if [ -n "$value" ]; then
      echo "$value"
    else
      echo ""
    fi
  else
    echo ".env 文件不存在"
  fi
}

# 检查 port 设置
app_port=$(get_env_value "PORT")
if [ -n "$app_port" ]; then
  echo "键 PORT 的值为--> $app_port"
else
  app_port="6006"
  echo "找不到键 PORT，使用默认值--> $app_port"
fi

max_wait_time=30
app_url="http://localhost:$app_port/test"
# 循环等待应用启动
for ((i = 0; i < max_wait_time; i++)); do
  # 使用 curl 检测应用是否可访问
  response=$(curl -s -o /dev/null -w "%{http_code}" "$app_url" || true)

  # 如果应用返回 200（OK）则表示应用已经启动完成
  if [ "$response" -eq 200 ]; then
    echo "应用已经启动完成"
    break
  fi

  # 应用未启动完成，等待一秒钟后重试
  echo '...'
  sleep 1
done
# 如果超过最大等待时间仍然没有启动完成，输出错误信息
if [ "$i" -eq "$max_wait_time" ]; then
  echo "应用启动超时"
  exit 1
fi
