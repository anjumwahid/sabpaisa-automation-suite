"""
PARALLEL Batch Runner — Run 100 clients in parallel (5 at once).
Each client runs in its own isolated config — no conflict.

Usage:
  python run_parallel_clients.py
  python run_parallel_clients.py --workers 10   # 10 parallel
  python run_parallel_clients.py --smoke        # run only E2E tests (faster)

Input: data/clients.json (list of clients)
Output: reports/Client_Regression_Report_TIMESTAMP.xlsx + per-client allure reports
"""

import json
import os
import sys
import subprocess
import argparse
import tempfile
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "openpyxl"], check=True)
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENTS_FILE = os.path.join(PROJECT_DIR, "data", "clients.json")
REPORTS_DIR = os.path.join(PROJECT_DIR, "reports")
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


def load_clients():
    with open(CLIENTS_FILE, "r") as f:
        return json.load(f)


def run_client(client, smoke_only=False):
    """Run tests for single client in isolated env vars."""
    mid = client["merchant_id"]
    env = client["environment"]
    allure_dir = os.path.join(REPORTS_DIR, f"allure-results-{mid}")

    # Pass config via env vars — no shared file conflict
    env_vars = os.environ.copy()
    env_vars["MERCHANT_ID_OVERRIDE"] = mid
    env_vars["ENV"] = env
    env_vars["HEADLESS"] = "true"
    env_vars["SLOW_MO"] = "0"

    cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_regression_suite.py",
        f"--alluredir={allure_dir}",
        "--clean-alluredir",
        "-q",
    ]

    if smoke_only:
        cmd.extend(["-k", "R9 or R10"])  # only E2E + full sequential

    start = datetime.now()
    print(f"[START] {mid} ({env})")

    try:
        result = subprocess.run(
            cmd, cwd=PROJECT_DIR, env=env_vars,
            capture_output=True, text=True, timeout=600,
        )
        duration = (datetime.now() - start).total_seconds()
        print(f"[DONE ] {mid}: exit={result.returncode} in {duration:.0f}s")
        return client, allure_dir, result.returncode, duration
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] {mid}")
        return client, allure_dir, -1, 600


def parse_results(allure_dir):
    results = {
        "total": 0, "passed": 0, "failed": 0, "broken": 0,
        "UPI": "N/A", "Cards": "N/A", "Netbanking": "N/A",
        "Wallets": "N/A", "Offline": "N/A",
        "Config": "N/A", "Customer": "N/A",
    }
    mode_map = {
        "upi": "UPI", "qr": "UPI",
        "card": "Cards", "cvv": "Cards",
        "netbanking": "Netbanking", "bank": "Netbanking", "equitas": "Netbanking",
        "wallet": "Wallets", "phonepe": "Wallets",
        "offline": "Offline", "cash": "Offline",
        "config": "Config", "merchant": "Config", "fetch": "Config",
        "customer": "Customer",
    }
    if not os.path.exists(allure_dir):
        return results
    for fname in os.listdir(allure_dir):
        if not fname.endswith("-result.json"):
            continue
        try:
            with open(os.path.join(allure_dir, fname), "r", encoding="utf-8") as f:
                data = json.load(f)
            status = data.get("status", "unknown")
            name = (data.get("name", "") + " " + data.get("fullName", "")).lower()
            results["total"] += 1
            if status == "passed":
                results["passed"] += 1
            elif status == "failed":
                results["failed"] += 1
            elif status == "broken":
                results["broken"] += 1
            for keyword, mode in mode_map.items():
                if keyword in name:
                    if results[mode] == "N/A":
                        results[mode] = status.upper()
                    elif results[mode] == "PASSED" and status != "passed":
                        results[mode] = status.upper()
                    break
        except Exception:
            pass
    return results


