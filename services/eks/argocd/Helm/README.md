## インストール
```
helm repo add argo https://argoproj.github.io/argo-helm

helm repo update

helm upgrade -i argo-cd argo/argo-cd \
  --namespace argocd --create-namespace \
  --set server.insecure=true \
  --set applicationSet.enabled=true
```


## ingress作成
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: argocd-server-ingress
  namespace: argocd
  annotations:
    kubernetes.io/ingress.class: "alb"
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/healthcheck-path: /healthz
    alb.ingress.kubernetes.io/success-codes: "200"
spec:
  ingressClassName: alb
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: argo-cd-argocd-server
                port:
                  number: 80
```


## values.yaml
```
configs:
  params:
    server.insecure: "true"
```


## 適用
```
helm upgrade -i argo-cd argo/argo-cd   -n argocd   -f values.yaml
    
kubectl -n argocd rollout restart deploy/argo-cd-argocd-server 
```


## パスワード取得
```
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo
```