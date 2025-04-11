/**
 * 讀墨嗜讀輔助工具
 * 
 * 此書籤工具可幫助在讀墨購物車與代購清單頁面顯示使用嗜讀方案的成本比例
 */
(function () {
    // 嗜讀方案：每月999元可獲得6點
    const PRICE_PER_POINT = 999 / 6;

    // 折扣閾值：低於此比例的書會被標記為特別划算
    const DISCOUNT_THRESHOLD = 0.75;

    /**
     * 計算書籍價格所需的點數
     * @param {number} price - 書籍價格（新台幣）
     * @returns {number} - 所需點數
     */
    const getPointsNeeded = (price) => {
        return Math.ceil(price / 250);
    };

    // 找出所有價格元素
    const priceElements = document.querySelectorAll(".item-price-box .item-price");

    // 處理每個價格元素
    priceElements.forEach(el => {
        // 解析價格文字（格式如 "NT$ 350"）
        const match = el.textContent.match(/NT\$ ?(\d+)/);
        if (!match) return;

        const price = parseInt(match[1], 10);
        const points = getPointsNeeded(price);
        const cost = points * PRICE_PER_POINT;
        const discount = cost / price;

        // 如果折扣夠低（特別划算），使用綠色背景標示
        if (discount <= DISCOUNT_THRESHOLD) {
            el.style.backgroundColor = "#c8facc"; // 淡綠底
            el.style.borderRadius = "4px";
            el.style.padding = "2px 4px";
        }

        // 加入折扣百分比標籤
        const label = document.createElement("span");
        label.textContent = ` (領書=${Math.round(discount * 100)}%)`;
        label.style.color = discount <= DISCOUNT_THRESHOLD ? "#0a8f3c" : "#555";
        label.style.fontSize = "0.9em";
        label.style.marginLeft = "4px";
        el.appendChild(label);
    });
})();
