# outland_milestone2.py
# Milestone 2: Create Outland Adventures DB, insert data, and display tables

import mysql.connector


def get_server_connection():
    """Connect to MySQL server (no specific database yet)."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="addimae69"
    )
    return conn


def get_db_connection():
    """Connect directly to the outland_adventures database."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="addimae69",
        database="outland_adventures"
    )
    return conn


def create_database_and_tables():
    """Create database and all tables."""
    conn = get_server_connection()
    cur = conn.cursor()

    # 1. Create database
    cur.execute("CREATE DATABASE IF NOT EXISTS outland_adventures;")
    conn.commit()
    print("Database outland_adventures created (or already exists).")

    # From here on we work inside the database
    cur.execute("USE outland_adventures;")

    # 2. Drop tables if they exist (makes re-running easier)
    drop_order = [
        "EQUIPMENT_SALE",
        "EQUIPMENT_RENTAL",
        "BOOKING",
        "TRIP_SCHEDULE",
        "TRIP",
        "GUIDE",
        "EQUIPMENT",
        "DESTINATION",
        "CUSTOMER"
    ]
    for t in drop_order:
        cur.execute(f"DROP TABLE IF EXISTS {t};")

    # 3. Create tables
    create_statements = [

        # CUSTOMER
        """
        CREATE TABLE CUSTOMER (
            CustomerID INT AUTO_INCREMENT PRIMARY KEY,
            FirstName VARCHAR(50),
            LastName VARCHAR(50),
            Email VARCHAR(100),
            Phone VARCHAR(20)
        );
        """,

        # DESTINATION
        """
        CREATE TABLE DESTINATION (
            DestinationID INT AUTO_INCREMENT PRIMARY KEY,
            RegionName VARCHAR(50),
            Description VARCHAR(255)
        );
        """,

        # TRIP
        """
        CREATE TABLE TRIP (
            TripID INT AUTO_INCREMENT PRIMARY KEY,
            TripName VARCHAR(100),
            Description VARCHAR(255),
            DestinationID INT,
            BasePrice DECIMAL(10,2),
            FOREIGN KEY (DestinationID) REFERENCES DESTINATION(DestinationID)
        );
        """,

        # GUIDE
        """
        CREATE TABLE GUIDE (
            GuideID INT AUTO_INCREMENT PRIMARY KEY,
            FirstName VARCHAR(50),
            LastName VARCHAR(50),
            Phone VARCHAR(20),
            Email VARCHAR(100),
            ExperienceNotes VARCHAR(255)
        );
        """,

        # TRIP_SCHEDULE
        """
        CREATE TABLE TRIP_SCHEDULE (
            ScheduleID INT AUTO_INCREMENT PRIMARY KEY,
            TripID INT,
            GuideID INT,
            StartDate DATE,
            EndDate DATE,
            Capacity INT,
            FOREIGN KEY (TripID) REFERENCES TRIP(TripID),
            FOREIGN KEY (GuideID) REFERENCES GUIDE(GuideID)
        );
        """,

        # EQUIPMENT
        """
        CREATE TABLE EQUIPMENT (
            EquipmentID INT AUTO_INCREMENT PRIMARY KEY,
            ItemName VARCHAR(100),
            Description VARCHAR(255),
            Category VARCHAR(50),
            QuantityAvailable INT,
            PurchaseDate DATE,
            AgeInYears INT
        );
        """,

        # BOOKING
        """
        CREATE TABLE BOOKING (
            BookingID INT AUTO_INCREMENT PRIMARY KEY,
            CustomerID INT,
            ScheduleID INT,
            NumberOfPeople INT,
            BookingDate DATE,
            Status VARCHAR(20),
            FOREIGN KEY (CustomerID) REFERENCES CUSTOMER(CustomerID),
            FOREIGN KEY (ScheduleID) REFERENCES TRIP_SCHEDULE(ScheduleID)
        );
        """,

        # EQUIPMENT_RENTAL
        """
        CREATE TABLE EQUIPMENT_RENTAL (
            RentalID INT AUTO_INCREMENT PRIMARY KEY,
            CustomerID INT,
            EquipmentID INT,
            RentalDate DATE,
            ReturnDate DATE,
            RentalFee DECIMAL(10,2),
            FOREIGN KEY (CustomerID) REFERENCES CUSTOMER(CustomerID),
            FOREIGN KEY (EquipmentID) REFERENCES EQUIPMENT(EquipmentID)
        );
        """,

        # EQUIPMENT_SALE
        """
        CREATE TABLE EQUIPMENT_SALE (
            SaleID INT AUTO_INCREMENT PRIMARY KEY,
            CustomerID INT,
            EquipmentID INT,
            SaleDate DATE,
            SalePrice DECIMAL(10,2),
            FOREIGN KEY (CustomerID) REFERENCES CUSTOMER(CustomerID),
            FOREIGN KEY (EquipmentID) REFERENCES EQUIPMENT(EquipmentID)
        );
        """
    ]

    for stmt in create_statements:
        cur.execute(stmt)

    conn.commit()
    cur.close()
    conn.close()
    print("All tables created successfully.")


