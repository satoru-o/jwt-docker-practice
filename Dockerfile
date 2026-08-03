FROM alpine:3.20

RUN apk add --no-cache curl busybox-extras

# 非rootユーザー・グループ作成
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

RUN mkdir -p /www && chown -R appuser:appgroup /www

USER appuser
WORKDIR /www

CMD ["sh", "-c", "echo \"Hello from $(hostname)\" > /www/index.html && httpd -f -p 80 -h /www"]