def generate_excel(all_results, total_duration):
    wb = Workbook()
    ws = wb.active
    ws.title = "Client Regression"

    header_font = Font(bold=True, size=11, color="FFFFFF")
    header_fill = PatternFill("solid", start_color="1565C0")
    pass_fill = PatternFill("solid", start_color="C6EFCE")
    fail_fill = PatternFill("solid", start_color="FFC7CE")
    na_fill = PatternFill("solid", start_color="F5F5F5")
    border = Border(*[Side(style="thin")] * 4)
    center = Alignment(horizontal="center", vertical="center")

    ws.merge_cells("A1:N1")
    ws["A1"] = f"SabPaisa Regression - {len(all_results)} Clients - {datetime.now().strftime('%d-%b-%Y %H:%M')} - Duration: {total_duration:.0f}s"
    ws["A1"].font = Font(bold=True, size=13, color="1565C0")
    ws["A1"].alignment = Alignment(horizontal="center")

    headers = ["S.No", "Client Code", "Env", "Total", "Passed", "Failed", "Broken",
               "Config", "UPI", "Cards", "Netbanking", "Wallets", "Offline", "Status"]

    for col, h in enumerate(headers, 1):
        c = ws.cell(row=3, column=col, value=h)
        c.font = header_font
        c.fill = header_fill
        c.alignment = center
        c.border = border

    for idx, (client, res, duration) in enumerate(all_results, 1):
        row = idx + 3
        is_pass = res["failed"] == 0 and res["broken"] == 0 and res["total"] > 0
        overall = "PASS" if is_pass else ("FAIL" if res["total"] > 0 else "NOT RUN")

        values = [idx, client["merchant_id"], client["environment"],
                  res["total"], res["passed"], res["failed"], res["broken"],
                  res["Config"], res["UPI"], res["Cards"],
                  res["Netbanking"], res["Wallets"], res["Offline"], overall]

        for col, v in enumerate(values, 1):
            c = ws.cell(row=row, column=col, value=v)
            c.alignment = center
            c.border = border
            if isinstance(v, str):
                if "PASS" in v:
                    c.fill = pass_fill
                elif "FAIL" in v or "BROKEN" in v:
                    c.fill = fail_fill
                elif v == "N/A" or v == "NOT RUN":
                    c.fill = na_fill

    # Summary
    summary_row = len(all_results) + 5
    total = len(all_results)
    passed = sum(1 for _, r, _ in all_results if r["failed"] == 0 and r["broken"] == 0 and r["total"] > 0)

    ws.cell(row=summary_row, column=1, value="SUMMARY").font = Font(bold=True, size=12)
    ws.cell(row=summary_row + 1, column=1, value="Total Clients:")
    ws.cell(row=summary_row + 1, column=2, value=total)
    ws.cell(row=summary_row + 2, column=1, value="Passed:")
    ws.cell(row=summary_row + 2, column=2, value=passed).fill = pass_fill
    ws.cell(row=summary_row + 3, column=1, value="Failed:")
    ws.cell(row=summary_row + 3, column=2, value=total - passed).fill = fail_fill if total - passed > 0 else na_fill
    ws.cell(row=summary_row + 4, column=1, value="Total Duration:")
    ws.cell(row=summary_row + 4, column=2, value=f"{total_duration:.0f} seconds ({total_duration/60:.1f} min)")

    widths = [6, 15, 12, 7, 8, 8, 8, 10, 8, 8, 12, 10, 10, 10]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[chr(64 + i)].width = w

    path = os.path.join(REPORTS_DIR, f"Client_Regression_Report_{TIMESTAMP}.xlsx")
    os.makedirs(REPORTS_DIR, exist_ok=True)
    wb.save(path)
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=5, help="Parallel workers (default: 5)")
    parser.add_argument("--smoke", action="store_true", help="Run only E2E/smoke (R9+R10) - faster")
    args = parser.parse_args()

    clients = load_clients()
    print(f"\n{'='*60}")
    print(f"  PARALLEL CLIENT RUNNER")
    print(f"{'='*60}")
    print(f"  Clients:  {len(clients)}")
    print(f"  Workers:  {args.workers} (parallel)")
    print(f"  Mode:     {'SMOKE (R9+R10 only)' if args.smoke else 'FULL REGRESSION'}")
    print(f"{'='*60}\n")

    start = datetime.now()
    all_results = []

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(run_client, c, args.smoke): c for c in clients}
        for fut in as_completed(futures):
            client, allure_dir, rc, duration = fut.result()
            results = parse_results(allure_dir)
            all_results.append((client, results, duration))

    # Sort by merchant_id for consistent order
    all_results.sort(key=lambda x: x[0]["merchant_id"])

    total_duration = (datetime.now() - start).total_seconds()
    excel_path = generate_excel(all_results, total_duration)

    # Final summary
    total = len(all_results)
    passed = sum(1 for _, r, _ in all_results if r["failed"] == 0 and r["broken"] == 0 and r["total"] > 0)

    print(f"\n{'='*60}")
    print(f"  BATCH COMPLETE")
    print(f"{'='*60}")
    print(f"  Total Clients: {total}")
    print(f"  Passed:        {passed}")
    print(f"  Failed:        {total - passed}")
    print(f"  Duration:      {total_duration:.0f} seconds ({total_duration/60:.1f} min)")
    print(f"  Excel Report:  {excel_path}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
