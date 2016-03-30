#/usr/bin/python
import os
import sys
import time
import logging
import datetime
import logging.handlers

class TVRefresher:
	def __init__(self):
		
		##
		## Logging changes
		LOG_FILENAME = '/logdirhere'
		self.logger = logging.getLogger('MyLogger')
		self.logger.setLevel(logging.DEBUG)
		handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=4096, backupCount=10)
		self.logger.addHandler(handler)
		
		##
		## Set params and scan
		self.param_dict = self.set_params()
		try:
			self.scan_folders()
		except:
			self.logger.exception('Exception')
	
	def set_params(self):
		parameters = {}
		home_dir = os.path.expanduser('~')
		parameters['home_dir'] = home_dir
		parameters['tv_dir'] = os.path.join(home_dir, '/tv/')
		parameters['out_dir'] = os.path.join(home_dir, './tvrefresh')
		return parameters			

	def scan_folders(self):
		tv_root = self.param_dict['tv_dir']
		tv_tree = next(os.walk(tv_root))[1]
		
		##
		## For every TV series folder in /tv/
		for series_folder in tv_tree:
			series_abspath = os.path.join(tv_root,series_folder)
			series_date = datetime.datetime.fromtimestamp(os.path.getmtime(series_abspath))
			series_seasons = next(os.walk(series_abspath))[1]
			
			##
			## For every season subfolder in the current TV series
			for season in series_seasons:
				season_abspath = os.path.join(tv_root,series_folder,season)
				season_date = datetime.datetime.fromtimestamp(os.path.getmtime(season_abspath))
				
				##
				## If the tv series mdate is older than season date
				## the subfolder has been updated, so update rootfolder
				if series_date < season_date:
					os.utime(series_abspath,None)
					loginfostr = '{}{}{}{}'.format('Series Updated: ', season, ' >> Time at: ', str(season_date))
					self.logger.info(loginfostr)

if __name__ == '__main__':
	TVRefresher()
	
	