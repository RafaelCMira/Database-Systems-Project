#!/usr/bin/tclsh

# Configurations

# Set PostgreSQL as Database
dbset db pg
# Set the benchmark
dbset bm TPC-C

# 1. Schema

# Number of warehouses
diset tpcc pg_count_ware 40
# Number of vusers
diset tpcc pg_num_vu 8


# 2. Driver script Options

diset tpcc pg_driver timed

# Transactions per user
diset tpcc pg_total_iterations 1000000
# Ramp up minutes
diset tpcc pg_rampup 2
# Test duration
diset tpcc pg_duration 10

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

foreach z {8 11 16 24} {
puts "Starting $z VU TEST"

# Set Vusers
vuset vu $z

# Run Vusers
vucreate
vurun

# Destroy Vusers
vudestroy

# Wait for 30s
puts "Waiting 30s to start new VU test"
after 30000
}

# Stop transaction counter
tcstop



