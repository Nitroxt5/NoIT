scroll_bar_style = """
    QScrollBar:vertical {
        background: transparent;
        width: 30px;
        margin: 2px;
    }

    QScrollBar::handle:vertical {
        background: rgb(20, 40, 80);
        min-height: 20px;
        border-radius: 4px;
    }

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        height: 0px;
        background: none;
    }
    QScrollBar:horizontal {
        background: transparent;
        height: 30px;
        margin: 2px;
    }

    QScrollBar::handle:horizontal {
        background: rgb(20, 40, 80);
        min-width: 20px;
        border-radius: 4px;
    }

    QScrollBar::add-line:horizontal,
    QScrollBar::sub-line:horizontal {
        width: 0px;
        background: none;
    }
    """