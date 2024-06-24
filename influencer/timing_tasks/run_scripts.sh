#!/usr/bin/env bash

# 运行定时脚本
source /www/wwwroot/influencer-mgr-be/venv/bin/activate
/www/wwwroot/influencer-mgr-be/venv/bin/python /www/wwwroot/influencer-mgr-be/timing_tasks/flush_create_to_send_workflow.py
/www/wwwroot/influencer-mgr-be/venv/bin/python /www/wwwroot/influencer-mgr-be/timing_tasks/flush_know_intent_category_to_next_workflow.py
/www/wwwroot/influencer-mgr-be/venv/bin/python /www/wwwroot/influencer-mgr-be/timing_tasks/flush_sended_to_invite_sample_workflow.py
# echo "Hello world!"