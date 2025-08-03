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

table_style = """            
    QTableWidget {
        color: white;
        gridline-color: rgba(255,255,255,40);
        border: none;
    }
    
    QTableCornerButton::section {
        background-color: rgb(20, 40, 80);
    }
    
    QHeaderView::section {
        background-color: rgba(255,255,255,40);
        color: white;
        font-weight: bold;
        border: none;
        padding: 4px;
    }
    """

button_style = """
    QPushButton {
        color: white;
        background-color: rgba(20, 40, 80, 100);
        border: 1px solid rgba(255, 255, 255, 60);
        border-radius: 6px;
        padding: 6px 12px;
    }
    QPushButton:hover {
        background-color: rgba(100, 140, 200, 180);
    }"""

combo_box_style = """
    QComboBox {
        color: white;
        background-color: rgba(20, 40, 80, 100);
        border: 1px solid rgba(255, 255, 255, 60);
        border-radius: 6px;
        padding: 6px 12px;
    }
    QComboBox QAbstractItemView {
        color: white;
        selection-background-color: rgba(100, 140, 200, 180);
    }"""

dialog_background_style = """
    background-color: rgba(20, 40, 80, 160);
    border: 1px solid rgba(255, 255, 255, 70);
    border-radius: 12px;
    """

progress_bar_style = """
    QProgressBar {
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.1);
        text-align: center;
        color: white;
    }
    QProgressBar::chunk {
        background-color: rgba(0, 150, 255, 0.4);
        border-radius: 10px;
        margin: 1px;
    }
    """