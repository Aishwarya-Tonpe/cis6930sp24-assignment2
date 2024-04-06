MOTIVATION

1. For what purpose was the dataset created?
The dataset was created to get more detailed information from the Norman PD website about the daily criminal incidents.

2. Who created the dataset and on behalf of which entity? 
The dataset was created by Aishwarya Tonpe for her CIS 6930 : Data Engineering course as a part of Assignment 2 which focused on Data Augmentatiob.

COMPOSITION

1. What do the instances that comprise the dataset represent?
The instances comprise of information about criminal incidents in Norman, Oklahoma derived, processed and augmented to give additional information
about the incidents

2. How many instances are there in total?
(The answer to this question is undetermined as we have not been told how many pdfs of incident summary reports will be scanned as a part of this assignment.
But the total number of instances will be amount to the total number of records combined across all the pdfs being traversed)

3. Does the dataset contain all possible instances or is it a sample of instances from a larger set?
The dataset is a sample of a larger set, the larger dataset consists of instances for daily activities in the past 2 months for every day.

4. What data does each instance consist of?
The data consists of text fields. The data consists of 8 text fields namely - Day of the Week, Time of Day, Weather, Location Rank, Side of Town,  Incident Rank, Nature, EMSSTAT
These fields are derived after processing dataa from the Norman Police Department's website for daily incident summaries. 

5. Is any information missing from individual instances?
Yes, information is missing from some of the instances. Some of the instances might have missing or dummy weather code as weather is 
dependent on the location and address. The address is used to determine the coordinates and then the coordinates are passed to the
weather API to determine the weather code. However, in some cases the coordinates of the location were not fetched accurately which
resulted into dummy or missing coordinates and a dummy weather code. In such cases the cooridnates are (999, 999) and the weather code
is -1. Also the side of town is determined using the coordinates and is missing in such cases.

6. Are there any errors, sources of noise, or redundancies in the dataset?
This data is augmented form the norman pd's daily incident summary. There are redundancies in some data which might have the same location,
same day, same time or hour and same incident type. In this case, the augmented data is redundant.

7. Is the dataset self-contained, or does it link to or otherwise rely on external resources?
The data is dependent on Norman PD's daily incident summary.

8. Does the dataset contain data that might be considered confidential (for example, data that is protected by legal privilege or by 
doctor-patient confidentiality, data that includes the content of individuals’ non-public communications)?
No.

9. Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety?
No.

COLLECTION PROCESS
1. How was the data associated with each instance acquired? Was the data directly observable, 
reported by subjects, or indirectly inferred/derived from other data (for example, part-of-speech tags, model-based guesses for 
age or language)?
The data was indirectly inferred from Norman PD's daily incident summary. There are 8 fields in the data, here is how every field was 
inferred:
a. Day of the week : Day of the week is inferred from DateTime Stamp in the incident Report. Sunday being Day 1 and Saturday being Day 7.
b. Time of the Day : Time of the day is inferred from DateTime Stamp in the incident Report and is essentially the hour in the Timestmap.
c. Weather : Weather is the WMO code which is fetched from the Weather API. The weather API takes the coordinates of the location and 
return the WMO code in its response. The coordinates are fetched using Google Maps API which takes the address of the place and returns
the coordinates.
d. Location Rank : For the Location rank all listed locations sorted and an integer ranking is given based on the frequency of locations 
with ties preserved. For instance, if there is a three-way tie for the most popular location, each location is ranked 1; 
the next most popular location is ranked 4
e. Side of town : Is determined based on the cooridnates by calculating the differences between the central and desired coordinates.
f. Incident Rank : All of the Natures are sorted. An integer ranking of the frequency of natures is assigned with ties preserved. 
For instance, if there is a three-way tie for the most popular incident, each incident is ranked 1; the next most popular nature 
is ranked 4.
g. Nature : This field is directly fetched from the report
h. EMSSAT : This is a boolean value that is True in two cases. First, if the Incident ORI was EMSSTAT or if the subsequent record or 
two contain an EMSSTAT at the same time and locaton.

2. Over what timeframe was the data collected?
The data consists from the past 2 months.

3. How was the data collected?
The data was collected using Norman PD's daily incident summary report and then augmenting it.
