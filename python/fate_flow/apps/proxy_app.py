#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
from flask import request
from flask.json import jsonify

from fate_arch.common import FederatedMode

from fate_flow.utils.api_utils import federated_api, forward_api, proxy_api


page_name = 'forward'


@manager.route('/<role>', methods=['post'])
def start_proxy(role):
    request_config = request.json or request.form.to_dict()
    _job_id = f"{role}_forward"
    if role in ['marketplace']:
        response = proxy_api(role, _job_id, request_config)
    else:
        headers = request.headers
        json_body = {}
        if request_config.get('header') and request_config.get("body"):
            src_party_id = request_config.get('header').get('src_party_id')
            dest_party_id = request_config.get('header').get('dest_party_id')
            json_body = request_config
            if headers:
                json_body['header'].update(headers)
        else:
            src_party_id = headers.get('src_party_id')
            dest_party_id = headers.get('dest_party_id')
            json_body["header"] = request.headers
            json_body["body"] = request_config
        response = federated_api(job_id=_job_id,
                                 method='POST',
                                 endpoint=f'/forward/{role}/do',
                                 src_party_id=src_party_id,
                                 dest_party_id=dest_party_id,
                                 src_role=None,
                                 json_body=json_body,
                                 federated_mode=FederatedMode.MULTIPLE)
    return jsonify(response)


@manager.route('/<role>/do', methods=['post'])
def start_forward(role):
    request_config = request.json or request.form.to_dict()
    response = forward_api(role, request_config)
    return jsonify(response)
