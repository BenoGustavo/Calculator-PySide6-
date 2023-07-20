import qdarktheme
from paths import (DARKER_PRIMARY_COLOR, DARKEST_PRIMARY_COLOR,
                       PRIMARY_COLOR,FONT_FAMILY)

qss = f"""
    QPushButton[cssClass="specialButton"] {{
        color: #232323;
        background: {PRIMARY_COLOR};
        font-family: {FONT_FAMILY};
    }}
    QPushButton[cssClass="specialButton"]:hover {{
        color: #232323;
        background: {DARKER_PRIMARY_COLOR};
        font-family: {FONT_FAMILY};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
        color: #232323;
        background: {DARKEST_PRIMARY_COLOR};
        font-family: {FONT_FAMILY};
    }}



        QPushButton[cssClass="backSpaceButton"] {{
        color: #232323;
        background: #f21d1d;
        font-family: {FONT_FAMILY};
    }}
    QPushButton[cssClass="backSpaceButton"]:hover {{
        color: #232323;
        background: #c91616;
        font-family: {FONT_FAMILY};
    }}
    QPushButton[cssClass="backSpaceButton"]:pressed {{
        color: #232323;
        background: #ad1111;
        font-family: {FONT_FAMILY};
    }}
"""


def setupTheme():
    qdarktheme.setup_theme(
        theme='dark',
        corner_shape='rounded',
        custom_colors={
            "[dark]": {
                "primary": f"{PRIMARY_COLOR}",
            },
            "[light]": {
                "primary": f"{PRIMARY_COLOR}",
            },
        },
        additional_qss=qss
    )