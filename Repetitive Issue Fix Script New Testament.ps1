Write-host "================================="
Write-Host "      Fixing Quotation Issue     "
Write-Host "              NT                 "
Write-Host "================================="
Write-Host " *Script can be modified to fix* "
Write-Host " *  various repetitive issues  * "

if (Test-Path C:\Scripts) {Remove-Item C:\Scripts -Recurse;}
New-Item -path "C:\Scripts" -ItemType directory
New-Item -path "C:\Scripts\New" -ItemType directory

Get-childitem -path "C:\Users\$env:UserName\Dropbox\AndroidApps" -recurse | Out-GridView -PassThru | Get-ChildItem | Out-GridView -PassThru | Get-ChildItem | Out-GridView -PassThru | Copy-item -Destination C:\Scripts

$origbooks=@("40_Matthew.usfm","41_Mark.usfm","42_Luke.usfm","43_John.usfm","44_Acts.usfm","45_Romans.usfm","46_1_Corinthians.usfm","47_2_Corinthians.usfm","48_Galatians.usfm","49_Ephesians.usfm","50_Philippians.usfm","51_Colossians.usfm","52_1_Thessalonians.usfm","53_2_Thessalonians.usfm","54_1_Timothy.usfm","55_2_Timothy.usfm","56_Titus.usfm","57_Philemon.usfm","58_Hebrews.usfm","59_James.usfm","60_1_Peter.usfm","61_2_Peter.usfm","62_1_John.usfm","63_2_John.usfm","64_3_John.usfm","65_Jude.usfm","66_Revelation.usfm")
$books =@("40_Matthew_rev.usfm","41_Mark_rev.usfm","42_Luke_rev.usfm","43_John_rev.usfm","44_Acts_rev.usfm","45_Romans_rev.usfm","46_1_Corinthians_rev.usfm","47_2_Corinthians_rev.usfm","48_Galatians_rev.usfm","49_Ephesians_rev.usfm","50_Philippians_rev.usfm","51_Colossians_rev.usfm","52_1_Thessalonians_rev.usfm","53_2_Thessalonians_rev.usfm","54_1_Timothy_rev.usfm","55_2_Timothy_rev.usfm","56_Titus_rev.usfm","57_Philemon_rev.usfm","58_Hebrews_rev.usfm","59_James_rev.usfm","60_1_Peter_rev.usfm","61_2_Peter_rev.usfm","62_1_John_rev.usfm","63_2_John_rev.usfm","64_3_John_rev.usfm","65_Jude_rev.usfm","66_Revelation_rev.usfm")
$thisorig
$thisbook

for($i = 0; $i -lt $books.count; $i++){
    $thisbook = $books[$i].ToString()
    New-Item -Path "C:\Scripts\New\$thisbook" -ItemType file
    $thisorig = $origbooks[$i].ToString()
    $oldfile = "C:\Scripts\$thisorig"
    $newfile = "C:\Scripts\New\$thisbook"
    $text = (Get-Content -Path $oldfile -ReadCount 0) 
    $text -replace '<<', '"' -replace '>>', '"' -replace "<", "'" -replace ">", "'" | Set-Content -Path $newfile

    $newname = $origbooks[$i].ToString()
    Rename-Item -Path "C:\Scripts\New\$thisbook" $newname
}
pause