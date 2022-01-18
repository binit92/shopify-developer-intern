import os
from pickletools import pyset
import tempfile
from flask import Flask
import pytest



app = Flask(__name__)

@pytest.fixture
def test_homepage(client):
    ret = app.index()
    print(ret)
    assert b'' in ret

  