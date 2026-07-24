# 紫记图标方案 — Phosphor Icons

## CDN

```html
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.2/src/regular/style.css" media="print" onload="this.media='all'">
```

## 使用方式

- 默认使用 `ph` 字重（1px 描边空心风格）
- 类名格式：`<i class="ph ph-icon-name"></i>`

## 完整映射表

| 用途 | Font Awesome (旧) | Phosphor (新) | 备注 |
|------|------------------|---------------|------|
| **导航 & 品牌** | | | |
| 品牌 logo | `fa-book-open` | `ph-book-open` | |
| 返回 | `fa-arrow-left` | `ph-arrow-left` | |
| 首页 | `fa-home` | `ph-house` | |
| 我的/用户 | `fa-user` | `ph-user` | |
| 账本列表 | `fa-book` | `ph-book` | |
| 退出 | `fa-sign-out-alt` | `ph-sign-out` | |
| 分享 | `fa-share-alt` | `ph-share-network` | |
| **主题** | | | |
| 日间模式 | `fa-sun` | `ph-sun` | |
| 夜间模式 | `fa-moon` | `ph-moon` | |
| **操作** | | | |
| 添加/新建 | `fa-plus` | `ph-plus` | FAB 加 `ph-bold` |
| 关闭 | `fa-times` | `ph-x` | |
| 删除 | `fa-trash-alt` | `ph-trash` | |
| 编辑/管理 | `fa-pen` | `ph-pencil` | |
| 退格 | `fa-backspace` | `ph-backspace` | |
| 连接/加入 | `fa-link` | `ph-link` | |
| **导航 Tab** | | | |
| 首页 | `fa-home` | `ph-house` | |
| 统计 | `fa-chart-pie` | `ph-chart-pie-slice` | |
| 流水 | `fa-list` | `ph-list-dashes` | |
| 成员 | `fa-users` | `ph-users` | |
| **日期/日历** | | | |
| 左箭头 | `fa-chevron-left` | `ph-caret-left` | |
| 右箭头 | `fa-chevron-right` | `ph-caret-right` | |
| 右箭头(列表) | `fa-chevron-right` | `ph-caret-right` | |
| **统计标签** | | | |
| 收入箭头 | `fa-arrow-down` | `ph-arrow-down` | |
| 支出箭头 | `fa-arrow-up` | `ph-arrow-up` | |
| **分类图标** | | | |
| 餐饮 | `fa-utensils` | `ph-fork-knife` | |
| 交通 | `fa-bus` | `ph-bus` | |
| 购物 | `fa-shopping-bag` | `ph-shopping-bag` | |
| 居住 | `fa-home` | `ph-house` | |
| 娱乐 | `fa-film` | `ph-film-strip` | |
| 医疗 | `fa-heartbeat` | `ph-heartbeat` | |
| 教育 | `fa-graduation-cap` | `ph-graduation-cap` | |
| 其他 | `fa-ellipsis-h` | `ph-dots-three` | |
| 工资 | `fa-wallet` | `ph-wallet` | |
| 奖金 | `fa-gift` | `ph-gift` | |
| 投资 | `fa-chart-line` | `ph-trend-up` | |
| 其他(收入) | `fa-plus-circle` | `ph-plus-circle` | |
| **其他** | | | |
| 用户头像占位 | `👤 emoji` | `ph-user-circle` | |
| Favicon | `💰 emoji` | `ph-currency-circle-dollar` | 或 SVG |
| 关闭浮卡 | `✕` | `ph-x` | |

## 维护说明

- 新增图标时在此表添加
- 保持只用 Phosphor Free 版图标（ph- 前缀），不要混用其他库
- 如需不同字重：`ph-bold` / `ph-light` / `ph-thin` / `ph-fill`
- 如果图标名不确定，查 https://phosphoricons.com
