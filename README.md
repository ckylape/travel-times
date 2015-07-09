## Travel Time Calculator

This is a simple script that uses [Waze](https://www.waze.com/)'s API to calculate travel times to and from a specific location and store them in a Google Docs Spreadsheet. The results can be used for trying to decide where to move to based on where you work and several of your most liked neighborhoods.


### Setup

Before you can use the script you need to:

* Create a Google Service Account
* Create a Google Spreadsheet
* Create a Settings File


#### Google Service Account

1. You need to create a [Google Developers](https://console.developers.google.com) project and create a [Service Account API](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) OAuth key.
2. You then need to download the JSON key by clicking on the `Generate new JSON key` button while logged in to the developer console.
3. Rename the JSON key to `oauth.json` and move it to the same directory of the python script.

#### Google Docs Spreadsheet

1. Login to [Google Docs](https://docs.google.com/spreadsheets)
2. Click the red plus button to `Create new spreadsheet`
3. The script looks for the the following headers:

   | timestamp | address | route | minutes | direction |
   | --------- | ------- | ----- | ------- | --------- |
   | -    	   | -		 | -	 | - 	   | - 		   |

   The headers can be styled and should not be case sensitive.

4. Copy the spreadsheet key from the url so it can be added to the settings in the next step.

#### Settings File

**Example:**

```json
{
	"spreadsheet_key": "this_key_is_in_the_url",
	"sub": "your_email@gmail.com",
  	"start": {
      "lat": 40.441741,
      "lon": -80.007191
    },
	"locations": [
		{
			"address": "Location 1 Name",
			"lat": 40.338378,
			"lon": -79.950963
		},
		{
			"address": "Location 2 Name",
			"lat": 40.543276,
			"lon": -80.010159
		}
	],
    "run": {
      "hours": [6,7,8,9,14,15,16,17],
      "weekends": false
    }
}
```

1. Create a `settings.json` file in the same directory as the python script.

    * `spreadsheet_key` - the unique string that can be found inside the URL when viewing/editing the spreadsheet
    * `sub` - your gmail account tied to the Google Developer Console/Google Sheet
    * `start` - this is your starting address, this can be a work address, etc.
    * `run` - logic for when the script can and cannot be ran
        * `hours` - the 24 hour integer that the script can be ran, if the current hour is not listed then the script will not run
        * `weekends` - a boolean to check if the script is allowed to be ran on the weekend

2. You can use [LatLong.net](http://www.latlong.net/convert-address-to-lat-long.html) to find latitude and longitude coordinatres from addresses. Remember that longitude is East/West (sometimes labeled X), and latitude is North/South (sometimes labeled Y).

### Usage

If you are using a virutalenv you can activate it now before installing the dependencies.

```bash
pip install -r requirements.txt
```

You then can simply run the script with `python main.py` or create a CRON job or scheduled task to run the script automatically.