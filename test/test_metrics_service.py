from unittest import TestCase

from services import metrics_service

COUNT = 'count'

ENVIRONMENT = 'environment'

OK = 'OK'
ERRORS = 'errors'


class Test(TestCase):
    def test_add_ok_metric_to_metrics(self):
        # given
        metrics_service.reset()

        # when
        metrics_service.add(ENVIRONMENT, OK)
        result = metrics_service.get_currents_metrics()

        # then
        self.assertEqual(result[OK][ENVIRONMENT], 1)
        self.assertEqual(result[COUNT], 1)

    def test_add_error_metric_to_metrics(self):
        # given
        metrics_service.reset()

        # when
        metrics_service.add(ENVIRONMENT, ERRORS)
        result = metrics_service.get_currents_metrics()

        # then
        self.assertEqual(result[ERRORS][ENVIRONMENT], 1)
        self.assertEqual(result[COUNT], 1)

    def test_add_many_metrics(self):
        # given
        metrics_service.reset()

        # when
        metrics_service.add(ENVIRONMENT, ERRORS)
        metrics_service.add(ENVIRONMENT, OK)
        setup = metrics_service.get_currents_metrics()

        # then
        self.assertEqual(setup[ERRORS][ENVIRONMENT], 1)
        self.assertEqual(setup[OK][ENVIRONMENT], 1)
        self.assertEqual(setup[COUNT], 2)

    def test_add_not_existing_metric_do_not_change_counts(self):
        # given
        metrics_service.reset()
        metrics_service.add(ENVIRONMENT, ERRORS)
        metrics_service.add(ENVIRONMENT, OK)
        setup = metrics_service.get_currents_metrics()

        # verify
        self.assertEqual(setup[ERRORS][ENVIRONMENT], 1)
        self.assertEqual(setup[OK][ENVIRONMENT], 1)
        self.assertEqual(setup[COUNT], 2)

        # when
        metrics_service.add("GARLIC", OK)

        # then
        result = metrics_service.get_currents_metrics()
        self.assertEqual(result[ERRORS][ENVIRONMENT], 1)
        self.assertEqual(result[OK][ENVIRONMENT], 1)
        self.assertEqual(result[COUNT], 2)

    def test_add_not_existing_metric_result_do_not_change_counts(self):
        # given
        metrics_service.reset()
        metrics_service.add(ENVIRONMENT, ERRORS)
        metrics_service.add(ENVIRONMENT, OK)
        setup = metrics_service.get_currents_metrics()

        # verify
        self.assertEqual(setup[ERRORS][ENVIRONMENT], 1)
        self.assertEqual(setup[OK][ENVIRONMENT], 1)
        self.assertEqual(setup[COUNT], 2)

        # when
        metrics_service.add(ENVIRONMENT, "UFO")

        # then
        result = metrics_service.get_currents_metrics()
        self.assertEqual(result[ERRORS][ENVIRONMENT], 1)
        self.assertEqual(result[OK][ENVIRONMENT], 1)
        self.assertEqual(result[COUNT], 2)


    def test_reset_should_clear_metrics(self):
        # given
        metrics_service.reset()
        metrics_service.add(ENVIRONMENT, ERRORS)
        metrics_service.add(ENVIRONMENT, OK)
        setup = metrics_service.get_currents_metrics()

        # verify
        self.assertEqual(setup[ERRORS][ENVIRONMENT], 1)
        self.assertEqual(setup[OK][ENVIRONMENT], 1)
        self.assertEqual(setup[COUNT], 2)

        # when
        metrics_service.reset()
        result = metrics_service.get_currents_metrics()
        # then
        self.assertEqual(result[ERRORS][ENVIRONMENT], 0)
        self.assertEqual(result[OK][ENVIRONMENT], 0)
        self.assertEqual(result[COUNT], 0)


    def test_should_save_backup(self):
        # given
        metrics_service.reset()
        metrics_service.add(ENVIRONMENT, ERRORS)
        metrics_service.add(ENVIRONMENT, OK)
        setup = metrics_service.get_currents_metrics()

        # verify
        self.assertEqual(setup[ERRORS][ENVIRONMENT], 1)
        self.assertEqual(setup[OK][ENVIRONMENT], 1)
        self.assertEqual(setup[COUNT], 2)

        # when
        result = metrics_service.generate_daily_metrics()

        # then
        self.assertEqual(result,'saved')
