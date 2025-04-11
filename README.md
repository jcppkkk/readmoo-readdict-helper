# 讀墨嗜讀輔助工具

這是一個簡單的瀏覽器書籤工具（Bookmarklet），可以幫助你在讀墨網站上更明智地選擇使用嗜讀方案購買書籍。

## 功能

此工具會在讀墨購物車與代購清單中：

1. 計算每本書使用嗜讀方案的成本比例（以百分比顯示）
2. 將特別值得使用嗜讀方案購買的書籍（成本比例低於75%）以綠色高亮提示
3. 在每本書的價格旁邊顯示使用嗜讀方案的成本比例

## 嗜讀方案說明

讀墨嗜讀方案（999元/月）提供6點領書額度，依照每本書的價格需要不同點數：

- 0-250元 ➜ 1點
- 251-500元 ➜ 2點
- 501-750元 ➜ 3點
- 751-1000元 ➜ 4點
- 依此類推（每250元一階）

因此每點的成本約為166.67元，本工具會計算使用嗜讀領書的實際成本比例。

## 使用方法

1. 建立新的書籤
2. 名稱自訂（例如：「讀墨嗜讀輔助」）
3. 在網址欄位貼上以下程式碼：

```javascript
javascript:(function(){const PRICE_PER_POINT=999/6;const DISCOUNT_THRESHOLD=0.75;const getPointsNeeded=(price)=>{return Math.ceil(price/250);};const priceElements=document.querySelectorAll(".item-price-box .item-price");priceElements.forEach(el=>{const match=el.textContent.match(/NT\$ ?(\d+)/);if(!match)return;const price=parseInt(match[1],10);const points=getPointsNeeded(price);const cost=points*PRICE_PER_POINT;const discount=cost/price;if(discount<=DISCOUNT_THRESHOLD){el.style.backgroundColor="#c8facc";el.style.borderRadius="4px";el.style.padding="2px 4px";}const label=document.createElement("span");label.textContent=` (領書=${Math.round(discount*100)}%)`;label.style.color=discount<=DISCOUNT_THRESHOLD?"#0a8f3c":"#555";label.style.fontSize="0.9em";label.style.marginLeft="4px";el.appendChild(label);});})();
```

4. 儲存書籤
5. 當你在瀏覽讀墨的購物車或代購清單時，點擊此書籤即可看到效果

## 使用情境

- 查看購物車中哪些書籍最適合用嗜讀方案購買
- 規劃代購清單，挑選值得用嗜讀方案領取的書籍
- 快速計算嗜讀方案的實際折扣率

## 注意事項

- 本工具僅在讀墨網站的購物車與代購清單頁面有效
- 計算基於嗜讀方案999元6點的定價
- 標示綠色的書籍代表使用嗜讀方案特別划算（成本低於原價的75%）

## 開發者資訊

本專案使用模板系統和 pre-commit hooks 來保持 bookmarklet 程式碼的一致性。

### 專案結構
- `src/readmoo-readdict-helper.js`: 主要的源代碼文件
- `templates/index.html`: HTML 模板文件，包含網站結構和 bookmarklet 佔位符
- `scripts/update_bookmarklet.py`: 自動更新 bookmarklet 的腳本
- `index.html`: 最終生成的網站文件（由模板生成）

### 開發設置

1. 安裝 pre-commit
```bash
pip install pre-commit
```

2. 安裝 Jinja2 (用於模板)
```bash
pip install jinja2
```

3. 安裝 git hooks
```bash
pre-commit install
```

4. 修改源代碼
當你修改 `src/readmoo-readdict-helper.js` 或 `templates/index.html` 並提交變更時，
pre-commit hook 將自動更新 `index.html` 中的 bookmarklet 代碼。

你也可以手動運行更新腳本:
```bash
python scripts/update_bookmarklet.py
```

### 特性
- **精簡自動化**: 源 JavaScript 文件會被自動精簡並更新到 bookmarklet
- **冪等性**: 只有在源代碼發生變化時才會更新 HTML
- **快速跳過**: 如果源文件沒有變更，則跳過更新步驟
