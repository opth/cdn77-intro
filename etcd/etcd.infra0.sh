#!/bin/bash
( ( nohup etcd --name infra0 --initial-advertise-peer-urls http://172.77.0.10:2380 \
  --listen-peer-urls http://172.77.0.10:2380 \
  --listen-client-urls http://172.77.0.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://172.77.0.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://172.77.0.10:2380,infra1=http://172.77.0.11:2380,infra2=http://172.77.0.12:2380 \
  --initial-cluster-state new \
  --listen-metrics-urls http://172.77.0.10:2381 \
  --metrics extensive ) & )