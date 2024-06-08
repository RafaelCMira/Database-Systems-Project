#!/usr/bin/tclsh

# Configurations

# Set PostgreSQL as Database
dbset db pg
# Set the benchmark
dbset bm TPC-C


diset connection pg_host posgres-database
diset connection pg_port 5432
diset connection pg_sslmode prefer

diset tpcc pg_superuser postgres
diset tpcc pg_superuserpass 1234
diset tpcc pg_defaultdb postgres
diset tpcc pg_user tpcc
diset tpcc pg_pass tpcc
diset tpcc pg_dbase tpcc
diset tpcc pg_tspace pg_default

# 1. Schema

# Number of warehouses
diset tpcc pg_count_ware 160
# Number of vusers
diset tpcc pg_num_vu 32


# 2. Driver script Options

diset tpcc pg_driver timed

# Transactions per user
diset tpcc pg_total_iterations 1000000
# Ramp up minutes
diset tpcc pg_rampup 1
# Test duration
diset tpcc pg_duration 9

# Use all warehouses (Optional, use in some tests)
diset tpcc pg_allwarehouse false

# Time profile (Mandatory for logs)
diset tpcc pg_timeprofile true

# Async connections (scalling) (Optional, use in some tests)
diset tpcc pg_async_scale false
# Clients per virtual user
diset tpcc pg_async_client 10

# 4. Transactions options
tcset refreshrate 10
tcset logtotemp 1
tcset unique 0
tcset timestamps 1

# Build schema

# Delete the schema if it exists
deleteschema
vudestroy

# Build the new schema
buildschema
vudestroy

# Load driver script
vudestroy
loadscript

# 3. Vuser options
vuset delay 500
vuset repeat 500
vuset iterations 1
vuset showoutput 0
vuset logtotemp 0
vuset unique 0
vuset nobuff 0
vuset timestamps 0


# Start transaction counter
tcstart

foreach z {8 16 32 64 100} {
    puts "Starting $z VU TEST"

    puts "Destroying VU"
    # Destroy Vusers
    vudestroy

    puts "Setting $z VU"
    # Set Vusers
    vuset vu $z

    puts "Creating and running $z VU"
    # Run Vusers
    vucreate
    vurun

    puts "Waiting 1 minute to destroy VU"
    after 60000
}

vudestroy

# Stop transaction counter
tcstop
