# Copyright (C) 2018 Bonsai, Inc.

# pylint: disable=missing-docstring
# pylint: disable=too-many-function-args
import json
import os
import pytest
import requests

from bonsai_ai import Brain, Config
from bonsai_ai.brain import IN_PROGRESS, STOPPED


def test_brain(train_config):
    """ Tests that a brain is created without errors """
    # Patch and Mock out requests/responses
    brain = Brain(train_config, 'cartpole')

    assert brain.config == train_config
    assert brain.name == 'cartpole'
    assert brain.description is None
    assert brain.latest_version == 1
    assert brain._timeout == 60


def test_brain_update(blank_brain, v2_get):
    """ Tests brain update function """
    assert blank_brain._state == IN_PROGRESS
    assert blank_brain.latest_version == 1

    # Brain.update gets called automatically so that these
    # properties stay in sync with the service
    assert blank_brain.ready is False
    assert blank_brain.state == STOPPED
    assert blank_brain.exists is True
    assert blank_brain.latest_version == 4


def test_brain_predict_version():
    """ Tests brain version property """
    config = Config([__name__, '--predict=4'])
    brain = Brain(config)
    assert brain.config.predict is True
    assert brain.config.brain_version == 4
    assert brain.version == 4


def test_brain_predict_exist_ready(predict_config, v2_get):
    """ Tests existence and readiness in predict mode """
    brain = Brain(predict_config)
    brain.update()
    assert brain.exists is True
    assert brain.ready is True


def set_proxies(http_proxy, https_proxy, all_proxy):
    def update_env_key(key, value=None):
        if value is None:
            try:
                del os.environ[key]
            except:
                pass
        else:
            os.environ[key] = value

    update_env_key('http_proxy', http_proxy)
    update_env_key('https_proxy', https_proxy)
    update_env_key('all_proxy', all_proxy)


def test_brain_no_proxy():
    config = Config([__name__])
    brain = Brain(config)
    assert brain._proxy_header() is None


def test_brain_with_proxy():
    # Patch and Mock out requests/responses
    set_proxies(http_proxy='pass',
                https_proxy=None,
                all_proxy=None)
    config = Config([__name__])
    brain = Brain(config)
    assert brain._proxy_header() is not None


def test_brain_name_is_not_none(train_config):
    brain = Brain(train_config)
    assert brain.name is not None


def test_brain_timeout():
    config = Config([__name__, '--network-timeout=1'])
    brain = Brain(config)
    assert brain._timeout == 1


def test_brain_training_episode_metrics(train_config):
    """
      NOTE: Test does not return correct JSON according to API documentation.
            We are verifying code paths.
    """
    brain = Brain(train_config)
    metrics = brain.training_episode_metrics()
    json.dumps(metrics)


def test_brain_iteration_metrics(train_config):
    """
      NOTE: Test does not return correct JSON according to API documentation.
            We are verifying code paths.
    """
    brain = Brain(train_config)
    metrics = brain.iteration_metrics()
    json.dumps(metrics)


def test_brain_test_episode_metrics(train_config):
    """
      NOTE: Test does not return correct JSON according to API documentation.
            We are verifying code paths.
    """
    brain = Brain(train_config)
    metrics = brain.training_episode_metrics()
    json.dumps(metrics)


@pytest.mark.parametrize('request_errors', ['connection'], indirect=True)
def test_brain_get_connection_error(train_config, request_errors, capsys):
    brain = Brain(train_config)
    brain.training_episode_metrics()
    _, err = capsys.readouterr()
    assert 'Unable to connect' in err


@pytest.mark.parametrize('request_errors', ['timeout'], indirect=True)
def test_brain_get_timeout_error(train_config, request_errors, capsys):
    brain = Brain(train_config)
    brain.training_episode_metrics()
    _, err = capsys.readouterr()
    assert 'timed out' in err


@pytest.mark.parametrize('request_errors', ['http'], indirect=True)
def test_brain_get_http_error(train_config, request_errors, capsys):
    brain = Brain(train_config)
    metrics = brain.training_episode_metrics()
    _, err = capsys.readouterr()
    assert 'Request failed' in err
    assert metrics == {}


if __name__ == '__main__':
    pytest.main([__file__])
