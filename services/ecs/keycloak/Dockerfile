# ===== Build stage =====
FROM quay.io/keycloak/keycloak:latest AS builder

# ビルド時オプション：ヘルス/メトリクス有効化、DBベンダ設定（例）
ENV KC_DB=postgres

WORKDIR /opt/keycloak

# 重要：ヘルスをメインHTTPポート(8080)で返すためのビルド時フラグを付ける
# ついでに health/metrics もビルド時に有効化
RUN /opt/keycloak/bin/kc.sh build \
    --health-enabled=true \
    --metrics-enabled=true \
    --http-management-health-enabled=false

# ===== Runtime stage =====
FROM quay.io/keycloak/keycloak:latest
COPY --from=builder /opt/keycloak/ /opt/keycloak/
ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]