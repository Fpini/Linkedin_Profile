import duckdb

conn = duckdb.connect()

a = conn.execute ('''CREATE TABLE Connections AS SELECT *
FROM read_csv('Connections.csv')''')

print(conn.sql('SHOW TABLES'))

print(conn.sql('''select count(*) from Connections'''))

print(conn.sql('''select * from Connections Limit 5'''))

print(conn.sql('''select Company, count(*) as conteggio from Connections group by all order by conteggio desc'''))

print(conn.sql('''select Position, count(*) as conteggio from Connections group by all order by conteggio desc'''))

print(conn.sql('''select "Email Address", count(*) as conteggio from Connections group by all order by conteggio desc'''))

b = conn.execute('''CREATE VIEW my_view AS
SELECT 
    CAST("First Name" AS VARCHAR) AS firstname,
    CAST("Last Name" AS VARCHAR) AS lastname,
    CAST(URL AS VARCHAR) AS url,
    CAST("Email Address" AS VARCHAR) AS emailaddress,
    CAST(Company AS VARCHAR) AS company,
    CAST(Position AS VARCHAR) AS position,
    STRPTIME("Connected On", '%d %b %Y') AS connectedon
FROM read_csv_auto('Connections.csv', AUTO_DETECT=TRUE)''')

print(conn.sql('''select year(connectedon), company, count(*) from my_view group by all order by all'''))