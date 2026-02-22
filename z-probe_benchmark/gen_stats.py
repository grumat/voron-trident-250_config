#!py -3
# This work is derived from `probe_accuracy.py` and customizes the 
# results for my Wiki page.
#
# spellchecker:words ztrace zstddevtrace btrace btemp bset bstrace etemp eset etrace atherms estrace rangemode showlegend tozero tozeroy zrange

import argparse
import json
import os
import math
from statistics import pstdev, fmean
import numpy as np
from scipy.optimize import curve_fit

import plotly.graph_objects as pgo
from plotly.subplots import make_subplots

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

# Samples to evaluate for power transitions
OFFSET_POWER = 20
# Samples to evaluate for temperature offset shifts
OFFSET_TEMP = 30

SOAK_QUALITY = 0.2/6

parser = argparse.ArgumentParser()
parser.add_argument('--data', default='./data/probe_accuracy_0.json')
parser.add_argument('--out', default='./data/probe_accuracy_0.jpg')
parser.add_argument('--title', default='Probe Accuracy: Standard')
parser.add_argument('--alt', action='store_true')


class HeatSoak(object):
	"""Computes heat soak values for phase having heat bead and hot end active"""
	def __init__(self, soak_time_from : int, soak_time_to : int  = -1) -> None:
		self.soak_time_from = soak_time_from
		self.soak_time_to = soak_time_to
		self.sd = 0.0
		self.diff = 0.0
		self.avg = 0.0
	def ComputeSoak(self, data : list[tuple[float, float]], cold : float):
		offset = data[0][0]
		start = self.soak_time_from * 60.0 + offset
		if self.soak_time_to > 0:
			stop = self.soak_time_to * 60.0 + offset
			samples = [z for ts, z in data if start <= ts and ts < stop ]
		else:
			samples = [z for ts, z in data if ts >= start]
		self.sd = pstdev(samples)
		self.diff = max(samples) - min(samples)
		self.avg = fmean(samples)
		self.displace = self.avg - cold
	def Print(self, z_extrapolated : float, prev : HeatSoak|None = None):
		if self.soak_time_to < 0:
			print("Total")
		else:
			print(f"After {self.soak_time_from} min")
		print(f"    Z avg = {self.avg:6.3f} mm")
		print(f"    Z comp = {self.avg-z_extrapolated:6.3f} mm")
		print(f"    Z disp = {self.displace:6.3f} mm")
		print(f"    Z stdev = {1000.0 * self.sd:6.3f} µm")
		print(f"    Z diff = {1000.0 * self.diff:6.2f} µm")
		if prev:
			rate = 1000.0*(self.avg - prev.avg)/float(self.soak_time_from - prev.soak_time_from)
			print(f"    Z prev = {rate:6.3f} µm/min")

def ExpDecayFunc(t, V0, tau):
	"""Define the model with V0 expressed in terms of tau"""
	return V0 * np.exp(-t / tau)


