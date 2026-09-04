# jwt-docker-practice

JWT（RS256）の発行・検証をDocker上で試す練習リポジトリです。
`issuer`（秘密鍵で署名・発行）と `verifier`（公開鍵で検証のみ）を別コンテナに分け、
`docker-compose up` で両方起動して `/login` → `/protected` や `/verify` を叩けます。

> [!NOTE]
> このリポジトリは個人の学習記録です。フォーク・Star等は自由にどうぞですが、
> PR・Issueは受け付けていません。
