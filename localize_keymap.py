import re
import shutil


def translate_zmk_to_jp_windows(content):
    # 置換辞書の定義 (USでの意図 -> JIS認識のWindows用のZMKコード)
    mapping = {
        # --- 数字キーのShift組み合わせ (最重要) ---
        r'LS\(N2\)': 'LBKT',  # US: @ -> JIS: [キー (@)
        r'LS\(N6\)': 'EQUAL',  # US: ^ -> JIS: ^キー (^)
        r'LS\(N7\)': 'LS(N6)',  # US: & -> JIS: Shift + 6 (&)
        r'LS\(N8\)': 'LS(QUOTE)',  # US: * -> JIS: Shift + : (*)
        r'LS\(N9\)': 'LS(N8)',  # US: ( -> JIS: Shift + 8 (()
        r'LS\(N0\)': 'LS(N9)',  # US: ) -> JIS: Shift + 9 ())

        # --- シンボル名での指定 ---
        r'AT_SIGN|AT': 'LBKT',
        r'DOUBLE_QUOTES|DQT': 'LS(N2)',
        r'SINGLE_QUOTE|SQT': 'LS(N7)',
        r'AMPERSAND|AMPS': 'LS(N6)',
        r'ASTERISK|ASTRK': 'LS(QUOTE)',
        r'LEFT_PARENTHESIS|LPAR': 'LS(N8)',  # ( -> Shift + 8
        r'RIGHT_PARENTHESIS|RPAR': 'LS(N9)',  # ) -> Shift + 9
        r'EQUAL': 'LS(MINUS)',
        r'PLUS': 'LS(SEMICOLON)',
        r'TILDE': 'LS(EQUAL)',
        r'CARET': 'EQUAL',
        r'COLON': 'QUOTE',

        # --- 括弧類 (前回修正済み) ---
        r'LEFT_BRACKET|LBKT': 'RBKT',  # [ -> ]キー ([)
        r'RIGHT_BRACKET|RBKT': 'BSLH',  # ] -> \キー (])
        r'LEFT_BRACE|LBRC': 'LS(RBKT)',  # {
        r'RIGHT_BRACE|RBRC': 'LS(BSLH)',  # }

        # --- その他 ---
        r'PIPE': 'LS(INT3)',
        r'UNDERSCORE|UNDER': 'LS(INT1)',
        r'LANG_ZENKAKUHANKAKU|ZNK_HNK|ZNK': 'GRAVE',
    }

    # 一括置換用の正規表現（カッコを含むため特殊文字をエスケープしたものを優先）
    # 重複を避けるため、長い文字列から順にマッチさせる
    sorted_patterns = sorted(mapping.keys(), key=len, reverse=True)
    pattern = re.compile(r'(?<![a-zA-Z_])(' + '|'.join(sorted_patterns) + r')(?![a-zA-Z_])')

    def replace_match(match):
        original = match.group(0)
        # エスケープを考慮してマッチング
        for k, v in mapping.items():
            if re.fullmatch(k, original):
                return v
        return original

    return pattern.sub(replace_match, content)


def main():
    input_file = 'charybdis.keymap'
    backup_file = 'charybdis_bk.keymap'
    output_file = 'charybdis.keymap'

    try:
        shutil.copyfile(input_file, backup_file)
        print(f"Backup created: {backup_file}")

        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        localized_content = translate_zmk_to_jp_windows(content)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(localized_content)

        print(f"Success! Overwritten {output_file}")
        print("Fixed: Parentheses ( ) and shifted numbers are now correctly mapped.")

    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
