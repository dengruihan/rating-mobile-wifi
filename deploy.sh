#!/bin/bash

echo "======================================"
echo "  WiFi 评分系统 - 远程服务器启动脚本"
echo "======================================"
echo ""

# 检查并停止已运行的服务
echo "检查并停止已运行的服务..."
pkill -f "python manage.py runserver" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 2

# 创建日志目录
mkdir -p logs

echo ""
echo "======================================"
echo "  启动后端服务 (Django)"
echo "======================================"
cd wifirating
python manage.py runserver 0.0.0.0:8001 > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "后端服务已启动，PID: $BACKEND_PID"
echo "后端日志: logs/backend.log"
echo "后端地址: http://0.0.0.0:8001/"
echo "管理员页面: http://0.0.0.0:8001/admin/"
cd ..

sleep 3

echo ""
echo "======================================"
echo "  启动前端服务 (Vue)"
echo "======================================"
cd wifi-rating-app
npm run dev -- --host 0.0.0.0 --port 5179 > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "前端服务已启动，PID: $FRONTEND_PID"
echo "前端日志: logs/frontend.log"
cd ..

sleep 3

echo ""
echo "======================================"
echo "  所有服务已启动！"
echo "======================================"
echo "后端地址: http://110.40.153.38:8001/"
echo "前端地址: http://110.40.153.38:5173/"
echo ""
echo "查看日志:"
echo "  后端: tail -f logs/backend.log"
echo "  前端: tail -f logs/frontend.log"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo "======================================"

# 等待用户中断
trap "echo ''; echo '正在停止所有服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '所有服务已停止'; exit 0" INT TERM

wait