class SoakStats(object):
	def __init__(self, cold :list[float], data : list[tuple[float, float]]) -> None:
		self.cold = cold
		self.cold_avg = fmean(cold)
		self.data = data
		self.total = HeatSoak(0)
		self.total.ComputeSoak(data, self.cold_avg)
		self.m : list[HeatSoak] = []
		for i in range(30):
			hs = HeatSoak(i, i+1)
			hs.ComputeSoak(data, self.cold_avg)
			self.m.append(hs)
	def ExpDecayFunc(self, t, tau = None):
		if not tau:
			tau = self.tau_fit
		V0 = self.z_last * np.exp(self.t_last / tau)
		return V0 * np.exp(-t / tau)
	def make_decay_(self, t, z):
		# Last point (anchor)
		self.t_last, self.z_last = t[-1], z[-1]
		# Fit the model to the data (only tau is fitted)
		params, _ = curve_fit(self.ExpDecayFunc, np.array(t), np.array(z), p0=[2])
		self.tau_fit = params[0]
		# Calculate V0 using the fitted tau
		#self.z0_fit = self.z_last * np.exp(self.t_last / self.tau_fit)

	def select_by_error(self, max_err : float):
		t_soak = 29
		z_soak = self.z_extrapolated
		for i in range(29, 0, -1):
			za = self.m[i].avg
			dif = abs(za - self.ExpDecayFunc(i))
			if dif >= max_err:
				break
			t_soak = i
			z_soak = za
		return (t_soak, z_soak, dif)

	def MakeFit(self):
		# Collect all data
		ts = []
		z = []
		for i in range(30):
			ts.append(self.m[i].soak_time_from)
			z.append(self.m[i].avg)
		# First approach used the tail samples
		self.make_decay_(ts[15:], z[15:])
		ts2 = ts.copy()
		z2 = z.copy()
		self.z_extrapolated = self.ExpDecayFunc(60.0)
		# Lear peak error rate and doubles it
		err_max = (SOAK_QUALITY + 3*max(abs(self.m[i].avg - self.ExpDecayFunc(i)) for i in range(15,30))) / 4.0

		# Widens the range accepting more error
		t_soak, z_soak, err_max = self.select_by_error(err_max)
		# Recompute if improved
		if t_soak < 15:
			self.make_decay_(ts[t_soak:], z[t_soak:])
			self.z_extrapolated = self.ExpDecayFunc(60.0)
		# Now compute the absolute distance to extrapolated Z
		self.t_soak = 29
		self.z_soak = self.m[29].avg
		for i in range(29, 0, -1):
			za = self.m[i].avg
			dif = abs(za - self.z_extrapolated)
			if dif >= SOAK_QUALITY:
				break
			self.t_soak = i
			self.z_soak = za

	def Print(self):
		print("===Heat Soak Statistics===")
		print(f"Extrapolation = {self.z_extrapolated:6.4f} mm")
		self.total.Print(self.z_extrapolated)
		self.m[0].Print(self.z_extrapolated)
		prev = 0
		for i in [1, 2, 3, 5, 7, 10, 15, 20, 25]:
			self.m[i].Print(self.z_extrapolated, self.m[prev])
			prev = i



def load_data(data_file: str) -> list:
	if not os.path.isabs(data_file):
		data_file = os.path.normpath(os.path.join(SCRIPT_DIR, data_file))
	with open(data_file, 'r') as f:
		data = [json.loads(line) for line in f]
	# Find minimum Z
	z_min = min([x['z'] for x in data if 'z' in x])
	# Anchor all z samples to that reference (this highly depends on current z_offset calibration from Klipper)
	for sample in data:
		if 'z' in sample:
			sample['z'] = sample['z'] - z_min
	return data


