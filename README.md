# Discord Data Package Dumper

A simple Python script that extracts messages from your Discord data package for selected years and saves them to a `messages.csv` file.

This file is formatted for submitting a GDPR erasure request to Discord Support.

## Requirements

* Python 3
* Your Discord data package

## How to use

1. Download and unzip your Discord data package.
2. Place the Python script inside the unzipped Discord package folder.
3. Run the script.
4. A `messages.csv` file will be created in the same folder.
5. Send the resulting file to Discord Support as needed for your GDPR erasure request.

## What it does

* Reads message data from your Discord export
* Filters messages by the years you specify
* Exports the results to a CSV file
