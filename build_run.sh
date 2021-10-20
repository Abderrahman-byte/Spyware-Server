#! /bin/bash

echo "[BUILD]" && python3 -m pip install -e . && echo -e "\n[EXECUTE]" && python3 -m spyware_server