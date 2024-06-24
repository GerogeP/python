#!/bin/bash  
    
if ! lsof -i:6006 | awk 'NR>1 {print $2}' | xargs kill -15; then  
  echo "Killing process on port 6006 failed, reloading supervisor..."  
  sudo supervisorctl reload  
else  
  echo "Process on port 6006 was successfully killed. Please wait to start!"  
fi
