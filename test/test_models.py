#!/usr/bin/env python3
import unittest
from src.models.base import BaseTable
from src.models.dns_cached import DnsQueryEvents
from datetime import datetime


class TestModels(unittest.TestCase):
    def test_dns_query_events(self):
        event = DnsQueryEvents(
            id="test1",
            timestamp=datetime.now(),
            level="INFO",
            category="dns",
            raw="Test raw log",
            subcategory="dns cached",
            query_contant="example.com.",
            rewrite_ttl="120",
            query_type="A",
            query_result="1.2.3.4",
            conn_id="111111",
            spendtime="100ms",
            dns_rules_name="",
            dns_rules_type="",
            dns_action="cached",
            dns_server=""
        )
        self.assertEqual(event.category, "dns")
        self.assertEqual(event.subcategory, "dns cached")


if __name__ == "__main__":
    unittest.main()