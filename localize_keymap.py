import re

def translate_zmk_to_jp_windows(content):
    # 置換ルールの定義 (USの意図 -> JIS認識のWindowsでその文字を出すためのZMKコード)
    # 形式: r'検索パターン', '置換先'
    replacements = [
        # --- 基本記号 (Shiftなし) ---
        (r'AT_SIGN|AT', 'LBKT'),              # @ -> [
        (r'DOUBLE_QUOTES|DQT', 'LS(N2)'),     # " -> Shift + 2
        (r'SINGLE_QUOTE|SQT', 'LS(N7)'),      # ' -> Shift + 7
        (r'AMPERSAND|AMPS', 'LS(N6)'),        # & -> Shift + 6
        (r'ASTERISK|ASTRK', 'LS(QUOTE)'),     # * -> Shift + : (JISの:)
        (r'EQUAL', 'LS(MINUS)'),              # = -> Shift + - (JISの-)
        (r'PLUS', 'LS(SEMICOLON)'),           # + -> Shift + ; (JISの;)
        (r'LEFT_BRACKET|LBKT', 'RBKT'),       # [ -> ]
        (r'RIGHT_BRACKET|RBKT', 'NON_US_HASH'),# ] -> \ (JISのむ) ※環境によりBSLH
        (r'LEFT_PARENTHESIS|LPAR', 'LS(N8)'), # ( -> Shift + 8
        (r'RIGHT_PARENTHESIS|RPAR', 'LS(N9)'),# ) -> Shift + 9
        (r'LEFT_BRACE|LBRC', 'LS(RBKT)'),     # { -> Shift + ]
        (r'RIGHT_BRACE|RBRC', 'LS(NON_US_HASH)'), # } -> Shift + \
        (r'TILDE', 'LS(EQUAL)'),              # ~ -> Shift + ^
        (r'CARET', 'EQUAL'),                  # ^ -> ^ (JISの^の位置)
        (r'COLON', 'QUOTE'),                  # : -> : (JISの:)
        (r'PIPE', 'LS(INT3)'),                # | -> Shift + ￥ (JISのろ/￥)
        
        # --- アンダーバー特選 ---
        # USの _ (UNDERSCORE) を JISの _ (INT1のShift) に変換
        (r'UNDERSCORE|UNDER', 'LS(INT1)'),    
        
        # --- 半角全角 (GRAVEキーをLANG_ZENKAKUHANKAKUへ) ---
        (r'kp GRAVE', 'kp LANG_ZENKAKUHANKAKU'),
    ]

    new_content = content
    for pattern, subst in replacements:
        # 単語境界を確認して誤置換を防ぐ (\bを使用)
        # ただし LS() などの括弧内も置換対象にする
        new_content = re.sub(r'(?<![a-zA-Z_])' + pattern + r'(?![a-zA-Z_])', subst, new_content)

    return new_content

def main():
    input_file = 'charybdis.keymap'
    output_file = 'charybdis_jp.keymap'

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        localized_content = translate_zmk_to_jp_windows(content)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(localized_content)
        
        print(f"Success! Generated {output_file}")
        print("Note: Check the 'combos' and 'macros' sections for logic consistency.")

    except FileNotFoundError:
        print(f"Error: {input_file} not found.")

if __name__ == "__main__":
    main()
