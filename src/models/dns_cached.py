from dataclasses import dataclass
from datetime import datetime
from .base import BaseTable

@dataclass
class DnsQueryEvents(BaseTable):
    query_contant: str  # 查询内容（域名）
    rewrite_ttl: str    # TTL 值
    query_type: str     # 查询类型（A、CNAME、SOA 等）
    query_result: str   # 查询结果（对于 SOA，合并后续字段为一字符串）
    conn_id: str        # 连接 ID
    spendtime: str      # 处理耗时
    dns_rules_name: str # 匹配到的 DNS 规则名
    dns_rules_type: str # DNS 规则类型
    dns_action: str     # DNS 动作（例如 cached）
    dns_server: str     # 若适用，DNS 服务器信息