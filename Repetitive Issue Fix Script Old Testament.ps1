Write-host "================================="
Write-Host "      Fixing Quotation Issue     "
Write-Host "              OT                 "
Write-Host "================================="
Write-Host " *Script can be modified to fix* "
Write-Host " *  various repetitive issues  * "

if (Test-Path C:\Scripts) {Remove-Item C:\Scripts -Recurse;}
New-Item -path "C:\Scripts" -ItemType directory
New-Item -path "C:\Scripts\New" -ItemType directory

Get-childitem -path "C:\Users\$env:UserName\Dropbox\AndroidApps" -recurse | Out-GridView -PassThru | Get-ChildItem | Out-GridView -PassThru | Get-ChildItem | Out-GridView -PassThru | Copy-item -Destination C:\Scripts

$origbooks=@("01_Genesis.usfm","02_Exodus.usfm","03_Leviticus.usfm","04_Numbers.usfm","05_Deuteronomy.usfm","06_Joshua.usfm","07_Judges.usfm","08_Ruth.usfm","09_1_Samuel.usfm","10_2_Samuel.usfm","11_1_Kings.usfm","12_2_Kings.usfm","13_1_Chronicles.usfm","14_2_Chronicles.usfm","15_Ezra.usfm","16_Nehemiah.usfm","17_Esther.usfm","18_Job.usfm","19_Psalms.usfm","20_Proverbs.usfm","21_Ecclesiastes.usfm","22_Song_of_Solomon.usfm","23_Isaiah.usfm","24_Jeremiah.usfm","25_Lamentations.usfm","26_Ezekiel.usfm","27_Daniel.usfm","28_Hosea.usfm","29_Joel.usfm","30_Amos.usfm","31_Obadiah.usfm","32_Jonah.usfm","33_Micah.usfm","34_Nahum.usfm","35_Habakkuk.usfm","36_Zephaniah.usfm","37_Haggai.usfm","38_Zechariah.usfm","39_Malachi.usfm")
$books =@("01_Genesis_rev.usfm","02_Exodus_rev.usfm","03_Leviticus_rev.usfm","04_Numbers_rev.usfm","05_Deuteronomy_rev.usfm","06_Joshua_rev.usfm","07_Judges_rev.usfm","08_Ruth_rev.usfm","09_1_Samuel_rev.usfm","10_2_Samuel_rev.usfm","11_1_Kings_rev.usfm","12_2_Kings_rev.usfm","13_1_Chronicles_rev.usfm","14_2_Chronicles_rev.usfm","15_Ezra_rev.usfm","16_Nehemiah_rev.usfm","17_Esther_rev.usfm","18_Job_rev.usfm","19_Psalms_rev.usfm","20_Proverbs_rev.usfm","21_Ecclesiastes_rev.usfm","22_Song_of_Solomon_rev.usfm","23_Isaiah_rev.usfm","24_Jeremiah_rev.usfm","25_Lamentations_rev.usfm","26_Ezekiel_rev.usfm","27_Daniel_rev.usfm","28_Hosea_rev.usfm","29_Joel_rev.usfm","30_Amos_rev.usfm","31_Obadiah_rev.usfm","32_Jonah_rev.usfm","33_Micah_rev.usfm","34_Nahum_rev.usfm","35_Habakkuk_rev.usfm","36_Zephaniah_rev.usfm","37_Haggai_rev.usfm","38_Zechariah_rev.usfm","39_Malachi_rev.usfm")
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