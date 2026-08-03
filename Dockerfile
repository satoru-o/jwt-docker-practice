FROM alpine:3.20

RUN apk add --no-cache curl

# 非rootユーザー・グループ作成
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

USER appuser

CMD [ "sleep", "infinity" ]