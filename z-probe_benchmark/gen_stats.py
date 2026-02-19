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
	def ComputeSoak(self, data : list[tuple[float, float]], cold : float, z_min : float):
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
		self.displace0 = self.avg - z_min
	def Print(self, prev : HeatSoak|None = None):
		if self.soak_time_from == 0:
			print("Total")
		else:
			print(f"After {self.soak_time_from} min")
		print(f"    Z avg = {self.avg:6.4f} mm")
		print(f"    Z disp = {self.displace:6.4f} mm")
		print(f"    Z stdev = {1000.0 * self.sd:6.3f} µm")
		print(f"    Z diff = {1000.0 * self.diff:6.2f} µm")
		if prev:
			rate = 1000.0*(self.avg - prev.avg)/float(self.soak_time_from - prev.soak_time_from)
			print(f"    Z prev = {rate:6.3f} µm/min")


class SoakStats(object):
	def __init__(self, z_min : float, cold :list[float], data : list[tuple[float, float]]) -> None:
		self.z_min = z_min
		self.cold = cold
		self.cold_avg = fmean(cold)
		self.data = data
		self.total = HeatSoak(0)
		self.m0 = HeatSoak(0, 1)
		self.m1 = HeatSoak(1, 2)
		self.m2 = HeatSoak(2, 3)
		self.m3 = HeatSoak(3, 4)
		self.m5 = HeatSoak(5, 6)
		self.m7 = HeatSoak(7, 8)
		self.m10 = HeatSoak(10, 11)
		self.m15 = HeatSoak(15, 16)
		self.m20 = HeatSoak(20, 21)
		self.m25 = HeatSoak(25, 26)
		self.m29 = HeatSoak(29, 30)
		self.total.ComputeSoak(data, self.cold_avg, z_min)
		self.m0.ComputeSoak(data, self.cold_avg, z_min)
		self.m1.ComputeSoak(data, self.cold_avg, z_min)
		self.m2.ComputeSoak(data, self.cold_avg, z_min)
		self.m3.ComputeSoak(data, self.cold_avg, z_min)
		self.m5.ComputeSoak(data, self.cold_avg, z_min)
		self.m7.ComputeSoak(data, self.cold_avg, z_min)
		self.m10.ComputeSoak(data, self.cold_avg, z_min)
		self.m15.ComputeSoak(data, self.cold_avg, z_min)
		self.m20.ComputeSoak(data, self.cold_avg, z_min)
		self.m25.ComputeSoak(data, self.cold_avg, z_min)
		self.m29.ComputeSoak(data, self.cold_avg, z_min)
	def Print(self):
		print("===Heat Soak Statistics===")
		self.total.Print()
		self.m1.Print()
		self.m2.Print(self.m1)
		self.m3.Print(self.m2)
		self.m5.Print(self.m3)
		self.m7.Print(self.m5)
		self.m10.Print(self.m7)
		self.m15.Print(self.m10)
		self.m20.Print(self.m15)
		self.m25.Print(self.m20)



def load_data(data_file: str) -> list:
	if not os.path.isabs(data_file):
		data_file = os.path.normpath(os.path.join(SCRIPT_DIR, data_file))
	with open(data_file, 'r') as f:
		return [json.loads(line) for line in f]