def write_chart(data: list, output_file: str, chart_title: str, alt : bool, soak_stats : SoakStats):

	if not os.path.isabs(output_file):
		output_file = os.path.normpath(os.path.join(SCRIPT_DIR, output_file))

	soak_start = soak_stats.data[0][0] / -60

	def SecToMin(v):
		return v / 60 + soak_start;

	z_trace = pgo.Scatter(
		x=[SecToMin(x['ts']) for x in data if 'z' in x],
		y=[z['z'] for z in data if 'z' in z],
		name='Z',
		mode='lines',
		line={'color': 'orange'},
		yaxis='y2'
	)

	z_extrapolated = pgo.Scatter(
		#x=[-5, 41],
		#y=[soak_stats.extrapolated_z, soak_stats.extrapolated_z],
		x=[SecToMin(x['ts']) for x in data if 'z' in x],
		y=[soak_stats.z_extrapolated for z in data if 'z' in z],
		line={'color': 'orange'},
		showlegend=False,
		mode='none',
		fill='tonexty',
		fillcolor='rgba(255,165,0,0.3)',
		yaxis='y2'
	)

	z_thr = pgo.Scatter(
		x=[soak_stats.t_soak], y=[soak_stats.z_soak],
		mode='markers',
		name='Heat soak threshold',
		marker=dict(size=8, color='blue'),
		yaxis='y2'
	)

	# Generate fitted curve
	time_fit = np.linspace(-5, 41, 20)
	z_fit = soak_stats.ExpDecayFunc(time_fit, soak_stats.tau_fit)
	z_discharge = pgo.Scatter(
		x=time_fit, y=z_fit,
		mode='lines',
		name=f'Fit: $V_0 e^{{-t/\\tau}}$',
		line=dict(color='darkgreen', width=2),
		yaxis='y2'
	)

	z_stdev_trace = pgo.Scatter(
		x=[ts for i, ts in enumerate(z_trace.x) if i >= 4],
		y=[pstdev(z_trace.y[i-4:i+1]) * 1000 for i, ts in enumerate(z_trace.y) if i >= 4],
		name='Z stddev',
		mode='markers',
		line={'color': 'gray'},
		yaxis='y3'
	)

	bed_trace = pgo.Scatter(
		x=[SecToMin(x['ts']) for x in data if 'btemp' in x],
		y=[x['btemp'] for x in data if 'btemp' in x],
		name='Bed temperature',
		mode='lines',
		line={'color': 'blue'}
	)

	extruder_trace = pgo.Scatter(
		x=[SecToMin(x['ts']) for x in data if 'etemp' in x],
		y=[x['etemp'] for x in data if 'etemp' in x],
		name='Extruder temperature',
		mode='lines',
		line={'color': 'red'}
	)
	soaking_bkg = pgo.Scatter(
		x=[SecToMin(x['ts']) for x in data if ('eset' in x) and 0 <= x['ts']],
		y=[soak_stats.z_extrapolated for z in data if ('eset' in z) and 0 <= z['ts']],
		showlegend=False,
		mode='none',
		fill='tozeroy',
		fillcolor='rgba(255,160,160,0.3)'
	)

	layout = pgo.Layout(
		autosize=False,
		width=1280,
		height=600
	)
	fig = pgo.Figure(layout=layout)
	fig.add_trace(z_trace)
	fig.add_trace(z_extrapolated)
	fig.add_trace(z_stdev_trace)
	fig.add_trace(z_discharge)
	fig.add_trace(bed_trace)
	fig.add_trace(extruder_trace)
	#fig.add_trace(soaking_bkg)
	fig.add_trace(z_thr)
	#fig.add_trace(z_dots)

	thermistors_xy = {}
	for d in data:
		if not 'atherms' in d:
			continue

		ts = SecToMin(d['ts'])
		for ad in d['atherms']:
			therm_id = ad['id']
			temp = ad['temp']
			try:
				thermistors_xy[therm_id]['x'].append(ts)
				thermistors_xy[therm_id]['y'].append(temp)
			except KeyError:
				thermistors_xy[therm_id] = {
					'x': [ts],
					'y': [temp]
				}

	for therm_id, xy in thermistors_xy.items():
		trace = pgo.Scatter(
			x=xy['x'],
			y=xy['y'],
			name=f'{therm_id} temperature',
			mode='lines'
		)
		fig.add_trace(trace)

	if alt:
		zrange = None
	else:
		z_max = max(z_trace.y)
		z_hi = 0.3
		while z_hi < z_max:
			z_hi += 0.2
		zrange = [-0.1,z_hi]

	fig.update_layout(
		title=dict(
			text=chart_title
		),
		legend=dict(
			x=1.1
		),
		xaxis=dict(
			title='minutes',
			domain=[0, 0.9]
		),
		yaxis=dict(
			title='°C',
		),
		yaxis2=dict(
			title='Z soak = 60 min / {0:.3f} mm → {1} min / Δ {2:.3f} mm'.format(soak_stats.z_extrapolated, soak_stats.t_soak, soak_stats.z_soak-soak_stats.z_extrapolated),
			anchor='x',
			overlaying='y',
			side='right',
			position=0.9,
			range=zrange
		),
		yaxis3=dict(
			title='Z10+ stddev = {:.2f} µm'.format(1000.0 * soak_stats.m[10].sd),
			rangemode='tozero',
			anchor='free',
			overlaying='y',
			side='right',
			position=1.0,
			range=[0,20]
		),
	)

	fig.write_image(output_file)


def real_world_stats(data : list) -> SoakStats:
	"Only the phase where heat-bed and hot-end are on are actually important"
	min_ts = data[0]['ts']
	cold_ts = min_ts + 5*60.0
	start_found = False
	cold = []
	samples = []
	for i, rec in enumerate(data):
		if "etemp" in rec:
			if not start_found:
				if rec["eset"] != 0.0:
					# Start of phase 3 with stable temp
					if abs(rec["etemp"] - rec["eset"]) <= 1.0:
						start_found = True
			elif rec["eset"] == 0.0:
				# End of phase 3
				break
		if "z" in rec:
			ts = rec["ts"]
			z = rec["z"]
			if (ts <= cold_ts):
				cold.append(z)
			if start_found:
				samples.append((ts, z))
	# Soaking statistics
	soak_stats = SoakStats(cold, samples)
	# Find a decay function
	soak_stats.MakeFit()
	return soak_stats