def insert_sample_data():
    """Insert sample rows into each table (6+ where needed)."""
    conn = get_db_connection()
    cur = conn.cursor()

    # CUSTOMER (6 rows)
    cur.execute("""
        INSERT INTO CUSTOMER (FirstName, LastName, Email, Phone) VALUES
        ('Emma','Collins','emma.collins@example.com','479-555-0101'),
        ('Noah','Ramirez','noah.ramirez@example.com','479-555-0102'),
        ('Sophia','Lee','sophia.lee@example.com','479-555-0103'),
        ('Liam','Johnson','liam.johnson@example.com','479-555-0104'),
        ('Olivia','Patel','olivia.patel@example.com','479-555-0105'),
        ('Ethan','Martinez','ethan.martinez@example.com','479-555-0106');
    """)

    # DESTINATION (3 rows)
    cur.execute("""
        INSERT INTO DESTINATION (RegionName, Description) VALUES
        ('Africa','Treks in Tanzania and Kenya'),
        ('Asia','Himalayan and Southeast Asia treks'),
        ('Southern Europe','Hiking in Greece and Italy');
    """)

    # TRIP (6 rows)
    cur.execute("""
        INSERT INTO TRIP (TripName, Description, DestinationID, BasePrice) VALUES
        ('Kilimanjaro Summit Trek',
         '8-day guided ascent of Mt. Kilimanjaro',1,3200.00),
        ('Serengeti Walking Safari',
         '5-day wildlife hiking and camping safari',1,2600.00),
        ('Himalayan Base Camp Adventure',
         '10-day trek to a Himalayan base camp',2,4100.00),
        ('Thai Jungle Explorer',
         '6-day jungle hike and river camping',2,2900.00),
        ('Greek Island Coastal Hike',
         '7-day coastal trail hike across Greek islands',3,2800.00),
        ('Alpine Village Trek',
         '7-day trek through European mountain villages',3,3000.00);
    """)

    # GUIDE (6 rows) – note escaped apostrophes using two single quotes
    cur.execute("""
        INSERT INTO GUIDE (FirstName, LastName, Phone, Email, ExperienceNotes) VALUES
        ('John','MacNell','479-555-0201',
         'mac.macnell@outlandadventures.com','Specializes in African treks'),
        ('D.B.','Marland','479-555-0202',
         'duke.marland@outlandadventures.com','Expert in Asian jungle routes'),
        ('Sarah','Park','479-555-0203',
         'sarah.park@outlandadventures.com','Experienced European hiking guide'),
        ('Miguel','Santos','479-555-0204',
         'miguel.santos@outlandadventures.com','Fluent in Spanish and Portuguese'),
        ('Hana','Kim','479-555-0205',
         'hana.kim@outlandadventures.com','High-altitude trekking specialist'),
        ('Luca','Rossi','479-555-0206',
         'luca.rossi@outlandadventures.com','Mediterranean coastal routes');
    """)

    # TRIP_SCHEDULE (5 rows)
    cur.execute("""
        INSERT INTO TRIP_SCHEDULE (TripID, GuideID, StartDate, EndDate, Capacity) VALUES
        (1, 1, '2026-06-10', '2026-06-18', 12),
        (1, 1, '2026-09-05', '2026-09-13', 10),
        (3, 2, '2026-04-01', '2026-04-11', 14),
        (5, 3, '2026-05-15', '2026-05-22', 16),
        (2, 1, '2026-07-20', '2026-07-25', 12);
    """)

    # EQUIPMENT (6 rows, including some older than 5 years)
    cur.execute("""
        INSERT INTO EQUIPMENT
            (ItemName, Description, Category, QuantityAvailable, PurchaseDate, AgeInYears)
        VALUES
        ('Summit Pro Tent','3-person four-season tent','Tent',15,'2021-03-10',4),
        ('Alpine Sleep Bag','0C mummy sleeping bag','Sleeping Bag',25,'2020-08-22',5),
        ('Trekking Poles','Adjustable carbon trekking poles','Poles',30,'2019-05-18',6),
        ('Trail Backpack','65L internal frame backpack','Backpack',20,'2022-01-05',3),
        ('Headlamp Plus','LED headlamp with batteries','Lighting',40,'2023-09-12',2),
        ('Camp Stove','Lightweight backpacking stove','Cooking',18,'2018-04-01',7);
    """)

    # BOOKING (6 rows)
    cur.execute("""
        INSERT INTO BOOKING
            (CustomerID, ScheduleID, NumberOfPeople, BookingDate, Status)
        VALUES
        (1, 1, 2, '2026-02-10', 'Confirmed'),
        (2, 1, 1, '2026-02-18', 'Confirmed'),
        (3, 3, 1, '2026-01-05', 'Confirmed'),
        (4, 4, 3, '2026-03-20', 'Pending'),
        (5, 5, 2, '2026-04-01', 'Cancelled'),
        (6, 2, 1, '2026-03-01', 'Confirmed');
    """)

    # EQUIPMENT_RENTAL (4 rows)
    cur.execute("""
        INSERT INTO EQUIPMENT_RENTAL
            (CustomerID, EquipmentID, RentalDate, ReturnDate, RentalFee)
        VALUES
        (1, 1, '2026-06-08', '2026-06-19', 120.00),
        (2, 2, '2026-06-08', '2026-06-19', 80.00),
        (3, 4, '2026-03-30', '2026-04-12', 65.00),
        (4, 3, '2026-05-13', '2026-05-24', 40.00);
    """)

    # EQUIPMENT_SALE (3 rows)
    cur.execute("""
        INSERT INTO EQUIPMENT_SALE
            (CustomerID, EquipmentID, SaleDate, SalePrice)
        VALUES
        (1, 5, '2026-02-11', 35.00),
        (3, 3, '2026-01-07', 70.00),
        (5, 4, '2026-04-03', 150.00);
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Sample data inserted into all tables.")


def show_tables():
    """Select and print all rows from each table (for screenshots)."""
    conn = get_db_connection()
    cur = conn.cursor()

    tables = [
        "CUSTOMER",
        "DESTINATION",
        "TRIP",
        "GUIDE",
        "TRIP_SCHEDULE",
        "EQUIPMENT",
        "BOOKING",
        "EQUIPMENT_RENTAL",
        "EQUIPMENT_SALE"
    ]

    for t in tables:
        cur.execute(f"SELECT * FROM {t};")
        rows = cur.fetchall()
        print("\n==============================")
        print(f"Table: {t}")
        print("==============================")
        for row in rows:
            print(row)

    cur.close()
    conn.close()


def main():
    create_database_and_tables()
    insert_sample_data()
    show_tables()


if __name__ == "__main__":
    main()
