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
import shutil
import tempfile

import mock
import pytest

import databricks_cli.configure.provider as provider
from databricks_cli.cluster_policies.api import ClusterPolicyApi


@pytest.fixture(autouse=True)
def mock_conf_dir():
    path = tempfile.mkdtemp()
    provider._home = path
    yield
    shutil.rmtree(path)


@pytest.fixture()
def fixture_cluster_policies_api():
    with mock.patch(
        "databricks_cli.cluster_policies.api.PolicyService"
    ) as service_mock:
        service_mock.return_value = mock.MagicMock()
        yield ClusterPolicyApi(None)
