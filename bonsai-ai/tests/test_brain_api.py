"""
Copyright (C) 2019 Microsoft
Tests for BrainAPI
"""
import pytest
from ws_aiohttp import START_STOP_RESUME, METRICS, BRAIN_STATUS, BRAIN_INFO, \
     SIMS
from bonsai_ai.exceptions import BonsaiServerError

def test_brain_info(brain_api):
    assert brain_api.get_brain_info('cartpole') == BRAIN_INFO

def test_status(brain_api):
    assert brain_api.get_brain_status('cartpole') == BRAIN_STATUS

def test_start_training(brain_api):
    assert brain_api.start_training('cartpole') == START_STOP_RESUME

def test_stop_training(brain_api):
    assert brain_api.stop_training('cartpole') == START_STOP_RESUME

def test_resume_training(brain_api):
    assert brain_api.resume_training('cartpole', 'latest') == START_STOP_RESUME

def test_training_episode_metrics(brain_api):
    assert brain_api.training_episode_metrics('cartpole', 'latest') == METRICS

def test_test_episode_metrics(brain_api):
    assert brain_api.test_episode_metrics('cartpole', 'latest') == METRICS

def test_iteration_metrics(brain_api):
    assert brain_api.iteration_metrics('cartpole', 'latest') == METRICS

def test_delete(brain_api):
    assert brain_api.delete_brain('cartpole') == {}

def test_sims_info(brain_api):
    assert brain_api.get_simulator_info('cartpole') == SIMS

@pytest.mark.parametrize('request_errors', ['connection'], indirect=True)
def test_get_connection_error(request_errors, brain_api):
    try:
        brain_api.test_episode_metrics('cartpole', 'latest')
    except BonsaiServerError as e:
        str(e).find('Unable to connect') >= 0
    else:
        assert False

@pytest.mark.parametrize('request_errors', ['timeout'], indirect=True)
def test_get_timeout_error(request_errors, brain_api):
    try:
        brain_api.test_episode_metrics('cartpole', 'latest')
    except BonsaiServerError as e:
        str(e).find('timed out') >= 0
    else:
        assert False

@pytest.mark.parametrize('request_errors', ['http'], indirect=True)
def test_get_http_error(request_errors, brain_api):
    try:
        brain_api.test_episode_metrics('cartpole', 'latest')
    except BonsaiServerError as e:
        str(e).find('Request failed') >= 0
    else:
        assert False

@pytest.mark.parametrize('request_errors', ['connection'], indirect=True)
def test_put_connection_error(request_errors, brain_api):
    try:
        brain_api.start_training('cartpole')
    except BonsaiServerError as e:
        assert str(e).find('Unable to connect') >= 0
    else:
        assert False

@pytest.mark.parametrize('request_errors', ['timeout'], indirect=True)
def test_put_timeout_error(request_errors, brain_api):
    try:
        brain_api.start_training('cartpole')
    except BonsaiServerError as e:
        assert str(e).find('timed out') >= 0
        pass
    else:
        assert False

@pytest.mark.parametrize('request_errors', ['http'], indirect=True)
def test_put_http_error(request_errors, brain_api):
    try:
        brain_api.start_training('cartpole')
    except BonsaiServerError as e:
        assert str(e).find('Request failed') >= 0
    else:
        assert False

def test_post_connection_error():
    pass

def test_post_timeout_error():
    pass

def test_post_http_error():
    pass

@pytest.mark.parametrize('request_errors', ['connection'], indirect=True)
def test_delete_connection_error(request_errors, brain_api):
    try:
        brain_api.delete_brain('cartpole')
    except BonsaiServerError as e:
        assert str(e).find('Unable to connect') >= 0
    else:
        assert False

@pytest.mark.parametrize('request_errors', ['timeout'], indirect=True)
def test_delete_timeout_error(request_errors, brain_api):
    try:
        brain_api.delete_brain('cartpole')
    except BonsaiServerError as e:
        assert str(e).find('timed out') >= 0
        pass
    else:
        assert False

@pytest.mark.parametrize('request_errors', ['http'], indirect=True)
def test_delete_http_error(request_errors, brain_api):
    try:
        brain_api.delete_brain('cartpole')
    except BonsaiServerError as e:
        assert str(e).find('Request failed') >= 0
    else:
        assert False