"""
Milestone 3 - Outland Adventures Reports
This script connects to the outland_adventures database and generates
three reports that help answer the business questions from the case study.

Reports:
1) Equipment sales by month (are equipment sales active enough?)
2) Bookings by destination and month (are certain regions trending down?)
3) Equipment older than five years (aging inventory)
"""

import mysql.connector


def get_connection():
    """Connect to the outland_adventures database."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="addimae69",
        database="outland_adventures"
    )
    return conn


def run_report(cursor, title, description, query):
    """Execute a query and print the results with a title and description."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    print(description)
    print("-" * 70)

    cursor.execute(query)
    rows = cursor.fetchall()
    col_names = cursor.column_names  # column headers

    # Print column headers
    header_line = " | ".join(col_names)
    print(header_line)
    print("-" * len(header_line))

    # Print each row
    for row in rows:
        row_values = [str(value) for value in row]
        print(" | ".join(row_values))

    if not rows:
        print("(no rows returned)")

    print("\n")  # blank line after each report


def main():
    conn = get_connection()
    cur = conn.cursor()

    # ------------------------------------------------------------------
    # Report 1: Equipment sales by month
    # ------------------------------------------------------------------
    report1_title = "Report 1: Equipment Sales by Month"
    report1_desc = (
        "Shows how many equipment items were sold each month and the total "
        "revenue for that month. This helps Outland Adventures decide whether "
        "equipment sales are strong enough to justify keeping the sales side "
        "of the business."
    )

    report1_sql = """
        SELECT
            DATE_FORMAT(SaleDate, '%Y-%m') AS SaleMonth,
            COUNT(*) AS NumberOfSales,
            SUM(SalePrice) AS TotalRevenue
        FROM EQUIPMENT_SALE
        GROUP BY DATE_FORMAT(SaleDate, '%Y-%m')
        ORDER BY SaleMonth;
    """

    run_report(cur, report1_title, report1_desc, report1_sql)

    # ------------------------------------------------------------------
    # Report 2: Bookings by destination and month
    # ------------------------------------------------------------------
    report2_title = "Report 2: Bookings by Destination and Month"
    report2_desc = (
        "Shows the number of bookings for each destination region by month. "
        "This helps Blythe and Jim see whether certain locations (Africa, "
        "Asia, Southern Europe) are trending downward in bookings over time."
    )

    report2_sql = """
        SELECT
            d.RegionName,
            DATE_FORMAT(ts.StartDate, '%Y-%m') AS TripMonth,
            COUNT(b.BookingID) AS NumberOfBookings
        FROM BOOKING b
        JOIN TRIP_SCHEDULE ts ON b.ScheduleID = ts.ScheduleID
        JOIN TRIP t ON ts.TripID = t.TripID
        JOIN DESTINATION d ON t.DestinationID = d.DestinationID
        GROUP BY d.RegionName, DATE_FORMAT(ts.StartDate, '%Y-%m')
        ORDER BY d.RegionName, TripMonth;
    """

    run_report(cur, report2_title, report2_desc, report2_sql)

    # ------------------------------------------------------------------
    # Report 3: Equipment older than five years
    # ------------------------------------------------------------------
    report3_title = "Report 3: Equipment Older Than Five Years"
    report3_desc = (
        "Lists equipment items with AgeInYears greater than 5, along with "
        "their category and current quantity. This helps identify old "
        "inventory that may need to be replaced or discounted."
    )

    report3_sql = """
        SELECT
            ItemName,
            Category,
            AgeInYears,
            QuantityAvailable
        FROM EQUIPMENT
        WHERE AgeInYears > 5
        ORDER BY AgeInYears DESC, ItemName;
    """

    run_report(cur, report3_title, report3_desc, report3_sql)

    # Close connection
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
