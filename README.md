AutoHotkey（AHK）を別プロジェクトで管理されているとのこと、了解いたしました。
今回のリポジトリを「**ZMKファームウェア側で完結させるローカライズ・ツール**」に特化した内容で `README.md` を作成しました。

---

# charybdis-zmk-jp-localizer

このプロジェクトは、**US配列の自作キーボード（Charybdis等）を、日本語（JIS）設定のWindows環境で「刻印通り」に使用する**ために、ZMKの `keymap` ファイルを自動変換するツールを提供します。

## 概要
WindowsのOS設定が日本語キーボード（JIS）になっている環境にUS配列のキーボードを接続すると、記号の配置がズレる問題が発生します。

本ツールは、PC側にソフトウェア（AutoHotkey等）を導入することなく、**キーボードのファームウェア（ZMK）レベルでキーコードを置換**することで、どのようなPCに繋いでもUS刻印通りの入力を可能にします。

## 特徴
- **ファームウェアレベルの解決**: PC側に常駐ソフトが不要。会社のPCや共有PCでもそのまま使えます。
- **一括変換**: `charybdis.keymap` 内の記号、コンボ、マクロ設定をJIS認識のWindowsに最適化されたコードへ自動置換します。
- **Charybdis特化**: トラックボール設定を含む複雑なレイヤー構造を維持したまま変換可能です。

## 🚀 使い方

### 1. 準備
1. 本リポジトリの `localize_keymap.py` をダウンロードします。
2. 同じフォルダに、あなたの元の `charybdis.keymap`（USベースの設定）を配置します。

### 2. 変換の実行
コマンドライン（ターミナル）で以下のコマンドを実行します。
```bash
python localize_keymap.py
```
実行後、同フォルダ内に **`charybdis_jp.keymap`** が生成されます。

### 3. ビルドと書き込み
1. 生成された `charybdis_jp.keymap` を、ZMKのビルド環境（または [keymap-editor](https://nickcoutsos.github.io/keymap-editor)）に読み込ませます。
2. 通常通りファームウェアをビルドし、Charybdisにフラッシュ（書き込み）してください。

## ⌨️ 主な置換・ローカライズ内容

WindowsがJIS認識している状態で、USの刻印通りの文字を出すために以下のような変換を行っています。

| 入力したい文字 | US物理キー印字 | ZMK内部で送信するコード |
| :--- | :--- | :--- |
| `@` | `Shift + 2` | `&kp LBKT` |
| `"` | `Shift + '` | `&kp LS(N2)` |
| `_` (アンダーバー) | `Shift + -` | `&kp LS(INT1)` |
| `(` | `Shift + 9` | `&kp LS(N8)` |
| `)` | `Shift + 0` | `&kp LS(N9)` |
| `^` | `Shift + 6` | `&kp EQUAL` |
| `:` | `Shift + ;` | `&kp QUOTE` |
| `[` | `[` | `&kp RBKT` |
| `]` | `]` | `&kp NON_US_HASH` |
| 半角/全角 | `` ` `` (Esc下) | `&kp LANG_ZENKAKUHANKAKU` |

## 📂 ファイル構成
- `localize_keymap.py`: `charybdis.keymap` をJIS Windows用に一括変換するPythonスクリプト。
- `charybdis.keymap`: 元となるUS配列ベースのキーマップファイル（バックアップ）。

## ⚠️ 注意事項
- **OS設定依存**: 本ツールで作成したキーマップは、Windowsの言語設定が「日本語（JIS）」になっている場合に正しく動作します。OSの設定が「英語（US）」に変更されているPCでは、記号が逆にズレることになります。
- **AutoHotkeyとの干渉**: 同様の変換を行うAutoHotkeyスクリプトを起動している場合は、二重変換を防ぐためにスクリプトを停止してください。

## 動作確認環境
- **Keyboard**: Charybdis (ZMK Firmware)
- **OS**: Windows 10 / 11 (日本語JISキーボード設定)
- **Python**: 3.x

## ライセンス
MIT License
