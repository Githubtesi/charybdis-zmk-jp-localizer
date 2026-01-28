import re
import shutil

def translate_zmk_to_jp_windows(content):
    # 置換辞書の定義 (USでの意図 -> JIS認識のWindows用のZMKコード)
    # キーには正規表現パターン、値には置換後の文字列を入れます
    mapping = {
        r'AT_SIGN|AT': 'LBKT',              # @ -> [
        r'DOUBLE_QUOTES|DQT': 'LS(N2)',     # " -> Shift + 2
        r'SINGLE_QUOTE|SQT': 'LS(N7)',      # ' -> Shift + 7
        r'AMPERSAND|AMPS': 'LS(N6)',        # & -> Shift + 6
        r'ASTERISK|ASTRK': 'LS(QUOTE)',     # * -> Shift + : (JISの:)
        r'EQUAL': 'LS(MINUS)',              # = -> Shift + - (JISの-)
        r'PLUS': 'LS(SEMICOLON)',           # + -> Shift + ; (JISの;)
        r'LEFT_BRACKET|LBKT': 'RBKT',       # [ -> ]
        r'RIGHT_BRACKET|RBKT': 'NON_US_HASH',# ] -> \ (JISのむ)
        r'LEFT_PARENTHESIS|LPAR': 'LS(N8)', # ( -> Shift + 8
        r'RIGHT_PARENTHESIS|RPAR': 'LS(N9)',# ) -> Shift + 9
        r'LEFT_BRACE|LBRC': 'LS(RBKT)',     # { -> Shift + ]
        r'RIGHT_BRACE|RBRC': 'LS(NON_US_HASH)', # } -> Shift + \
        r'TILDE': 'LS(EQUAL)',              # ~ -> Shift + ^
        r'CARET': 'EQUAL',                  # ^ -> ^ (JISの^の位置)
        r'COLON': 'QUOTE',                  # : -> : (JISの:)
        r'PIPE': 'LS(INT3)',                # | -> Shift + ￥
        r'UNDERSCORE|UNDER': 'LS(INT1)',    # _ -> Shift + ろ
        r'LANG_ZENKAKUHANKAKU|ZNK_HNK|ZNK': 'GRAVE', # 半角全角 -> GRAVE
    }

    # すべてのキーを結合して一つの正規表現にする
    # (?<![a-zA-Z_])(パターンA|パターンB|...)(?![a-zA-Z_])
    pattern = re.compile(r'(?<![a-zA-Z_])(' + '|'.join(mapping.keys()) + r')(?![a-zA-Z_])')

    # 置換用のコールバック関数
    def replace_match(match):
        original = match.group(0)
        # どのパターンにマッチしたかを探して置換後の値を取得
        for k, v in mapping.items():
            if re.fullmatch(k, original):
                return v
        return original

    # 一括で置換を実行
    return pattern.sub(replace_match, content)

def main():
    input_file = 'charybdis.keymap'
    backup_file = 'charybdis_bk.keymap'
    output_file = 'charybdis.keymap'

    try:
        # バックアップ作成
        shutil.copyfile(input_file, backup_file)
        print(f"Backup created: {backup_file}")

        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 変換
        localized_content = translate_zmk_to_jp_windows(content)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(localized_content)

        print(f"Success! Overwritten {output_file}")
        print("Done. No more double-replacement for @ sign.")

    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
