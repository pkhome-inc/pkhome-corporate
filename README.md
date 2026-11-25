# PKHOME corporate site

PKHOME株式会社 コーポレートサイト（静的 HTML）。

- 公開: GitHub Pages（`.github/workflows/pages.yml`、main への push で自動デプロイ）
- 編集対象: `index.html`、`sumusumu/index.html`
- 独自ドメイン: `CNAME`（pkhome.co.jp）
- 公開 URL: https://pkhome.co.jp

## FUNDIA の表示切替

- FUNDIA 部分には `data-fundia` の目印が付いている。`<html data-fundia="off">` で非表示、`"on"` で表示（文言は消していない）
- 切替: Actions →「FUNDIA 表示切替」→ Run workflow で off / on を選ぶ（コミットと公開まで自動）
- 確認用: https://pkhome.co.jp/?fundia=1 でその場だけ表示
