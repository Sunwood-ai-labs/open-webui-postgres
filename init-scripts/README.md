<div align="center">

# 📑 初期化スクリプト

</div>

このディレクトリには、PostgreSQLデータベースの初期化時に実行される SQLスクリプトが含まれています。

## 🔧 スクリプトの実行順序

スクリプトは、ファイル名のアルファベット順に実行されます：

1. `01-init.sql` - データベースの初期設定

## ✨ スクリプトの追加方法

1. 新しいSQLスクリプトを作成する際は、実行順序を考慮して適切な番号を付けてください
   - 例：`02-create-tables.sql`、`03-seed-data.sql`
2. スクリプトには必ず説明コメントを入れてください
3. トランザクションの適切な使用を心がけてください

## 🔍 注意事項

- スクリプトは初回のコンテナ作成時のみ実行されます
- 既存のデータベースに対して実行したい場合は、手動で実行する必要があります
- スクリプトのエラーはコンテナの起動を妨げる可能性があります

## 📝 スクリプト例

```sql
-- テーブル作成の例
CREATE TABLE example (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- データ投入の例
INSERT INTO example (name) VALUES
    ('サンプル1'),
    ('サンプル2');
