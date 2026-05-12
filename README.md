# scripts-to-systems-lab

Local lab environment for the [From Scripts to Systems](https://jiminbyun.medium.com/from-scripts-to-systems-making-automation-actually-work-in-production-2509d5c4fde5) series.

Runs the full RealSmile stack locally — Kubernetes, Prometheus, Grafana, Loki, Alloy — on minikube.

---

## Prerequisites

Install these before running `bootstrap.sh`. Verify each with the command shown.

| Tool | Verify | Install |
|------|--------|---------|
| Docker | `docker --version` | [docs.docker.com](https://docs.docker.com/get-docker/) |
| Python 3 | `python3 --version` | [python.org](https://www.python.org/downloads/) |
| minikube | `minikube version` | [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io/docs/start/) |
| kubectl | `kubectl version --client` | [kubernetes.io](https://kubernetes.io/docs/tasks/tools/) |
| Helm | `helm version` | [helm.sh](https://helm.sh/docs/intro/install/) |
| Ansible | `ansible --version` | `pip3 install ansible --break-system-packages` |
| Terraform | `terraform version` | [developer.hashicorp.com](https://developer.hashicorp.com/terraform/install) |

> WSL users: Install Docker Desktop for Windows and enable WSL integration.
> Docker Desktop → Settings → Resources → WSL Integration → enable your distro.

---

## Quickstart

```bash
git clone https://github.com/JiminByun0101/scripts-to-systems-lab.git
cd scripts-to-systems-lab
bash bootstrap.sh
```

Bootstrap takes 5–10 minutes on first run. When it finishes, run the port-forwards it prints and open Grafana at `http://localhost:3000`.

---

## What Gets Installed

| Component | Namespace | Purpose |
|-----------|-----------|---------|
| RealSmile FastAPI app | `realsmile` | Sample backend — exposes `/health` and `/metrics` |
| kube-prometheus-stack | `monitoring` | Prometheus + Grafana + Alertmanager |
| Loki | `logging` | Log aggregation |
| Alloy | `logging` | Log shipping agent (DaemonSet) |
| Terraform | — | Grafana resources as code (Part 6) |
| rollback-controller | `monitoring` | Webhook receiver — rolls back realsmile on `HighPaymentFailureRate` alert |

---

## Access

After bootstrap, run these port-forwards:

```bash
# App
kubectl port-forward svc/realsmile-backend 8000:8000 -n realsmile &

# Grafana
kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring &

# Prometheus
kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090:9090 -n monitoring &

# Alertmanager
kubectl port-forward svc/monitoring-kube-prometheus-alertmanager 9093:9093 -n monitoring &
```

| Service | URL | Login |
|---------|-----|-------|
| Grafana | http://localhost:3000 | admin / realsmile-admin |
| Prometheus | http://localhost:9090 | — |
| App | http://localhost:8000/health | — |
| Alertmanager | http://localhost:9093 | — |

---
 
## After Bootstrap
 
Loki datasource is not configured automatically. Add it in Grafana after bootstrap:
 
1. Open `http://localhost:3000` → **Connections → Data Sources → Add new data source → Loki**
2. URL: `http://loki.logging.svc.cluster.local:3100`
3. **Save & Test** — you should see "Data source successfully connected."
To verify logs are flowing, go to **Explore → Loki**, switch to **Code** mode, and run:
 
```
{namespace="realsmile"}
```
 
---

## Series

| Part | Title |
|------|-------|
| 0 | [Why your scripts are stuck in the backlog](https://jiminbyun.medium.com/from-scripts-to-systems-making-automation-actually-work-in-production-2509d5c4fde5) |
| 0.5 | [Setting Up the Lab](https://medium.com/@jiminbyun/from-scripts-to-systems-building-the-automation-that-thinks-0-5-0c2482f32cdf) |
| 1 | [PR triage is breaking under volume](https://jiminbyun.medium.com/from-scripts-to-systems-building-the-automation-that-thinks-1-31470a2103c4) |
| 2 | [Deployments need a human watching Grafana](https://jiminbyun.medium.com/from-scripts-to-systems-building-the-automation-that-thinks-2-c4e01657941e) |
| 3 | Log patterns are going undetected — coming soon |
| 4 | On-call starts every incident from scratch — coming soon |
| 5 | Preview environments are created by hand — coming soon |
| 6 | Alert rules live in Grafana UI, nowhere else — coming soon |
| 7 | Making It Production-Ready — coming soon |