#! /bin/bash
set -euo pipefail

echo "==> Starting RealSmile lab bootstrap..."

# --- Step 1: minikube ---
echo "==> Starting minikube..."
minikube start --driver=docker --cpus=4 --memory=6144
minikube addons enable ingress
minikube addons enable metrics-server

# --- Step 2: Ansible ---
echo "==> Running Ansible playbook..."
ansible-playbook -i ansible/inventory.ini ansible/playbook.yml

# --- Step 3: Build app image ---
echo "==> Building app image..."
eval $(minikube docker-env)
docker build -t realsmile-backend:latest ./app

# --- Step 4: Deploy app with Helm ---
echo "==> Deploying RealSmile app..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana-community https://grafana-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
 
helm upgrade --install realsmile ./realsmile-chart -n realsmile

# --- Step 5: Prometheus + Grafana ---
echo "==> Installing Prometheus + Grafana..."
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack \
  -n monitoring \
  -f monitoring/monitoring-values.yaml

# --- Step 6: Loki + Alloy ---
echo "==> Installing Loki..."
helm upgrade --install loki grafana-community/loki \
  -n logging \
  -f monitoring/loki-values.yaml

echo "==> Installing Alloy..."
helm upgrade --install alloy grafana/alloy \
  -n logging \
  -f monitoring/alloy-values.yaml

# --- Done ---
echo ""
echo "==> Bootstrap complete. Stack is up."
echo ""
echo "    App:        kubectl port-forward svc/realsmile-backend 8000:8000 -n realsmile &"
echo "    Grafana:    kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring &"
echo "    Prometheus: kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090:9090 -n monitoring &"
echo ""
echo "    Grafana login: admin / realsmile-admin"