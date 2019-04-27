# flake8: noqa

sp_key_overrides = {
    'Microtropis japonica (Franch. et Sav.) Hallier f. var. japonica': 'microtropis_japonica_var_japonica',
    'Microtropis japonica (Franch. et Sav.) Hallier f. var. sakaguchiana (Koidz.) Hatus. ex Shimabuku': 'microtropis_japonica_var_sakaguchiana'
}

angiosperm_overrides = {
    # typo fixes
    1764: (
        {
            '新リスト和名': 'カズサハリイ',
            '和名異名': '',
            'GreenList学名': 'Eleocharis congesta D.Don var. japonica (Miq.) H.Hara ×var. thermaris (Hultén) T.Koyama',
            'APG科和名': 'カヤツリグサ科',
            'APG科名': 'Cyperaceae',
        },
        [
            {
                '新リスト和名': 'カズサハリイ',
                '和名異名': '',
                'GreenList学名': 'Eleocharis congesta D.Don var. japonica (Miq.) H.Hara x var. thermaris (Hultén) T.Koyama',
                'APG科和名': 'カヤツリグサ科',
                'APG科名': 'Cyperaceae',
            }
        ]
    ),
    3210: (
        {
            '新リスト和名': 'オキチハギ',
            '和名異名': '',
            'GreenList学名': 'Hylodesmum podocarpum (DC.) H.Ohashi et R.R.Mill subsp. oxyphyllum (DC.) H.Ohashi et R.R.Mill var. japonicum (Miq.) H.Ohashif. decorum (Iwata) H.Ohashi',
            'APG科和名': 'マメ科',
            'APG科名': 'Fabaceae/Leguminosae',
        },
        [
            {
                '新リスト和名': 'オキチハギ',
                '和名異名': '',
                'GreenList学名': 'Hylodesmum podocarpum (DC.) H.Ohashi et R.R.Mill subsp. oxyphyllum (DC.) H.Ohashi et R.R.Mill var. japonicum (Miq.) H.Ohashi f. decorum (Iwata) H.Ohashi',
                'APG科和名': 'マメ科',
                'APG科名': 'Fabaceae/Leguminosae',
            }
        ]
    ),
    7741: (
        {
            '新リスト和名': 'アオオニヤブタビラコ',
            '和名異名': '',
            'GreenList学名': 'Lapsanastrum humile (Thunb.) Pak et K.Bremerx Youngia japonica (L.) DC.',
            'APG科和名': 'キク科',
            'APG科名': 'Asteraceae/Compositae',
        },
        [
            {
                '新リスト和名': 'アオオニヤブタビラコ',
                '和名異名': '',
                'GreenList学名': 'Lapsanastrum humile (Thunb.) Pak et K.Bremer x Youngia japonica (L.) DC.',
                'APG科和名': 'キク科',
                'APG科名': 'Asteraceae/Compositae',
            }
        ]
    ),
    2151: (
        {
            '新リスト和名': 'メンテンササガヤ'  # duplicating scientific name
        },
        []
    ),
    2166: (
        {
            '新リスト和名': 'タカノハススキ'  # cultivar
        },
        []
    ),
    2284: (
        {
            '新リスト和名': 'ラッキョウヤダケ'  # cultivar
        },
        []
    ),
    2220: (
        {
            '新リスト和名': 'ヤシバダケ'  # cultivar
        },
        []
    ),
    2283: (
        {
            '新リスト和名': 'キシマヤダケ'  # cultivar
        },
        []
    ),
    5394: (
        {
            '新リスト和名': 'ヤエヤマヤマボウシ'  # duplicating scientific name
        },
        []
    ),
    7345: (
        {
            '新リスト和名': 'オオユウガギク'  # duplicating scientific name
        },
        []
    ),
    7346: (
        {
            '新リスト和名': 'キタガワユウガギク'  # duplicating scientific name
        },
        []
    ),
    7347: (
        {
            '新リスト和名': 'イワバノギク'  # duplicating scientific name
        },
        []
    ),

    # move ワカミヤスミレ to just below ナルカミスミレ
    3094: (
        {'新リスト和名': 'ワカミヤスミレ'},
        []
    ), 
    4417: (
        {
            '新リスト和名': 'ナルカミスミレ',
            '和名異名': '',
            'GreenList学名': 'Viola eizanensis (Makino) Makino var. simplicifolia Makino f. leucantha Hiyama',
            'APG科和名': 'スミレ科',
            'APG科名': 'Violaceae',
        },
        [
            {
                '新リスト和名': 'ナルカミスミレ',
                '和名異名': '',
                'GreenList学名': 'Viola eizanensis (Makino) Makino var. simplicifolia Makino f. leucantha Hiyama',
                'APG科和名': 'スミレ科',
                'APG科名': 'Violaceae',
            },
            {
                '新リスト和名': 'ワカミヤスミレ',
                '和名異名': '',
                'GreenList学名': 'Viola eizanensis Makino x V. keiskei Miq.',
                'APG科和名': 'スミレ科',
                'APG科名': 'Violaceae',
            },

        ]
    )
}