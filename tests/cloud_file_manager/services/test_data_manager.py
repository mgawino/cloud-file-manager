# -*- coding: utf-8 -*-
from cloud_file_manager.services.data_manager import DataManager


def test_data_manager_create_from_config():
    data_manager = DataManager.from_environ_config()
