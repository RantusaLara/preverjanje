import pandas as pd
import numpy as np
import json

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently.metrics import *
from evidently.test_suite import TestSuite
from evidently.test_preset import DataStabilityTestPreset
from evidently.tests import *
import sys

import os


def main():
    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../..'))
    merged = os.path.join(root_dir, 'data', 'processed', 'current_data.csv')
    referenced = os.path.join(
        root_dir, 'data', 'processed', 'reference_data.csv')
    report_file = os.path.join(root_dir, 'reports', 'data_drift.html')

    csv1 = pd.read_csv(merged)
    current = pd.DataFrame(csv1)
    current.rename(columns={'final_grade': 'target'}, inplace=True)
    #current['final_grade'] = current['final_grade'].values + \
    #    np.random.normal(0, 5, current.shape[0])

    csv2 = pd.read_csv(referenced)
    reference = pd.DataFrame(csv2)
    reference.rename(columns={'final_grade': 'target'}, inplace=True)
    #reference['final_grade'] = reference['final_grade'].values + \
    #    np.random.normal(0, 5, reference.shape[0])

    report = Report(metrics=[
        DataDriftPreset(),
    ])
    report.run(reference_data=reference, current_data=current)
    report.save_html(report_file)

    tests = TestSuite(tests=[
        TestColumnsType(),
        TestNumberOfDriftedColumns(column_name='target')
    ])

    tests.run(reference_data=reference, current_data=current)
    result = tests.as_dict()
    print(tests.json())

    if not result["summary"]["all_passed"]:
        print("Stability failed!")
        sys.exit(1)

    print("Stability succeeded!")
    sys.exit(0)


if __name__ == '__main__':
    main()