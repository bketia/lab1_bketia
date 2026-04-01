# Create archive directory if it does not exist
if (!(Test-Path "archive")) {
    New-Item -ItemType Directory -Name "archive"
}

# Check if grades.csv exists
if (!(Test-Path "grades.csv")) {
    Write-Host "Error: grades.csv not found."
    exit
}

# Create timestamp
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

# Create new archived filename
$newFile = "archive\grades_$timestamp.csv"

# Move and rename the file into archive
Move-Item grades.csv $newFile

# Create a new empty grades.csv file
New-Item grades.csv -ItemType File

# Log the action
"$timestamp | grades.csv | $newFile" >> organizer.log

Write-Host "Archive completed successfully." 