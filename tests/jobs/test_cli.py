# Databricks CLI
# Copyright 2017 Databricks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"), except
# that the use of services to which certain application programming
# interfaces (each, an "API") connect requires that the user first obtain
# a license for the use of the APIs from Databricks, Inc. ("Databricks"),
# by creating an account at www.databricks.com and agreeing to either (a)
# the Community Edition Terms of Service, (b) the Databricks Terms of
# Service, or (c) another written agreement between Licensee and Databricks
# for the use of the APIs.
#
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import mock
from tabulate import tabulate

import databricks_cli.jobs.cli as cli
from databricks_cli.utils import pretty_format
from tests.utils import get_callback

CREATE_RETURN = {'job_id': 5}
CREATE_JSON = '{"name": "test_job"}'


def test_create_cli_json():
    with mock.patch('databricks_cli.jobs.cli.create_job') as create_job_mock:
        with mock.patch('databricks_cli.jobs.cli.click.echo') as echo_mock:
            create_job_mock.return_value = CREATE_RETURN
            get_callback(cli.create_cli)(None, CREATE_JSON)
            assert create_job_mock.call_args[0][0] == json.loads(CREATE_JSON)
            assert echo_mock.call_args[0][0] == pretty_format(CREATE_RETURN)


def test_create_cli_json_file(tmpdir):
    path = tmpdir.join('job.json').strpath
    with open(path, 'w') as f:
        f.write(CREATE_JSON)
    with mock.patch('databricks_cli.jobs.cli.create_job') as create_job_mock:
        with mock.patch('databricks_cli.jobs.cli.click.echo') as echo_mock:
            create_job_mock.return_value = CREATE_RETURN
            get_callback(cli.create_cli)(path, None)
            assert create_job_mock.call_args[0][0] == json.loads(CREATE_JSON)
            assert echo_mock.call_args[0][0] == pretty_format(CREATE_RETURN)


def test_reset_cli_json():
    with mock.patch('databricks_cli.jobs.cli.reset_job') as reset_job_mock:
        with mock.patch('databricks_cli.jobs.cli.click.echo') as echo_mock:
            reset_job_mock.return_value = CREATE_RETURN
            get_callback(cli.reset_cli)(None, CREATE_JSON)
            assert reset_job_mock.call_args[0][0] == json.loads(CREATE_JSON)
            assert echo_mock.call_args[0][0] == pretty_format(CREATE_RETURN)


LIST_RETURN = {
    'jobs': [{
        'job_id': 1,
        'settings': {
            'name': 'a'
        }
    }]
}


def test_list_jobs():
    with mock.patch('databricks_cli.jobs.cli.list_jobs') as list_jobs_mock:
        with mock.patch('databricks_cli.jobs.cli.click.echo') as echo_mock:
            list_jobs_mock.return_value = LIST_RETURN
            get_callback(cli.list_cli)(None)
            assert echo_mock.call_args[0][0] == tabulate([(1, 'a')], tablefmt='plain')


def test_list_jobs_output_json():
    with mock.patch('databricks_cli.jobs.cli.list_jobs') as list_jobs_mock:
        with mock.patch('databricks_cli.jobs.cli.click.echo') as echo_mock:
            list_jobs_mock.return_value = LIST_RETURN
            get_callback(cli.list_cli)('json')
            assert echo_mock.call_args[0][0] == pretty_format(LIST_RETURN)


RUN_NOW_RETURN = {
    "number_in_job": 1,
    "run_id": 1
}
NOTEBOOK_PARAMS = '{"a": 1}'
JAR_PARAMS = '[1, 2, 3]'


def test_run_now_no_params():
    with mock.patch('databricks_cli.jobs.cli.run_now') as run_now_mock:
        with mock.patch('databricks_cli.jobs.cli.click.echo') as echo_mock:
            run_now_mock.return_value = RUN_NOW_RETURN
            get_callback(cli.run_now_cli)(1, None, None)
            assert run_now_mock.call_args[0][0] == 1
            assert run_now_mock.call_args[0][1] is None
            assert run_now_mock.call_args[0][2] is None
            assert echo_mock.call_args[0][0] == pretty_format(RUN_NOW_RETURN)


def test_run_now_with_params():
    with mock.patch('databricks_cli.jobs.cli.run_now') as run_now_mock:
        with mock.patch('databricks_cli.jobs.cli.click.echo') as echo_mock:
            run_now_mock.return_value = RUN_NOW_RETURN
            get_callback(cli.run_now_cli)(1, JAR_PARAMS, NOTEBOOK_PARAMS)
            assert run_now_mock.call_args[0][0] == 1
            assert run_now_mock.call_args[0][1] == json.loads(JAR_PARAMS)
            assert run_now_mock.call_args[0][2] == json.loads(NOTEBOOK_PARAMS)
            assert echo_mock.call_args[0][0] == pretty_format(RUN_NOW_RETURN)
