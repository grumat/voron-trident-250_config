#!py -3
# Takes results.txt and produces tables for markdown.

import argparse
import re
import sys
from contextlib import contextmanager

parser = argparse.ArgumentParser()
parser.add_argument('filename', default='Results.txt')
parser.add_argument('--out', default=None)


BLOCK1 = re.compile(r'.+Local Diff/StdDev:\s+([\d\.-]+)\sµm\s/\s+([\d\.-]+)\sµm\s+\|\s+([\d\.-]+)\sµm\s/\s+([\d\.-]+)\sµm')
EXTRAP = re.compile(r'Extrapolation = ([\d\.-]+) mm')
BLOCK2 = re.compile(r'\s+Z\s[acdefigmoprstv]+\s=\s+([\d\.-]+)\s[mµ]m')

class Sensor:
	def __init__(self, title : str) -> None:
		self.title = title
		self.part1 = []
		self.extrapolated = ""
		self.avg = []
		self.comp = []
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
				m = EXTRAP.match(next(cursor).rstrip())
				sensor.extrapolated = m[1]
				next(cursor)	# eat title
				for i in range(11):
					m = BLOCK2.match(next(cursor).rstrip())
					sensor.avg.append(m[1])
					m = BLOCK2.match(next(cursor).rstrip())
					sensor.comp.append(m[1])
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

	def Print(self, fh):
		print('### Sample Difference (µm)', file=fh)
		print(file=fh)
		print('| Z-Probe            | Overall | Phase 1 | Phase 2 | Phase 3 | Phase 4 |', file=fh)
		print('|--------------------|:-------:|:-------:|:-------:|:-------:|:-------:|', file=fh)
		for sensor in self.sensors:
			print('| {0:19}| {1:>7} | {2:>7} | {3:>7} | {4:>7} | {5:>7} |'.format(sensor.title, *tuple(sensor.part1[0])), file=fh)
		print(file=fh)
		print(file=fh)

		print('### Standard Deviation (µm)', file=fh)
		print(file=fh)
		print('| Z-Probe            | Overall | Phase 1 | Phase 2 | Phase 3 | Phase 4 |', file=fh)
		print('|--------------------|:-------:|:-------:|:-------:|:-------:|:-------:|', file=fh)
		for sensor in self.sensors:
			print('| {0:19}| {1:>7} | {2:>7} | {3:>7} | {4:>7} | {5:>7} |'.format(sensor.title, *tuple(sensor.part1[1])), file=fh)
		print(file=fh)
		print(file=fh)

		print('### Sample Difference (µm)', file=fh)
		print(file=fh)
		print('| Z-Probe            | Overall | Phase 1 | Phase 2 | Phase 3 | Phase 4 |', file=fh)
		print('|--------------------|:-------:|:-------:|:-------:|:-------:|:-------:|', file=fh)
		for sensor in self.sensors:
			print('| {0:19}| {1:>7} | {2:>7} | {3:>7} | {4:>7} | {5:>7} |'.format(sensor.title, *tuple(sensor.part1[2])), file=fh)
		print(file=fh)
		print(file=fh)

		print('### Standard Deviation (µm)', file=fh)
		print(file=fh)
		print('| Z-Probe            | Overall | Phase 1 | Phase 2 | Phase 3 | Phase 4 |', file=fh)
		print('|--------------------|:-------:|:-------:|:-------:|:-------:|:-------:|', file=fh)
		for sensor in self.sensors:
			print('| {0:19}| {1:>7} | {2:>7} | {3:>7} | {4:>7} | {5:>7} |'.format(sensor.title, *tuple(sensor.part1[3])), file=fh)
		print(file=fh)
		print(file=fh)
		print(file=fh)

		#####################################################################################

		print('## Average Z Value (in mm)', file=fh)
		print(file=fh)
		print('| Z-Probe            | Any Soak | 0 Min  | 1 Min  | 2 Min  | 3 Min  | 5 Min  | 7 Min  | 10 Min | 15 Min | 20 Min | 25 Min |', file=fh)
		print('|--------------------|:--------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|', file=fh)
		for sensor in self.sensors:
			print('| {0:19}| {1:>8} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} |'.format(sensor.title, *tuple(sensor.avg)), file=fh)
		print(file=fh)
		print(file=fh)

		print('## Z Value Offset To Extrapolation (in mm)', file=fh)
		print(file=fh)
		print('| Z-Probe            | Extrapolation | Any Soak | 0 Min  | 1 Min  | 2 Min  | 3 Min  | 5 Min  | 7 Min  | 10 Min | 15 Min | 20 Min | 25 Min |', file=fh)
		print('|--------------------|:-------------:|:--------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|', file=fh)
		for sensor in self.sensors:
			print('| {0:19}| {1:>13} | {2:>8} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} | {12:>6} |'.format(sensor.title, sensor.extrapolated, *tuple(sensor.comp)), file=fh)
		print(file=fh)
		print(file=fh)

		print('## Z Value Evolution (in µm/min)', file=fh)
		print(file=fh)
		print('| Z-Probe            |  0-1 Min  |  1-2 Min  |  2-3 Min  |  3-5 Min  |  5-7 Min  | 7-10 Min  | 10-15 Min | 15-20 Min | 20-25 Min |', file=fh)
		print('|--------------------|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|', file=fh)
		for sensor in self.sensors:
			print('| {0:19}| {1:>9} | {2:>9} | {3:>9} | {4:>9} | {5:>9} | {6:>9} | {7:>9} | {8:>9} | {9:>9} |'.format(sensor.title, *tuple(sensor.prev)), file=fh)
		print(file=fh)
		print(file=fh)

		print('Z Value Displacement (Cold to Hot Values in mm)', file=fh)
		print(file=fh)
		print('| Z-Probe            | Any Soak | 0 Min  | 1 Min  | 2 Min  | 3 Min  | 5 Min  | 7 Min  | 10 Min | 15 Min | 20 Min | 25 Min |', file=fh)
		print('|--------------------|:--------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|', file=fh)
		for sensor in self.sensors:
			print('| {0:19}| {1:>8} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} |'.format(sensor.title, *tuple(sensor.disp)), file=fh)
		print(file=fh)
		print(file=fh)

		print('## Standard Deviation (µm)', file=fh)
		print(file=fh)
		print('| Z-Probe            | Any Soak | 0 Min  | 1 Min  | 2 Min  | 3 Min  | 5 Min  | 7 Min  | 10 Min | 15 Min | 20 Min | 25 Min |', file=fh)
		print('|--------------------|:--------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|', file=fh)
		for sensor in self.sensors:
			print('| {0:19}| {1:>8} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} |'.format(sensor.title, *tuple(sensor.stddev)), file=fh)
		print(file=fh)
		print(file=fh)

		print('## Amplitude Difference (µm)', file=fh)
		print(file=fh)
		print('| Z-Probe            | Any Soak | 0 Min  | 1 Min  | 2 Min  | 3 Min  | 5 Min  | 7 Min  | 10 Min | 15 Min | 20 Min | 25 Min |', file=fh)
		print('|--------------------|:--------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|', file=fh)
		for sensor in self.sensors:
			print('| {0:19}| {1:>8} | {2:>6} | {3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>6} | {9:>6} | {10:>6} | {11:>6} |'.format(sensor.title, *tuple(sensor.diff)), file=fh)
		print(file=fh)
		print(file=fh)


	def Do(self, fname : str):
		with open(fname) as fh:
			cursor = iter(fh)
			self.LocateHead(cursor)
		cursor = None


@contextmanager
def open_or_stdout(file_path=None):
	if file_path is None:
		yield sys.stdout
	else:
		with open(file_path, 'w', encoding='UTF-8') as fh:
			yield fh


def main():
	args = parser.parse_args()
	t = Tables()
	t.Do(args.filename)
	with open_or_stdout(args.out) as fh:
		t.Print(fh)

if __name__ == '__main__':
	main()
