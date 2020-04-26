import os
from unittest import TestCase

import config_test
from services import backup_service


class BackupTest(TestCase):
    def test_backup_result(self):
        # given
        results = [config_test.result_as_dict, config_test.result_as_dict, config_test.result_as_dict]

        # when
        result = backup_service.backup_result(results)

        # debug
        print(result)

        # then
        self.assertTrue(os.path.exists(result))
