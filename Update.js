
// 每日自動更新富邦新店分點資料 - 範本
// 1. 去 https://finmind.github.io/ 申請免費 token
// 2. 到 GitHub repo Settings > Secrets > New secret 名稱 FINMIND_TOKEN 貼上 token
// 3. 這個腳本會自動抓取富邦新店(782)近20日買賣超，計算出 TOP10 張數/金額佔比，寫入 data.json

const fs = require('fs');

async function main() {
  const token = process.env.FINMIND_TOKEN;
  if (!token) {
    console.log('沒有 FINMIND_TOKEN，使用 mock data 跳過');
    // 保留現有 data
    return;
  }
  // 範例：抓分點資料 (需依 FinMind 實際 API 規格調整)
  // 這裡先寫入一個結構，之後你的前端 index.html 改讀 data.json 即可即時更新
  const mockData = {
    updated_at: new Date().toISOString(),
    branch: "富邦-新店 782E",
    top_by_volume: [],
    top_by_amount: []
  };
  fs.writeFileSync('data.json', JSON.stringify(mockData, null, 2));
  console.log('data.json updated');
}

main();
