import platform
from datetime import datetime
import time
import sqlite3
import serial
import obd.io
import obd.sensors
from obd.utils import scan_serial

PORTNAME = "COM8"
LOG_SENSORS = ["rpm", "speed", "throttle_pos", "load", "temp"]

conn = sqlite3.connect('obdlog.db')

try:
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS Log 
                 (id INTEGER PRIMARY KEY, timestamp TEXT, speed REAL, rpm REAL, load REAL, throttle REAL, coolant REAL)""")
    conn.commit()
    del c
    
    # Set up OBD port
    port = obd.io.OBDPort(PORTNAME, None, 2, 2)
    if port.State == 0:
        port.close()
        port = None
        raise Exception("Cannot connect to %s" % PORTNAME)
        
    # Logging
    print "Logging started"
    
    while True:
        now_utc = datetime.utcnow()
        
        results = {}
        results["timestamp"] = str(now_utc)
        for index in LOG_SENSORS:
            (name, value, unit) = self.port.sensor(index)
            results[obd.sensors.SENSORS[index].shortname] = value;

        tup = (results["timestamp"], 
               results["speed"], 
               results["rpm"], 
               results["load"], 
               results["throttle_pos"], 
               results["temp"])

        # Save row
        c = conn.cursor()
        c.execute("INSERT INTO Log (timestamp,speed,rpm,load,throttle,coolant) VALUES (?,?,?,?,?,?)", tup)
        conn.commit()
        
        print tup
        
        # Sleep for a moment, as it is REALLY fast
        time.sleep(0.2)
    
finally:
    print "Finished"
    conn.close()




