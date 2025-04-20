# -*- coding: utf-8 -*-

import logs_db  # logs_db.change_db_path(file)
from pathlib import Path

db_tables = ["logs", "list_logs"]


def view_logs(request):
    # ---
    db_path = request.args.get("db_path")
    # ---
    dbs = []
    # ---
    if db_path:
        dbs = logs_db.change_db_path(db_path)
        # ---
        db_path = db_path if db_path in dbs else "new_logs.db"
    # ---
    page = request.args.get("page", 1, type=int)
    # ---
    per_page = request.args.get("per_page", 10, type=int)
    order = request.args.get("order", "desc").upper()
    order_by = request.args.get("order_by", "response_count")
    # ---
    status = request.args.get("status", "")
    like = request.args.get("like", "")
    # ---
    table_name = request.args.get("table_name", "")
    # ---
    if table_name not in db_tables:
        table_name = "logs"
    # ---
    # Validate values
    page = max(1, page)
    per_page = max(1, min(100, per_page))

    # Offset for pagination
    offset = (page - 1) * per_page
    # ---
    order_by_types = [
        "id",
        "endpoint",
        "request_data",
        "response_status",
        "response_time",
        "response_count",
        "timestamp",
    ]
    # ---
    if order_by not in order_by_types:
        order_by = "timestamp"
    # ---
    # [{'response_status': 'no_result', 'numbers': 10066}, {'response_status': 'success', 'numbers': 12}
    status_table = logs_db.get_response_status(table_name=table_name)
    # ---
    status = status if (status in status_table or status == "Category") else ""
    # ---
    logs = logs_db.get_logs(per_page, offset, order, order_by=order_by, status=status, table_name=table_name, like=like)
    # ---
    # Convert to list of dicts
    log_list = []
    # ---
    for log in logs:
        # {'id': 1, 'endpoint': 'api', 'request_data': 'Category:1934-35 in Bulgarian football', 'response_status': 'true', 'response_time': 123123.0, 'response_count': 6, 'timestamp': '2025-04-10 01:08:58'}
        # ---
        request_data = log["request_data"].replace("_", ' ')
        # ---
        log_list.append(
            {
                "id": log["id"],
                "endpoint": log["endpoint"],
                "request_data": request_data,
                "response_status": log["response_status"],
                "response_time": log["response_time"],
                "timestamp": log["timestamp"],
                "response_count": log["response_count"],
            }
        )
    # ---
    total_logs = logs_db.count_all(status=status, table_name=table_name, like=like)
    # ---
    # Pagination calculations
    total_pages = (total_logs + per_page - 1) // per_page
    start_log = (page - 1) * per_page + 1
    end_log = min(page * per_page, total_logs)
    start_page = max(1, page - 2)
    end_page = min(start_page + 4, total_pages)
    start_page = max(1, end_page - 4)
    # ---
    sum_all = logs_db.sum_response_count(status=status, table_name=table_name, like=like)
    # ---
    if status == "":
        status = "All"
    # ---
    table_new = {
        "sum_all": f"{sum_all:,}",
        "db_path": db_path,
        "table_name": table_name,
        "total_pages": total_pages,
        "total_logs": f"{total_logs:,}",
        "start_log": start_log,
        "end_log": end_log,
        "start_page": start_page,
        "end_page": end_page,
        "order": order,
        "order_by": order_by,
        "per_page": per_page,
        "page": page,
        "status": status,
        "like": like,
    }
    # ---
    if "All" not in status_table:
        status_table.append("All")
    # ---
    if "Category" not in status_table:
        status_table.append("Category")
    # ---
    result = {
        "dbs": dbs,
        "logs": log_list,
        "order_by_types": order_by_types,
        "tab": table_new,
        "status_table": status_table,
    }
    # ---
    return result
