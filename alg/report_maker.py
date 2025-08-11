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
        self.report_getters = (self._get_device_info, self._get_dataset_info, self._get_results, self._get_best_algs,
                               self._get_styles)
        self.accuracy = {}

    def create_report(self):
        if not self.first:
            return True
        self.first = False
        for report_getter in self.report_getters:
            self.report += report_getter()
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
            self.accuracy[alg] = accuracy_score(self.pipeline.tester.true[alg], self.pipeline.tester.pred[alg])
            precision, recall, f1, _ = precision_recall_fscore_support(self.pipeline.tester.true[alg],
                                                                       self.pipeline.tester.pred[alg],
                                                                       average='macro', zero_division=0)
            text += (f'<td>{self.pipeline.tester.params[alg]}</td>'
                     f'<td>{self.accuracy[alg] * 100:.2f}%</td><td>{precision * 100:.2f}%</td>'
                     f'<td>{recall * 100:.2f}%</td><td>{f1 * 100:.2f}%</td>'
                     f'<td>{self.pipeline.tester.fit_time[alg]:.5f} s</td>'
                     f'<td>{self.pipeline.tester.pred_time[alg]:.5f} s</td></tr>')
        return f'{text}</table>'

    def _get_best_algs(self):
        best_accuracy = max(self.accuracy.values())
        best_accuracy_algs = [k for k, v in self.accuracy.items() if v == best_accuracy]
        best_time = min(self.pipeline.tester.pred_time.values())
        best_time_algs = [k for k, v in self.pipeline.tester.pred_time.items() if v == best_time]
        if len(best_accuracy_algs) == 1:
            accuracy_text = 'The best algorithm by accuracy is <b>'
        else:
            accuracy_text = 'The best algorithms by accuracy are <b>'
        for alg in best_accuracy_algs:
            accuracy_text += f'{alg}, '
        accuracy_text = f'{accuracy_text[:-2]}</b> with the accuracy value of <b>{best_accuracy * 100:.2f}%</b><br>'
        if len(best_time_algs) == 1:
            time_text = 'The most time efficient algorithm is <b>'
        else:
            time_text = 'The most time efficient algorithms are <b>'
        for alg in best_time_algs:
            time_text += f'{alg}, '
        time_text = f'{time_text[:-2]}</b> with the time value of <b>{best_time:.5f} s</b>'
        return f'<p>{accuracy_text + time_text}</p>'

    @staticmethod
    def _get_styles():
        text = '<style> td { text-align: center; vertical-align: middle; } </style>'
        return text
