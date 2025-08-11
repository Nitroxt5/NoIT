import cpuinfo
import GPUtil
import psutil

from pathlib import Path

from PyQt5.QtWidgets import QPushButton
from sklearn.metrics import precision_recall_fscore_support, accuracy_score


class Reporter:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.first = True
        self.report = '<!DOCTYPE html><html><body>'
        self.column_names = ('Algorithm', 'Hyperparameters', 'Accuracy', 'Precision', 'Recall', 'F1-Score', 'Fit time',
                             'Predict time')

    def create_report(self):
        if not self.first:
            return True
        self.first = False
        self.report += self._get_device_info()
        self.report += self._get_dataset_info()
        self.report += self._get_results()
        self.report += self._get_styles()
        self.report += '</body></html>'
        path = Path(f'reports\\{self.pipeline.data_name}_report.html')
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as file:
            file.write(self.report)
        self._create_info_window(f'Report `{self.pipeline.data_name}_report.html` is done. '
                                 f'It can be seen in `reports` folder.')
        return False

    def _create_info_window(self, info=''):
        end_btn = QPushButton('End')
        end_btn.clicked.connect(self.pipeline.parent().parent().open_file_loader)
        self.pipeline.eda.create_dialog_window([end_btn], info)

    @staticmethod
    def _get_device_info():
        text = f'CPU: {cpuinfo.get_cpu_info()["brand_raw"]}.<br>'
        text += f'Memory: {round(psutil.virtual_memory().total / 1024**3)}GB.<br>GPU: '
        for gpu in GPUtil.getGPUs():
            text += f'{gpu.name}.<br>'
        return f'<p>{text}</p>'

    def _get_dataset_info(self):
        text = (f'Testing on `{self.pipeline.data_name}` dataset.<br>'
                f'Dataset consists of {len(self.pipeline.eda.data)} rows and '
                f'{len(self.pipeline.eda.data.columns)} columns.')
        return f'<p>{text}</p>'

    def _get_results(self):
        text = f'<table border="1"><tr>'
        for col in self.column_names:
            text += f'<th>{col}</th>'
        text += '</tr>'
        for alg in self.pipeline.tester.true:
            text += f'<tr><td>{alg}</td>'
            accuracy = accuracy_score(self.pipeline.tester.true[alg], self.pipeline.tester.pred[alg])
            precision, recall, f1, _ = precision_recall_fscore_support(self.pipeline.tester.true[alg],
                                                                       self.pipeline.tester.pred[alg],
                                                                       average='macro', zero_division=0)
            text += (f'<td>{self.pipeline.tester.params[alg]}</td>'
                     f'<td>{accuracy * 100:.2f}%</td><td>{precision * 100:.2f}%</td>'
                     f'<td>{recall * 100:.2f}%</td><td>{f1 * 100:.2f}%</td>'
                     f'<td>{self.pipeline.tester.fit_time[alg]:.5f} s</td>'
                     f'<td>{self.pipeline.tester.pred_time[alg]:.5f} s</td></tr>')
        return text

    @staticmethod
    def _get_styles():
        text = '<style> td { text-align: center; vertical-align: middle; } </style>'
        return text
