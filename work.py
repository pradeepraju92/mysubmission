import csv
import dateutil.parser as parser
import time
from datetime import datetime,timedelta
from dateutil import tz

#Class to normalize input csv file based on rules found in README.md
class CSVEditor:
	def __init__(self):	
		self.rowNumber = 0 #value used to track the rownumber to indicate the rowNumber error for unparseable data.
		self.isRowUnicodeValid = True #flag to keep track of data validity. If this flag is false then that specific row will be skipped from normalization process.
	
	def csvEdit(self):
		iFilename = input("Enter the inputfilename along with the path: ") #Input csv filename
		oFilename = input("Enter the outputfilename along with the path: ") #Output csv filename
		#Using dictReader to identify fieldnames and retrieve data using fieldnames as dictreader stored row as dictionary object.
		#Since the file is in UTF-8 character set, the data is encoded in UTF-8, characters failing the encoding process are replaced with unicode characters.
		csvReader = csv.DictReader(open(iFilename,'r+',encoding='UTF-8',errors='replace'),delimiter=',')
		csvWriter = csv.DictWriter(open(oFilename,'w+',encoding='UTF-8',errors='replace'),delimiter=',',fieldnames=csvReader.fieldnames,lineterminator='\n') 
		csvWriter.writeheader()
		for row in csvReader:
			self.rowNumber = self.rowNumber + 1
			self.isRowUnicodeValid = True
			output = {}
			output['Timestamp'] = self.csvTimeConverter(row['Timestamp'])
			output['Address'] = self.csvAddressConverter(row['Address'])
			output['ZIP'] = self.csvZipcodeConverter(row['ZIP'])
			output['FullName'] = self.csvNameConverter(row['FullName'])
			output['FooDuration'] = self.csvFooDurationConverter(row['FooDuration'])
			output['BarDuration'] = self.csvBarDurationConverter(row['BarDuration'])
			output['TotalDuration'] = self.csvTotalDurationConverter(row['TotalDuration'])
			output['Notes'] = self.csvNotesConverter(row['Notes'])
			if(self.isRowUnicodeValid):
				csvWriter.writerow(output)
		open(iFilename,'r+').close()
		open(oFilename,'w+').close()
		print("CSV file is normalized and output file is saved at " + str(oFilename))

	def timeZoneConverter(self,from_tz,to_tz,value):
	#function to convert PST to EST.
		from_tz = tz.gettz(from_tz)
		to_tz = tz.gettz(to_tz)
		value = datetime.strptime(value,'%Y-%m-%dT%H:%M:%S')
		value = value.replace(tzinfo=from_tz)
		estValue = value.astimezone(to_tz)
		return estValue.isoformat()
		
	def csvTimeConverter(self,value):
	#function to convert datetime format to ISO 8601 format.
		try:
			valDate = parser.parse(value)
			valDateISO = self.ISOFormatConverter(valDate)
			valDateISOEST = self.timeZoneConverter('America/Los_Angeles','America/New_York',valDateISO)
			return valDateISOEST
		except ValueError:
			print("Row number " + str(self.rowNumber) + " has unparseable data, hence ignoring.")
			self.isRowUnicodeValid = False
	
	def ISOFormatConverter(self,value):
		return value.isoformat()
	
	def csvAddressConverter(self,value):
	#function to return unicode valid address value.
		return value
	
	def csvZipcodeConverter(self,value):
	#function to normalize zip field.
		if(len(value) == 5):
			return value
		elif(len(value) < 5):
			return value.zfill(5) #zfill function will prefix the number with zero and the length of the resultant field should be of 5 character length.
		else:
			return value[0:5]
	
	def csvNameConverter(self,value):
	#function to return uppercase unicode valid name value.
		try:
			return value.upper()
		except ValueError:
			print("Row number " + str(self.rowNumber) + " has unparseable data, hence ignoring.")
			self.isRowUnicodeValid = False
		
	def csvFooDurationConverter(self,value):
	#function to convert time value to seconds.
		try:
			self.fooDurationSecs = 0
			hours, rest = value.split(':',1) #removing hours field separately as value goes beyond 24
			valTime = time.strptime(rest,'%M:%S.%f')
			self.fooDurationSecs = float(timedelta(hours=int(hours)).total_seconds()) + float(timedelta(minutes=valTime.tm_min,seconds=valTime.tm_sec).total_seconds()) + float('.'+value.split('.')[1]) #calculating total seconds using hour, minute,second, microsecond.
			return self.fooDurationSecs
		except ValueError:
			print("Row number " + str(self.rowNumber) + " has unparseable data, hence ignoring.")
			self.isRowUnicodeValid = False
	
	def csvBarDurationConverter(self,value):
	#function to convert time value to seconds.
		try:
			self.barDurationSecs = 0
			hours, rest = value.split(':',1)
			valTime = time.strptime(rest,'%M:%S.%f')
			self.barDurationSecs = float(timedelta(hours=int(hours)).total_seconds()) + float(timedelta(minutes=valTime.tm_min,seconds=valTime.tm_sec).total_seconds()) + float('.'+value.split('.')[1])
			return self.barDurationSecs
		except ValueError:
			print("Row number " + str(self.rowNumber) + " has unparseable data, hence ignoring.")
			self.isRowUnicodeValid = False

	def csvTotalDurationConverter(self,value):
	#function to return total duration which is a sum of fooDurationSecs and barDurationSecs
		return format(self.fooDurationSecs + self.barDurationSecs,'.3f')
		
	def csvNotesConverter(self,value):
	#function to return unicode valid notes text value.
		return value
		
def main():
	sample = CSVEditor()
	sample.csvEdit()

if __name__ == "__main__":
    main()
