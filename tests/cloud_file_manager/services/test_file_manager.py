# -*- coding: utf-8 -*-
from cloud_file_manager.services.file_manager import FileManager


def test_file_manager_create_from_config():
    file_manager = FileManager.create_from_environ()

