#!/usr/bin/python

# MIT License
# 
# Copyright (c) 2017 John Bryan Moore
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import VL53L0X
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped

class rangeNode(Node):
	def __init__(self):
		super().__init__('delta_node')
		self.publisher = self.create_publisher(PointStamped, '/Delta', 10);
		timer_period = 0.1; # 10 Hz
		self.calls = 0;
		self.sensorObject = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x29); # from VL module
		self.sensorObject.open() # Activate sensor
		self.sensorObject.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER) #lol what a syntax
		self.sensor_timing = self.sensorObject.get_timing() # in the package, they set a lower limit of 20,000 , not sure why

		self.int_distance = 0
		self.timer = self.create_timer(timer_period, self.run);

	def run(self):

		if self.calls < 25:
			self.calls += 1
			self.int_distance = self.int_distance + self.sensorObject.get_distance()
			print("Taring %d/25" % self.calls)
		elif self.calls == 25:
			self.tare = self.int_distance / 25
			self.calls += 1
		# We have now call 25 readings and gotten the average, tare the sensor and read as normal
		else:
			distance_out = self.sensorObject.get_distance() - self.tare
			print("distance: %d \t tare value: %d" % (distance_out, self.tare))
def main(args=None):

	rclpy.init(args=args)
	range_node = rangeNode()
	rclpy.spin(range_node)
	range_node.destroy_node()
	rclpy.shutdown()


if __name__ == '__main__':

	main()

	## Create a VL53L0X object
#tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
	## I2C Address can change before tof.open()
	## tof.change_address(0x32)
#tof.open()
	## Start ranging
#tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

#timing = tof.get_timing()
#if timing < 20000:
#    timing = 20000
#print("Timing %d ms" % (timing/1000))

#for count in range(1, 101):
 #   distance = tof.get_distance()
  #  if distance > 0:
   #     print("%d mm, %d cm, %d" % (distance, (distance/10), count))

    #time.sleep(timing/1000000.00)

#tof.stop_ranging()
#tof.close()

