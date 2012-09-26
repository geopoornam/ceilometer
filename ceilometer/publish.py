# -*- encoding: utf-8 -*-
#
# Copyright © 2012 New Dream Network, LLC (DreamHost)
#
# Author: Doug Hellmann <doug.hellmann@dreamhost.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Publish a counter using the preferred RPC mechanism.
"""

from ceilometer.openstack.common import cfg
from ceilometer.openstack.common import log
from ceilometer.openstack.common import rpc
from ceilometer import meter

LOG = log.getLogger(__name__)

PUBLISH_OPTS = [
    cfg.StrOpt('metering_topic',
               default='metering',
               help='the topic ceilometer uses for metering messages',
               ),
    ]


def register_opts(config):
    """Register the options for publishing metering messages.
    """
    config.register_opts(PUBLISH_OPTS)


register_opts(cfg.CONF)


def publish_counter(context, counter, topic, secret):
    """Send a metering message for the data represented by the counter.

    :param context: Execution context from the service or RPC call
    :param counter: ceilometer.counter.Counter instance
    """
    msg = {
        'method': 'record_metering_data',
        'version': '1.0',
        'args': {'data': meter.meter_message_from_counter(counter, secret),
                 },
        }
    LOG.debug('PUBLISH: %s', str(msg))
    rpc.cast(context, topic, msg)
    rpc.cast(context, topic + '.' + counter.name, msg)