def write_chart(data: list, output_file: str, chart_title: str, alt : bool, soak_stats : SoakStats):

	if not os.path.isabs(output_file):
		output_file = os.path.normpath(os.path.join(SCRIPT_DIR, output_file))

	min_ts = data[0]['ts']
	z_min = min([x['z'] for x in data if 'z' in x])


	ztrace = pgo.Scatter(
		x=[x['ts'] - min_ts for x in data if 'z' in x],
		y=[(x['z'] - z_min) for x in data if 'z' in x],
		name='Z',
		mode='lines',
		line={'color': 'orange'},
		yaxis='y2'
	)
	#######################################################################################################
	## Discharge curve Calculation
	#######################################################################################################
	soak_start = soak_stats.data[0][0] - min_ts

	time_data = np.array([5, 7, 10, 15, 20, 25, 29])
	z_avg_data = np.array([soak_stats.m5.avg - z_min, soak_stats.m7.avg - z_min, 
						  soak_stats.m10.avg - z_min, soak_stats.m15.avg - z_min, 
						  soak_stats.m20.avg - z_min, soak_stats.m25.avg - z_min, 
						  soak_stats.m29.avg - z_min])
	# Apply transformation
	time_data_transformed = (time_data * 60) + soak_start
	# Last point (anchor)
	t_last, z_last = time_data[-1], z_avg_data[-1]

	# Define the model with V0 expressed in terms of tau
	def exp_decay_anchored(t, tau):
		V0 = z_last * np.exp(t_last / tau)
		return V0 * np.exp(-t / tau)
	# Fit the model to the data (only tau is fitted)
	params, covariance = curve_fit(exp_decay_anchored, time_data, z_avg_data, p0=[2])
	tau_fit = params[0]
	# Calculate V0 using the fitted tau
	z0_fit = z_last * np.exp(t_last / tau_fit)
	# Generate fitted curve
	time_fit = np.linspace(-5, 40, 20)
	z_fit = exp_decay_anchored(time_fit, tau_fit)
	time_fit_transformed = (time_fit * 60) + soak_start

	z_dots = pgo.Scatter(
		x=time_data_transformed, y=z_avg_data,
		mode='markers',
		name='Approximation',
		marker=dict(size=8, color='blue'),
		yaxis='y2'
	)
	z_discharge = pgo.Scatter(
		x=time_fit_transformed, y=z_fit,
		mode='lines',
		name=f'Fit: $V_0 e^{{-t/\\tau}}$, $V_0$={z0_fit:.2f}, $\\tau$={tau_fit:.2f}',
		line=dict(color='darkgreen', width=2),
		yaxis='y2'
	)

	zn = exp_decay_anchored(60, tau_fit)
	for t in range(60, 2, -1):
		zt = exp_decay_anchored(t, tau_fit)
		if abs(zt - zn) > SOAK_QUALITY:
			break
	if t > 30:
		t = 30
	z_thr = pgo.Scatter(
		x=[(t * 60) + soak_start], y=[zt],
		mode='markers',
		name=f'Z thr',
		marker=dict(size=8, color='darkolivegreen'),
		yaxis='y2'
	)
	#######################################################################################################
	#######################################################################################################

	z_max = max(ztrace.y)
	z_hi = 0.3
	while z_hi < z_max:
		z_hi += 0.2
	
	sdy_local = [pstdev(ztrace.y[i-9:i+1]) * 1000 for i, ts in enumerate(ztrace.y) if i >= 9]
	final = fmean(sdy_local)
	dif_local = [(max(ztrace.y[i-9:i+1]) - min(ztrace.y[i-9:i+1])) for i, ts in enumerate(ztrace.y) if i >= 9]
	dif_local = fmean(dif_local)

	z_stdev_trace = pgo.Scatter(
		x=[ts for i, ts in enumerate(ztrace.x) if i >= 4],
		y=[pstdev(ztrace.y[i-4:i+1]) * 1000 for i, ts in enumerate(ztrace.y) if i >= 4],
		name='Z stddev',
		mode='markers',
		line={'color': 'gray'},
		yaxis='y3'
	)

	bed_trace = pgo.Scatter(
		x=[x['ts'] - min_ts for x in data if 'btemp' in x],
		y=[x['btemp'] for x in data if 'btemp' in x],
		name='bed temperature',
		mode='lines',
		line={'color': 'blue'}
	)

	extruder_trace = pgo.Scatter(
		x=[x['ts'] - min_ts for x in data if 'etemp' in x],
		y=[x['etemp'] for x in data if 'etemp' in x],
		name='extruder temperature',
		mode='lines',
		line={'color': 'red'}
	)
	soaking_bkg = pgo.Scatter(
		x=[x['ts'] - min_ts for x in data if ('eset' in x) and soak_start <= (x['ts'] - min_ts)],
		y=[x['eset'] for x in data if ('eset' in x) and soak_start <= (x['ts'] - min_ts)],
		showlegend=False,
		mode='none',
		fill='tozeroy',
		fillcolor='rgba(255,128,128,0.3)'
	)

	layout = pgo.Layout(
		autosize=False,
		width=1280,
		height=600
	)
	fig = pgo.Figure(layout=layout)
	fig.add_trace(ztrace)
	fig.add_trace(z_stdev_trace)
	fig.add_trace(z_discharge)
	fig.add_trace(bed_trace)
	fig.add_trace(extruder_trace)
	fig.add_trace(soaking_bkg)
	fig.add_trace(z_thr)
	#fig.add_trace(z_dots)

	thermistors_xy = {}
	for d in data:
		if not 'atherms' in d:
			continue

		ts = d['ts'] - min_ts
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
		zrange = [-0.1,z_hi]

	fig.update_layout(
		title=dict(
			text=chart_title
		),
		legend=dict(
			x=1.1
		),
		xaxis=dict(
			title='seconds',
			domain=[0, 0.9]
		),
		yaxis=dict(
			title='°C',
		),
		yaxis2=dict(
			title='Z soak = 60 min / {2:.3f} mm → {0} min / Δ {1:.3f} mm'.format(t, zt-zn, zn),
			anchor='x',
			overlaying='y',
			side='right',
			position=0.9,
			range=zrange
		),
		yaxis3=dict(
			title='Z10+ stddev = {:.2f} µm'.format(1000.0 * soak_stats.m10.sd),
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
	z_min = min([x['z'] for x in data if 'z' in x])
	return SoakStats(z_min, cold, samples)




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
