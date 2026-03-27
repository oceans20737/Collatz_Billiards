# Shiftless Collatz Billiards 🎱

**Author:** Hiroshi Harada  
**Date:** March 27, 2026  
**License:** Code under MIT, Generated Media under CC BY 4.0

![Shiftless Collatz Billiards Animation (Seed 27)](collatz_shiftless_billiards_animation_seed_27.gif)

## 概要

本リポジトリは、**シフトレス・コラッツ・モデル（Shiftless Collatz Model）** を可視化するための Python ツール群を提供します。

標準的な $3n+1$ では、右シフト（2 で割る操作）によって情報が失われますが、シフトレス・コラッツ・モデルは次の式で軌道を更新し、**ビット情報を一切失わない**ことが特徴です。

$$n_{k+1} = 3n_k + 2^{v_2(n_k)}$$

この軌道を $\log_3$ 格子平面上に描くと、  
- **3倍成長による慣性（Inertia）**
- **LSB 由来の上向きの“しなり”（Warp）**
- **$2^M$ に対応するジャックポケット（Jackpot）**

といった物理的な構造が現れ、まるでビリヤードのような弾道運動として観察できます。

---

## 含まれるファイル

### `collatz_billiards_image.py`
シフトレス・コラッツ軌道の **高解像度（300 DPI）静止画** を生成します。  
論文、ポスター、静的図版に最適です。

### `collatz_billiards_animation.py`
軌道を **シネマティックな追跡ズームアニメーション**（GIF、および ffmpeg があれば MP4）として出力します。

特徴:
- タイル境界での前後ポーズ  
- ジャックポット到達時のズーム停止  
- 最終オーバービューのフリーズ  
- 見やすい軌道ラインとビリヤード台の演出  

---

## 必要環境

```bash
pip install numpy matplotlib tqdm
```

*注意: MP4 出力には `ffmpeg` が必要です。GIF 出力は `ffmpeg` が無くても動作します。*

## 使い方

ターミナルまたは Jupyter から直接実行できます。
各スクリプト末尾の `seed_to_hunt` を変更することで、任意の初期値の軌道を探索できます。

```bash
# 高解像度の静止画を生成
python collatz_billiards_image.py

# アニメーション（GIF / MP4）を生成
python collatz_billiards_animation.py
```

## 出力例（シード = 27）

- 41 ステップの長い旅
- 最終到達点は $2^{64}$
- 前半は LSB の影響で激しい“しなり”
- 中盤はジャックポケットをかすめるニアミスが連続
- 終盤は局所成長率が最大 3.2 に達し、強烈な最終突進で収束

上の GIF はその軌道の全体像を示しています。

## ライセンス

- Python ソースコード: MIT License
- 生成された画像・アニメーション: CC BY 4.0
- © 2026 Hiroshi Harada
```