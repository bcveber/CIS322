import acp_times
import nose
import logging
import arrow

logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.WARNING)
log = logging.getLogger(__name__)

#times less than first
def small():
	date = arrow.Arrow(2013,5,5)
	assert acp_times.open_time(150, 200, arrow.get(date)) == (date.shift(hours=4,minutes=25)).isoformat()
	assert acp_times.close_time(150, 200, arrow.get(date)) == (date.shift(hours=10)).isoformat()

#additions of times
def big():
	date = arrow.Arrow(2013,5,5)
	assert acp_times.open_time(700, 1000, arrow.get(date)) == (date.shift(hours=22,minutes=22)).isoformat()
	assert acp_times.close_time(700, 1000, arrow.get(date)) == (date.shift(hours=48,minutes=45)).isoformat()

#time that is exactly equal
def exact():
	date = arrow.Arrow(2013,5,5)
	assert acp_times.open_time(600, 600, arrow.get(date)) == (date.shift(hours=18,minutes=48)).isoformat()
	assert acp_times.close_time(600, 600, arrow.get(date)) == (date.shift(hours=40)).isoformat()

#test control value of 550
def reg():
	date = arrow.Arrow(2013,5,5)
	assert acp_times.open_time(550, 600, arrow.get(date)) == (date.shift(hours=17,minutes=8)).isoformat()
	assert acp_times.close_time(550, 600, arrow.get(date)) == (date.shift(hours=36,minutes=40)).isoformat()

#control value that is odd
def oddnum():
	date = arrow.Arrow(2013,5,5)
	assert acp_times.open_time(311, 400, arrow.get(date)) == (date.shift(hours=9,minutes=21)).isoformat()
	assert acp_times.close_time(311, 400, arrow.get(date)) == (date.shift(hours=20,minutes=44)).isoformat()
