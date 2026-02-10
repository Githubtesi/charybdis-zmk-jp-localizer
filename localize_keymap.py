import re
import shutil
from datetime import datetime


def translate_zmk_to_jp_windows(content):
    # 置換辞書の定義 (USでの意図 -> JIS認識のWindows用のZMKコード)
    mapping = {
        # --- 数字キーのShift組み合わせ (JIS Windows用修正) ---
        r'LS\(N2\)': 'LBKT',  # @
        r'LS\(N6\)': 'EQUAL',  # ^
        r'LS\(N7\)': 'LS(N6)',  # &
        r'LS\(N8\)': 'LS(QUOTE)',  # *
        r'LS\(N9\)': 'LS(N8)',  # (
        r'LS\(N0\)': 'LS(N9)',  # )

        # --- 基本キーの正規化 (ビルドエラー防止: 長い名前をZMK標準の短い名前に) ---
        r'BACKSPACE|BSPC': 'BSPC',
        r'DELETE|DEL': 'DEL',
        r'ENTER|RET': 'RET',
        r'ESCAPE|ESC': 'ESC',
        r'UP_ARROW|UP': 'UP',
        r'DOWN_ARROW|DOWN': 'DOWN',
        r'LEFT_ARROW|LEFT': 'LEFT',
        r'RIGHT_ARROW|RIGHT': 'RIGHT',
        r'LEFT_SHIFT|LSHFT|LSHIFT': 'LSHFT',
        r'RIGHT_SHIFT|RSHFT|RSHIFT': 'RSHFT',
        r'LEFT_CONTROL|LCTRL|LCONTROL': 'LCTRL',
        r'RIGHT_CONTROL|RCTRL|RCONTROL': 'RCTRL',
        r'LEFT_ALT|LALT': 'LALT',
        r'RIGHT_ALT|RALT': 'RALT',

        # --- シンボル名での指定（長い名前を標準の名前に変換しつつJIS対応） ---
        r'EXCLAMATION|EXCL': 'EXCL',
        r'AT_SIGN|AT': 'LBKT',
        r'POUND|HASH': 'HASH',
        r'DOLLAR|DLLR': 'DLLR',
        r'PERCENT|PRCNT': 'PRCNT',
        r'CARET': 'EQUAL',
        r'AMPERSAND|AMPS': 'LS(N6)',
        r'ASTERISK|ASTRK': 'LS(QUOTE)',
        r'LEFT_PARENTHESIS|LPAR': 'LS(N8)',
        r'RIGHT_PARENTHESIS|RPAR': 'LS(N9)',

        r'DOUBLE_QUOTES|DQT': 'LS(N2)',
        r'SINGLE_QUOTE|SQT': 'LS(N7)',
        r'EQUAL': 'LS(MINUS)',
        r'PLUS': 'LS(SEMI)',
        r'TILDE': 'LS(EQUAL)',
        r'COLON': 'QUOTE',
        r'SEMICOLON|SEMI': 'SEMI',

        # --- 不等号・疑問符 ---
        r'LESS_THAN|LT': 'LT',
        r'GREATER_THAN|GT': 'GT',
        r'QUESTION|QUES': 'QUES',

        # --- 括弧類 ---
        r'LEFT_BRACKET|LBKT': 'RBKT',
        r'RIGHT_BRACKET|RBKT': 'BSLH',
        r'LEFT_BRACE|LBRC': 'LS(RBKT)',
        r'RIGHT_BRACE|RBRC': 'LS(BSLH)',

        # --- その他 ---
        r'PIPE': 'LS(INT3)',
        r'UNDERSCORE|UNDER': 'LS(INT1)',
        r'LANG_ZENKAKUHANKAKU|ZNK_HNK|ZNK': 'GRAVE',
    }

    # 長いパターンから順にマッチさせる
    sorted_patterns = sorted(mapping.keys(), key=len, reverse=True)
    pattern = re.compile(r'(?<![a-zA-Z_])(' + '|'.join(sorted_patterns) + r')(?![a-zA-Z_])')

    def replace_match(match):
        original = match.group(0)
        for k, v in mapping.items():
            if re.fullmatch(k, original):
                return v
        return original

    return pattern.sub(replace_match, content)


def main():
    input_file = 'charybdis.keymap'
    output_file = 'charybdis.keymap'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    backup_file = f'charybdis_bk_{timestamp}.keymap'
    try:
        shutil.copyfile(input_file, backup_file)
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        localized_content = translate_zmk_to_jp_windows(content)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(localized_content)
        print(f"Success! {output_file} has been updated and fixed.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()