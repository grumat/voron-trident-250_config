#!py -3
# Takes results.txt and produces tables for markdown.

import re

BLOCK1 = re.compile(r'.+Local Diff/StdDev:\s+([\d\.-]+)\sµm\s/\s+([\d\.-]+)\sµm\s+\|\s+([\d\.-]+)\sµm\s/\s+([\d\.-]+)\sµm')
BLOCK2 = re.compile(r'\s+Z\s[adefigprstv]+\s=\s+([\d\.-]+)\s[mµ]m')

class Sensor:
	def __init__(self, title : str) -> None:
		self.title = title
		self.part1 = []
		self.avg = []
		self.disp = []
		self.stddev = []
		self.diff = []
		self.prev = []

class Tables:
	def __init__(self) -> None:
		self.sensors : list[Sensor] = []

	def Block1(self, cursor, sensor: Sensor):
		found = False
		row1 = []
		row2 = []
		row3 = []
		row4 = []
		while found == False:
			mark = ""
			while not mark:
				mark = next(cursor).rstrip()
			if mark == "Stats for Moving Window of 10 Consecutive Elements:":
				found = True
				for i in range(5):
					m = BLOCK1.match(next(cursor).rstrip())
					row1.append(m[1])
					row2.append(m[2])
					row3.append(m[3])
					row4.append(m[4])
		sensor.part1 = [row1, row2, row3, row4]
	
	def Block2(self, cursor, sensor: Sensor):
		found = False
		while found == False:
			mark = ""
			while not mark:
				mark = next(cursor).rstrip()
			if mark == "===Heat Soak Statistics===":
				found = True
				next(cursor)	# eat title
				for i in range(10):
					m = BLOCK2.match(next(cursor).rstrip())
					sensor.avg.append(m[1])
					m = BLOCK2.match(next(cursor).rstrip())
					sensor.disp.append(m[1])
					m = BLOCK2.match(next(cursor).rstrip())
					sensor.stddev.append(m[1])
					m = BLOCK2.match(next(cursor).rstrip())
					sensor.diff.append(m[1])
					m = BLOCK2.match(next(cursor).rstrip())
					if m:
						sensor.prev.append(m[1])
						next(cursor)

	def LocateHead(self, cursor):
		try:
			title = ""
			while True:
				while not title:
					title = next(cursor).rstrip()
				mark = ""
				while not mark:
					mark = next(cursor).rstrip()
				if mark == "Start Condition:":
					sensor = Sensor(title)
					self.Block1(cursor, sensor)
					self.Block2(cursor, sensor)
					self.sensors.append(sensor)
					title = ""
				else:
					title = mark
		except StopIteration:
			pass

	def Print(self):
		print('### Sample Difference (µm)')
		print()
		print('| Z-Probe            | Overall | Phase 1 | Phase 2 | Phase 3 | Phase 4 |')
		print('|--------------------|:-------:|:-------:|:-------:|:-------:|:-------:|')
		for sensor in self.sensors:
			print('| {0:19}| {1:>7} | {2:>7} | {3:>7} | {4:>7} | {5:>7} |'.format(sensor.title, *tuple(sensor.part1[0])))
		print()
		print()

		print('### Standard Deviation (µm)')
		print()
		print('| Z-Probe            | Overall | Phase 1 | Phase 2 | Phase 3 | Phase 4 |')
		print('|--------------------|:-------:|:-------:|:-------:|:-------:|:-------:|')
		for sensor in self.sensors:
			print('| {0:19}| {1:>7} | {2:>7} | {3:>7} | {4:>7} | {5:>7} |'.format(sensor.title, *tuple(sensor.part1[1])))
		print()
		print()

		print('### Sample Difference (µm)')
		print()
		print('| Z-Probe            | Overall | Phase 1 | Phase 2 | Phase 3 | Phase 4 |')
		print('|--------------------|:-------:|:-------:|:-------:|:-------:|:-------:|')
		for sensor in self.sensors:
			print('| {0:19}| {1:>7} | {2:>7} | {3:>7} | {4:>7} | {5:>7} |'.format(sensor.title, *tuple(sensor.part1[2])))
		print()
		print()

		print('### Standard Deviation (µm)')
		print()
		print('| Z-Probe            | Overall | Phase 1 | Phase 2 | Phase 3 | Phase 4 |')
		print('|--------------------|:-------:|:-------:|:-------:|:-------:|:-------:|')
		for sensor in self.sensors:
			print('| {0:19}| {1:>7} | {2:>7} | {3:>7} | {4:>7} | {5:>7} |'.format(sensor.title, *tuple(sensor.part1[3])))
		print()
		print()
		print()

		#####################################################################################

		print('## Average Z Value (in mm)')
		print()
		print('| Z-Probe            | No Soak | 1 Min  | 2 Min  | 3 Min  | 5 Min  | 7 Min  | 10 Min | 15 Min | 20 Min | 25 Min |')
		print('|--------------------|:-------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|')
		for sensor in self.sensors:
			print('| {0:19}| {1:>7} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} |'.format(sensor.title, *tuple(sensor.avg)))
		print()
		print()

		print('## Z Value Evolution (in µm/min)')
		print()
		print('| Z-Probe            |  1-2 Min  |  2-3 Min  |  3-5 Min  |  5-7 Min  | 7-10 Min  | 10-15 Min | 15-20 Min | 20-25 Min |')
		print('|--------------------|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|')
		for sensor in self.sensors:
			print('| {0:19}| {1:>9} | {2:>9} | {3:>9} | {4:>9} | {5:>9} | {6:>9} | {7:>9} | {8:>9} |'.format(sensor.title, *tuple(sensor.prev)))
		print()
		print()

		print('Z Value Displacement (Cold to Hot Values in mm)')
		print()
		print('| Z-Probe            | No Soak | 1 Min  | 2 Min  | 3 Min  | 5 Min  | 7 Min  | 10 Min | 15 Min | 20 Min | 25 Min |')
		print('|--------------------|:-------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|')
		for sensor in self.sensors:
			print('| {0:19}| {1:>7} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} |'.format(sensor.title, *tuple(sensor.disp)))
		print()
		print()

		print('## Standard Deviation (µm)')
		print()
		print('| Z-Probe            | No Soak | 1 Min  | 2 Min  | 3 Min  | 5 Min  | 7 Min  | 10 Min | 15 Min | 20 Min | 25 Min |')
		print('|--------------------|:-------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|')
		for sensor in self.sensors:
			print('| {0:19}| {1:>7} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} |'.format(sensor.title, *tuple(sensor.stddev)))
		print()
		print()

		print('## Amplitude Difference (µm)')
		print()
		print('| Z-Probe            | No Soak | 1 Min  | 2 Min  | 3 Min  | 5 Min  | 7 Min  | 10 Min | 15 Min | 20 Min | 25 Min |')
		print('|--------------------|:-------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|')
		for sensor in self.sensors:
			print('| {0:19}| {1:>7} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} |'.format(sensor.title, *tuple(sensor.diff)))
		print()
		print()


	def Do(self, fname : str):
		with open(fname) as fh:
			cursor = iter(fh)
			self.LocateHead(cursor)
		cursor = None


def main():
	t = Tables()
	t.Do("Results.txt")
	t.Print()

if __name__ == '__main__':
	main()
