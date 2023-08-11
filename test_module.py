import unittest
from unittest import mock
import utils
import pandas as pd

data = {
    'sid': [123, 456, 789],
    'score': [None, 3, None],
    'comment': ['', 'Hello World!', '']
}

class TestUtilFunctions(unittest.TestCase):

    def test_load_pdf_list(self):
        with mock.patch('os.listdir') as mocked_listdir:
            mocked_listdir.return_value = ['123@test123test@course.pdf', '789@test789test@course.pdf']
            res = utils.load_pdf_list()
        ans = {'123':'123@test123test@course.pdf', '789':'789@test789test@course.pdf'}
        self.assertEqual(res, ans)

    def test_sid_list(self):
        with mock.patch('pandas.read_csv') as mocked_read_csv:
            mocked_read_csv.return_value = pd.DataFrame(data)
            res = utils.sid_list()
        ans = [123, 456, 789]
        self.assertEqual(res, ans)

    def test_sid_ungraded_list(self):
        with mock.patch('pandas.read_csv') as mocked_read_csv:
            mocked_read_csv.return_value = pd.DataFrame(data)
            res = utils.sid_ungraded_list()
        ans = [123, 789]
        self.assertEqual(res, ans)

    def test_sid_graded_list(self):
        with mock.patch('pandas.read_csv') as mocked_read_csv:
            mocked_read_csv.return_value = pd.DataFrame(data)
            res = utils.sid_graded_list()
        ans = [456]
        self.assertEqual(res, ans)
    
    def test_update_grade(self):
        with mock.patch('pandas.read_csv') as mocked_read_csv:
            mocked_read_csv.return_value = pd.DataFrame(data)
            with mock.patch('pandas.DataFrame.to_csv') as mocked_to_csv:
                utils.update_grade(123,'5','test')

        mocked_to_csv.assert_called_once_with('save.csv', index=False)
    
    def test_convert_pdf_to_images(self):
        pass

    def test_get_image_filenames(self):
        pass

    def test_get_next_sid(self):
        pass

    def test_get_file(self):
        pass

    def test_get_sid_with_file(self):
        pass

    
if __name__ == '__main__':
    unittest.main()