def moving_stats(col : list):
	all_sdy = pstdev(col) * 1000.0
	all_dif = (max(col) - min(col)) * 1000.0
	# Stddev of each 10 group
	stddev_set = [pstdev(col[i-9:i+1]) * 1000 for i, ts in enumerate(col) if i >= 9]
	sdy = fmean(stddev_set)
	dif = [(max(col[i-9:i+1]) - min(col[i-9:i+1])) for i, ts in enumerate(col) if i >= 9]
	dif = fmean(dif) * 1000.0
	return all_sdy, all_dif, sdy, dif


def print_stats(data : list, title : str):
	min_ts = data[0]['ts']
	start_btemp = data[0]['btemp']
	start_etemp = data[0]['etemp']

	print('{:}\n'.format(title))
	print('Start Condition:')
	print('- Bed Temperature: {:.1f}'.format(start_btemp))
	print('- Nozzle Temperature: {:.1f}'.format(start_etemp))
	print()

	cur_t = 0.0
	phase = 1
	phase1 = []
	phase2 = []
	phase3 = []
	phase4 = []
	all_z = []
	for d in data:
		if 'z' in d:
			z = d['z']
			all_z.append(z)
			if phase == 1:
				phase1.append(z)
			elif phase == 2:
				phase2.append(z)
			elif phase == 3:
				phase3.append(z)
			else:
				phase4.append(z)
		else:
			cur_t = d['ts'] - min_ts
			bed_temp = d['btemp']
			bed_set = d['bset']
			if phase == 1:
				if bed_set:
					phase = 2
			elif phase == 2:
				if bed_temp >= bed_set:
					phase = 3
			elif phase == 3:
				if bed_set == 0.0:
					phase = 4


	# Moving window
	asdy0, adif0, sdy0, dif0 = moving_stats(all_z)
	asdy1, adif1, sdy1, dif1 = moving_stats(phase1)
	asdy2, adif2, sdy2, dif2 = moving_stats(phase2)
	asdy3, adif3, sdy3, dif3 = moving_stats(phase3)
	asdy4, adif4, sdy4, dif4 = moving_stats(phase4)

	print('Stats for Moving Window of 10 Consecutive Elements:')
	print('- All Phases Total Diff/StdDev (all) |  Local Diff/StdDev:  {:5.2f} µm / {:5.2f} µm  |  {:5.2f} µm / {:5.2f} µm'.format(adif0, asdy0, dif0, sdy0))
	print('- Phase 1 Total Diff/StdDev (all)    |  Local Diff/StdDev:  {:5.2f} µm / {:5.2f} µm  |  {:5.2f} µm / {:5.2f} µm'.format(adif1, asdy1, dif1, sdy1))
	print('- Phase 2 Total Diff/StdDev (all)    |  Local Diff/StdDev:  {:5.2f} µm / {:5.2f} µm  |  {:5.2f} µm / {:5.2f} µm'.format(adif2, asdy2, dif2, sdy2))
	print('- Phase 3 Total Diff/StdDev (all)    |  Local Diff/StdDev:  {:5.2f} µm / {:5.2f} µm  |  {:5.2f} µm / {:5.2f} µm'.format(adif3, asdy3, dif3, sdy3))
	print('- Phase 4 Total Diff/StdDev (all)    |  Local Diff/StdDev:  {:5.2f} µm / {:5.2f} µm  |  {:5.2f} µm / {:5.2f} µm'.format(adif4, asdy4, dif4, sdy4))
	print()


def main():
	args = parser.parse_args()

	data = load_data(args.data)
	soak_stats = real_world_stats(data)

	write_chart(data, args.out, args.title, args.alt, soak_stats)
	print_stats(data, args.title)

	soak_stats.Print()
	print()
	print()


if __name__ == '__main__':
	main()
