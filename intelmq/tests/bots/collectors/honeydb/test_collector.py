# -*- coding: utf-8 -*-
"""
Testing Honeydb collector
"""
import os

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    import intelmq.bots.collectors.honeydb.collector_honeydb
