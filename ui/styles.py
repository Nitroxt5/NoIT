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
    QTableWidget::item:selected {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: none;
    }
    QTableWidget::item:hover {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: none;
    }
    """

dialog_button_style = """
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

file_loader_style = """
    QWidget {
        background-color: rgb(20, 40, 80);
        border: 1px solid rgba(255, 255, 255, 60);
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }

    QLabel {
        font-size: 30px;
    }

    QPushButton {
        color: white;
        background-color: rgb(47, 58, 57);
        border: 1px solid rgba(255, 255, 255, 40);
        border-radius: 6px;
        padding: 6px 12px;
        font-size: 30px;
    }

    QPushButton:hover {
        background-color: rgba(47, 58, 57, 200);
    }
    """

delete_button_style = """    
    QPushButton {
        color: red;
        font-weight: bold;
        font-size: 25px;
        border: none;
        border-radius: 0px;
        background-color: rgba(20, 40, 80, 100);
    }
    QPushButton:hover {
        background-color: rgba(100, 140, 200, 180);
    }"""

line_edit_style = """
    QLineEdit {
        color: white;
        background-color: rgba(20, 40, 80, 100);
        border: 1px solid rgba(255, 255, 255, 60);
        border-radius: 6px;
        padding: 4px 12px;
    }"""

report_style = """
    body {
      background: linear-gradient(135deg, #e0f7fa, #fce4ec);
      font-family: 'Segoe UI', sans-serif;
      color: #333;
      margin: 0;
      padding: 2em;
    }
    .container {
      backdrop-filter: blur(12px);
      background: rgba(255, 255, 255, 0.25);
      border-radius: 16px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.3);
      padding: 2em;
      max-width: 1200px;
      margin: auto;
    }
    h1, h2, h3 {
      color: #444;
      text-shadow: 0 1px 1px rgba(255, 255, 255, 0.6);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 1em;
      background: rgba(255, 255, 255, 0.4);
      border-radius: 8px;
      overflow: hidden;
    }
    th, td {
      padding: 0.75em;
      text-align: center;
      vertical-align: middle;
      border-bottom: 1px solid rgba(255, 255, 255, 0.3);
    }
    th {
      background-color: rgba(255, 255, 255, 0.6);
      font-weight: bold;
    }
    tr:hover {
      background-color: rgba(255, 255, 255, 0.2);
    }
    a {
      color: #0077cc;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
"""